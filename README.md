# Sentiment Analysis of Reddit Posts by US State

This project performs sentiment analysis on Reddit posts related to US states and visualizes the results on an interactive map. We use the Reddit API to collect posts and comments, and the VADER library for sentiment analysis.

# Objective

The goal of this project is to evaluate the sentiment of people towards each US state based on Reddit posts and comments. The results are displayed on a map of the US, where each state is colored according to the average sentiment expressed in the posts and comments.

# Features

1. **Data Collection**: Uses the Reddit API (praw) to collect posts and comments.
2. **Sentiment Analysis**: Applies sentiment analysis using the vaderSentiment library.
3. **Visualization**: Creates an interactive map of the United States using plotly to visualize the sentiment analysis results.

# Code Structure

- `initialize_reddit()`: Configures and returns the Reddit API client.
