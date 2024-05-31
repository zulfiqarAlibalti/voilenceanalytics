import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from geopy.geocoders import Nominatim
from textblob import TextBlob
import nltk
import pdfkit
from flask import Flask, send_file

# Download NLTK data
nltk.download('punkt')

# Load data
file_path = 'voilence-tweets2012-15.csv'
df = pd.read_csv(file_path)

# Clean the Timestamp column
def clean_timestamp(ts):
    try:
        return pd.to_datetime(ts)
    except:
        return pd.NaT

df['Timestamp'] = df['Timestamp'].apply(clean_timestamp)
df = df.dropna(subset=['Timestamp'])

# Sentiment analysis using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

df['Sentiment'] = df['Text'].apply(analyze_sentiment)

# Sentiment Timeline
sentiment_counts_over_time = df.groupby([df['Timestamp'].dt.date, 'Sentiment']).size().unstack(fill_value=0)
timeline_fig = px.line(sentiment_counts_over_time, title='Sentiment Over Time')
timeline_fig.update_layout(xaxis_title='Date', yaxis_title='Tweet Count')

# Sentiment Donut
sentiment_counts = df['Sentiment'].value_counts()
donut_fig = px.pie(values=sentiment_counts, names=sentiment_counts.index, hole=0.4, title='Sentiment Distribution')

# Top Users
top_users = df['User'].value_counts().head(10)
top_users_fig = go.Figure(go.Bar(
    x=top_users.values,
    y=top_users.index,
    orientation='h',
    marker=dict(
        color=top_users.values,
        colorscale='Viridis',
        showscale=True
    )
))
top_users_fig.update_layout(title='Top Users', xaxis_title='Tweet Count', yaxis_title='User')

# Top Followers
top_followers = df.groupby('User')['Followers'].max().sort_values(ascending=False).head(10)
top_followers_fig = go.Figure(go.Bar(
    x=top_followers.values,
    y=top_followers.index,
    orientation='h',
    marker=dict(
        color=top_followers.values,
        colorscale='Viridis',
        showscale=True
    )
))
top_followers_fig.update_layout(title='Top Followers', xaxis_title='Follower Count', yaxis_title='User')

# Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Text']))
wc_img = BytesIO()
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(wc_img, format='png')
wc_img.seek(0)
wc_base64 = base64.b64encode(wc_img.getvalue()).decode()

# Geolocation Map
geolocator = Nominatim(user_agent="geoapiExercises")
locations = df['Location'].dropna().unique()[:100]
location_data = []
for location in locations:
    try:
        loc = geolocator.geocode(location)
        if loc:
            location_data.append({'Location': location, 'lat': loc.latitude, 'lon': loc.longitude})
    except:
        pass

# Convert to DataFrame
location_df = pd.DataFrame(location_data)
if not location_df.empty:
    geo_fig = px.scatter_mapbox(location_df, lat='lat', lon='lon', text='Location', zoom=2, title='Geolocation of Tweets')
    geo_fig.update_layout(mapbox_style="open-street-map")
else:
    geo_fig = go.Figure()
    geo_fig.update_layout(title='Geolocation of Tweets')

# Top Positive and Negative Sentiment
positive_sentiment = df[df['Sentiment'] == 'positive']['User'].value_counts().head(10)
negative_sentiment = df[df['Sentiment'] == 'negative']['User'].value_counts().head(10)

positive_fig = go.Figure(go.Bar(
    x=positive_sentiment.values,
    y=positive_sentiment.index,
    orientation='h',
    marker=dict(
        color=positive_sentiment.values,
        colorscale='Viridis',
        showscale=True
    )
))
positive_fig.update_layout(title='Top Positive Sentiment Users', xaxis_title='Tweet Count', yaxis_title='User')

negative_fig = go.Figure(go.Bar(
    x=negative_sentiment.values,
    y=negative_sentiment.index,
    orientation='h',
    marker=dict(
        color=negative_sentiment.values,
        colorscale='Viridis',
        showscale=True
    )
))
negative_fig.update_layout(title='Top Negative Sentiment Users', xaxis_title='Tweet Count', yaxis_title='User')

# Top Hashtags
df['Hashtags'] = df['Text'].apply(lambda x: [word for word in x.split() if word.startswith('#')])
all_hashtags = sum(df['Hashtags'], [])
top_hashtags = pd.Series(all_hashtags).value_counts().head(10)

hashtags_fig = go.Figure(go.Bar(
    x=top_hashtags.values,
    y=top_hashtags.index,
    orientation='h',
    marker=dict(
        color=top_hashtags.values,
        colorscale='Viridis',
        showscale=True
    )
))
hashtags_fig.update_layout(title='Top Hashtags', xaxis_title='Count', yaxis_title='Hashtag')

# Top 5 City-wise Sentiment
top_cities = df['Location'].value_counts().head(5).index
city_sentiment = df[df['Location'].isin(top_cities)].groupby(['Location', 'Sentiment']).size().unstack(fill_value=0)
city_sentiment_fig = px.bar(city_sentiment, title='Top 5 City-wise Sentiment')
city_sentiment_fig.update_layout(xaxis_title='City', yaxis_title='Tweet Count')

# Dash App Layout with Custom CSS
server = Flask(__name__)
app = Dash(__name__, server=server)

app.layout = html.Div(className='container', children=[
    html.H1('Twitter  Voilence Extremism Data Analytics Dashboard'),
    html.Button("Download PDF", id="btn-pdf", className='btn btn-primary'),
    dcc.Download(id="download-pdf"),
    html.Div(className='card', children=[
        dcc.Graph(figure=timeline_fig)
    ]),
    html.Div(className='row', children=[
        html.Div(className='column', children=[
            html.Div(className='card', children=[
                dcc.Graph(figure=donut_fig)
            ])
        ]),
        html.Div(className='column', children=[
            html.Div(className='card', children=[
                dcc.Graph(figure=top_followers_fig)
            ])
        ])
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=top_users_fig)
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=positive_fig)
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=negative_fig)
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=hashtags_fig)
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=city_sentiment_fig)
    ]),
    html.Div(className='card', children=[
        html.H3('Word Cloud'),
        html.Img(src='data:image/png;base64,{}'.format(wc_base64))
    ]),
    html.Div(className='card', children=[
        dcc.Graph(figure=geo_fig)
    ])
])

@app.callback(
    Output("download-pdf", "data"),
    [Input("btn-pdf", "n_clicks")],
    prevent_initial_call=True
)
def download_pdf(n_clicks):
    rendered_html = app.server.app_context().app.render_template('index.html')
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(rendered_html, 'output.pdf', configuration=config)
    return send_file('output.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)
