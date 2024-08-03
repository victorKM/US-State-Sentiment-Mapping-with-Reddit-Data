# Sentiment Analysis of Reddit Posts by US State

This project performs sentiment analysis on Reddit posts related to US states and visualizes the results on an interactive map. We use the Reddit API to collect posts and comments, and the VADER library for sentiment analysis.

# Objective

The goal of this project is to evaluate the sentiment of people towards each US state based on Reddit posts and comments. The results are displayed on a map of the US, where each state is colored according to the average sentiment expressed in the posts and comments. States that are more blue are perceived more positively, while states that are more red are perceived more negatively.

# Features

1. **Data Collection**: Uses the Reddit API (praw) to collect posts and comments
2. **Sentiment Analysis**: Applies sentiment analysis using the vaderSentiment library
3. **Visualization**: Creates an interactive map of the United States and bars graph using plotly to visualize the sentiment analysis results

# Code Structure

- `load_states()`: Loads the list of states and their codes
- `analyse_post(post)`: Processes a post and its comments, calculating the average sentiment
- `analyse_state(state)`: Collect and analyzes the sentiment of the state posts
- `analyze_state_sentiments(reddit, analyzer, states)`: Collects and analyzes the sentiment of posts for each state
- `create_dataframe(states, sentiment_result)`: Creates a DataFrame with states and their average sentiments
- `plot_map(df)`: Creates and returns an interactive map of the United States with sentiment by state
- `plot_sentiment_distribution(df)`: Creates and returns an bar graphic of sentiment distribution by state
- `plot_posts_sentiments`: Creates and show graph bar graphics of the posts sentiments of a state
- `get_input_stae_name(posts_state_data):` Get input value from user to plot the posts sentiments of this state
- `__main__()`: Main function that runs the entire sentiment analysis workflow

# Example

![image1](https://github.com/user-attachments/assets/a608217b-48da-454f-95df-7f011dc17e19)

![image2](https://github.com/user-attachments/assets/d83fab3a-a88e-4d1c-886e-63788fffb6d9)

![image3](https://github.com/user-attachments/assets/3616324b-6406-4ddb-a6f8-3a5252ba33b3)

![imagem4](https://github.com/user-attachments/assets/8270f4db-b46b-4f77-b65d-363e530795f2)

![imagem5](https://github.com/user-attachments/assets/84638196-3a99-4720-bcfe-ea83277609af)

# Techonlogies Used

- Python
- Libraries: praw, pandas, vaderSentiment, plotly, concurrent, tkinter, matplotlib
