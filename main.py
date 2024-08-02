import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor

states_info = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY",
    "Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO",
    "Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC",
    "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD",
    "Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY"
}

# Set up and return the Reddit API client
def initialize_reddit():
    return praw.Reddit(
        client_id='CLIENT_ID',
        client_secret='CLIENT_SECRET',
        user_agent='mmm'
    )

# Initialize and return the sentiment analyzer
def initialize_analyzer():
    return SentimentIntensityAnalyzer()

# Load the list of states
def load_states():
    names = []
    codes = []
    for state, code in states_info.items():
        names.append(state)
        codes.append(code)
    return {"name": names, "code": codes}

# Helper function to process posts
def process_post(post, analyzer):
    sum_sentiments = 0
    sum_posts_comments = 0
    comments = post.comments.list()
    
    for comment in comments[:40]:  # Limit the number of comments to process
        if isinstance(comment, praw.models.Comment):
            sentiment_comment = analyzer.polarity_scores(comment.body)['compound']
            sum_sentiments += sentiment_comment
            sum_posts_comments += 1
    
    return sum_sentiments, sum_posts_comments

# Collect and analyze the sentiment of posts for a state
def analyze_state_sentiments(reddit, analyzer, states, time):
    def analyze_state(state):
        sum_total_sentiments = 0
        sum_posts_comments = 0
        posts = reddit.subreddit('all').search(state, sort='relevance', time_filter=time, limit=10)
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_post, post, analyzer) for post in posts]
            for future in futures:
                sum_sentiments, num_comments = future.result()
                sum_total_sentiments += sum_sentiments
                sum_posts_comments += num_comments
        
        average_sentiment = sum_total_sentiments / sum_posts_comments if sum_posts_comments > 0 else 0
        return average_sentiment
    
    # Analyze all states
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_state, states))
    
    return results

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
        plot_bgcolor='gray',  # Cor de fundo do gráfico
        paper_bgcolor='white'  # Cor de fundo do papel (opcional)
    )

    return fig

# Main function to execute the sentiment analysis workflow
def main():
    # Load necessary instances
    reddit = initialize_reddit()
    analyzer = initialize_analyzer()

    # Load the list of states
    states = load_states()

    # Analyze the sentiments of the states
    sentiment_result = analyze_state_sentiments(reddit, analyzer, states["name"], time='year')

    # Create and show the DataFrame
    df = create_dataframe(states, sentiment_result)

    # Create and show a bars graph of sentiments by state
    fig = plot_sentiment_distribution(df)
    fig.show()

    # Create and show the map of the United States
    fig1 = plot_map(df)
    fig1.show()

if __name__ == '__main__':
    main()