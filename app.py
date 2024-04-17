import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load the dataset
df = pd.read_csv("ProcessedTweets.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Twitter Data Dashboard"),
    
    # Dropdown menu for month selection
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in df['Month'].unique()],
        value=df['Month'].unique()[0]
    ),
    
    # Range slider for sentiment
    html.Label('Sentiment Range'),
    dcc.RangeSlider(
        id='sentiment-slider',
        min=df['Sentiment'].min(),
        max=df['Sentiment'].max(),
        step=0.1,
        marks={i: str(i) for i in range(int(df['Sentiment'].min()), int(df['Sentiment'].max())+1)},
        value=[df['Sentiment'].min(), df['Sentiment'].max()]
    ),
    
    # Range slider for subjectivity
    html.Label('Subjectivity Range'),
    dcc.RangeSlider(
        id='subjectivity-slider',
        min=df['Subjectivity'].min(),
        max=df['Subjectivity'].max(),
        step=0.1,
        marks={i: str(i) for i in range(int(df['Subjectivity'].min()), int(df['Subjectivity'].max())+1)},
        value=[df['Subjectivity'].min(), df['Subjectivity'].max()]
    ),
    
    # Scatter plot
    dcc.Graph(id='scatter-plot'),
    
    # Tweet display table
    html.H3("Tweet Display"),
    html.Div(id='tweet-table')
])

# Callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = df[(df['Month'] == selected_month) &
                     (df['Sentiment'] >= sentiment_range[0]) & (df['Sentiment'] <= sentiment_range[1]) &
                     (df['Subjectivity'] >= subjectivity_range[0]) & (df['Subjectivity'] <= subjectivity_range[1])]
    
    return {
        'data': [
            {'x': filtered_df['Dimension 1'], 'y': filtered_df['Dimension 2'], 'type': 'scatter', 'mode': 'markers'}
        ],
        'layout': {}
    }

# Callback to update the tweet display table
@app.callback(
    Output('tweet-table', 'children'),
    [Input('scatter-plot', 'selectedData')]
)
def update_tweet_table(selected_data):
    if selected_data:
        selected_points = [point['pointIndex'] for point in selected_data['points']]
        selected_tweets = df.iloc[selected_points]['RawTweet']
        return html.Table([
            html.Tr(html.Td(tweet)) for tweet in selected_tweets
        ])
    else:
        return html.Table()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
