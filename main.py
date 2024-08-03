import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from wordcloud import WordCloud
import matplotlib.pyplot as plt

STATES_INFO = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY",
    "Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO",
    "Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC",
    "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD",
    "Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY"
}

REDDIT = praw.Reddit(client_id='CLIENT_ID',client_secret='CLIENT_SECRET',user_agent='mmm')

ANALYZER = SentimentIntensityAnalyzer()

# Load the list of states
def load_states():
    names = []
    codes = []
    for state, code in STATES_INFO.items():
        names.append(state)
        codes.append(code)
    return {"name": names, "code": codes}

# Helper function to process posts
def analyse_post(post):
    sum_sentiments = 0
    sum_comments = 0
    comments = post.comments.list()
    
    for comment in comments[:40]: 
        if isinstance(comment, praw.models.Comment):
            sum_sentiments += ANALYZER.polarity_scores(comment.body)['compound']
            sum_comments += 1
    
    post_data = {
        'post_title': post.title,
        'average_sentiments': sum_sentiments/sum_comments,
        'num_comments': sum_comments
    }
    
    return post_data, sum_sentiments

def analyze_state(state):
        sum_total_sentiments = 0
        sum_posts_comments = 0
        post_state_data = []
        posts = REDDIT.subreddit('all').search(state, sort='relevance', time_filter='year', limit=10)
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(analyse_post, post) for post in posts]
            for future in futures:
                post_data, sum_sentiments = future.result()
                post_state_data.append(post_data)
                sum_total_sentiments += sum_sentiments
                sum_posts_comments += post_data['num_comments']
        
        average_sentiment = sum_total_sentiments / sum_posts_comments if sum_posts_comments > 0 else 0
        post_state_data.append(average_sentiment)
        return average_sentiment, post_state_data, state

# Collect and analyze the sentiment of posts for a state
def analyze_state_sentiments(states):
    sentiments_result = []
    results = {}
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze_state, state) for state in states]
        for future in futures:
            average_sentiment, post_state_data, state = future.result()
            sentiments_result.append(average_sentiment)
            results[state] = post_state_data
    
    return sentiments_result, results

# Create and return a DataFrame with states and their average sentiments
def create_dataframe(states, sentiment_result):
    data = {
        'state_name': states["name"],
        'sentiment': sentiment_result,
        'state_code': states["code"]
    }
    return pd.DataFrame(data=data)

# Function to build and show the map
def plot_map(df):
    fig = px.choropleth(df,
                        locations="state_code", 
                        locationmode="USA-states", 
                        color="sentiment", 
                        scope="usa", 
                        color_continuous_scale='RdBu',  
                        title='Sentiments by US State',
                        hover_name="state_name",
                        hover_data={"state_name": False, "sentiment": True, "state_code": False})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Function showing a bars graphics of distribuition of the sentiment by state
def plot_sentiment_distribution(df):

    # Sort the DataFrame by sentiment in ascending order
    df_sorted = df.sort_values(by="sentiment", ascending=True)
    
    # Create the bar chart
    fig = px.bar(df_sorted,
                 x="state_name",
                 y="sentiment",
                 color="sentiment",
                 color_continuous_scale='RdBu',
                 title="Sentiment Distribution by US State",
                 labels={"state_name": "State", "sentiment": "Average Sentiment"})
    
    # Update layout to change the background color
    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Average Sentiment",
        plot_bgcolor='gray',  
        paper_bgcolor='white' 
    )

    return fig

def plot_posts_sentiments(results, entry):
    posts = results[entry.get()][:-1]
    
    data = {
        "post_title": [post['post_title'] for post in posts],
        "sentiment": [post['average_sentiments'] for post in posts]
    }
    
    df = pd.DataFrame(data)

    df_sorted = df.sort_values(by='sentiment', ascending=True)
    
    fig = px.bar(df_sorted,
                 x="post_title",
                 y="sentiment",
                 color="sentiment",
                 color_continuous_scale='RdBu',
                 title=f'Sentiments of Posts of {entry.get()}',
                 labels={"sentiment": "Sentiment Value", "post_title": "Post Title"},
                 orientation='v')
    
    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        xaxis_title="Post Title",
        yaxis_title="Sentiment Value",
        xaxis_tickfont=dict(size=14),  
        xaxis_title_font=dict(size=16),  
        yaxis_title_font=dict(size=16)   
    )

    fig.update_traces(marker=dict(line=dict(color='black', width=1))) 
    
    fig.show()

def get_input_state_name(results):
    root = tk.Tk()
    root.title("Sentiments Posts by State")

    font_settings = ('Arial', 18)

    entry_label = tk.Label(root, text="Type the state name:", font=font_settings)
    entry_label.pack(pady=10, padx=10)
    entry = tk.Entry(root, font=font_settings, width=30)
    entry.pack(pady=10, padx=10)

    search_button = tk.Button(root, text="Search", font=font_settings, command=lambda: plot_posts_sentiments(results, entry))
    search_button.pack(pady=10, padx=10)

    root.mainloop()

def main():
    # Load the list of states
    states = load_states()

    # Analyze the sentiments of the states
    sentimentResult, results = analyze_state_sentiments(states["name"])

    # Create and show the DataFrame
    df = create_dataframe(states, sentimentResult)

    # Create and show a bars graph of sentiments by state
    fig = plot_sentiment_distribution(df)
    fig.show()

    # Create and show the map of the United States
    fig1 = plot_map(df)
    fig1.show()

    # Show State Posts Sentiments
    get_input_state_name(results)

if __name__ == '__main__':
    main()