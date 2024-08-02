import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import requests

states_info = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
}

# "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY",
#     "Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO",
#     "Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC",
#     "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD",
#     "Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY"

# Configura e retorna o cliente da API do Reddit
def initialize_reddit():
    return praw.Reddit(
        client_id='pS9ynIbJmJCc3eDNudBu-Q',
        client_secret='uaNYaSdYl5qOjkdxgq5Ysm7KLoT3VQ',
        user_agent='mmm'
    )

# Inicializa e retorna o analisador de sentimentos 
def initialize_analyzer():
    return SentimentIntensityAnalyzer()

# Carrega a lista de estados
def load_states():
    names = []
    codes = []
    for state, code in states_info.items():
        names.append(state)
        codes.append(code)
    return {"name": names, "code": codes}

# Coleta e analisa os sentimentos das postagens de um estado
def analyze_state_sentiments(reddit, analyzer, states):
    sentiment_result = []
    for state in states:
        sum_total_sentiments = 0
        sum_posts_comments = 0
        posts = reddit.subreddit('all').search(state, sort='hot', time_filter='year', limit=5)
        for post in posts:
            sum_sentiments = 0
            comments = post.comments.list()
            for comment in comments[:10]:
                if isinstance(comment, praw.models.Comment):
                    sum_posts_comments += 1
                    sentiment_comment = analyzer.polarity_scores(comment.body)['compound']
                    sum_sentiments += sentiment_comment
            sum_total_sentiments += sum_sentiments 

        average_sentiment = sum_total_sentiments / sum_posts_comments if sum_posts_comments > 0 else 0
        sentiment_result.append(average_sentiment)
    return sentiment_result

# Cria e retorna um DataFrame com os estados e seus sentimentos medios
def create_dataframe(states, sentiment_result):
    data = {
        'state_name': states["name"],
        'sentiment': sentiment_result,
        'state_code': states["code"]
    }
    return pd.DataFrame(data=data)

# Funcao para montar e mostrar o mapa
def plot_map(df):
    fig = px.choropleth(df,
                        locations="state_code", 
                        locationmode="USA-states", 
                        color="sentiment", 
                        scope="usa", 
                        color_continuous_scale='RdBu',  # Usando a escala vermelho-verde
                        title='Sentimentos por Estado nos EUA',
                        hover_name="state_name",
                        hover_data={"state_name": False, "sentiment": True, "state_code": False})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Funcao principal para executar o fluxo de analise de sentimentos
# Configuracoes da API do Reddit e do analisador de sentimentos
def main():
    # Carrega as instancias necessarias
    reddit = initialize_reddit()
    analyzer = initialize_analyzer()

    # Carrega a lista de estados
    states = load_states()

    # Analisa os sentimentos dos estados
    sentiment_result = analyze_state_sentiments(reddit, analyzer, states["name"])

    # Cria e mostra o DataFrame
    df = create_dataframe(states, sentiment_result)

    # Mostra mapa dos Estados Unidos
    fig = plot_map(df)
    fig.show()

if __name__ == '__main__':
    main()