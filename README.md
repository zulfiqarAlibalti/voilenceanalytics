<div align="center">
  <br />
  <a href="https://youtu.be/vpvtZZi5ZWk?feature=shared" target="_blank">
    <img src="https://github.com/zulfiqarAlibalti/voilenceanalytics/blob/master/assets/img/project-banner.png" alt="Project Banner">
  </a>
  <br />

  <div>
    <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB" alt="python" />
    <img src="https://img.shields.io/badge/-Pandas-black?style=for-the-badge&logoColor=white&logo=pandas&color=150458" alt="pandas" />
    <img src="https://img.shields.io/badge/-Plotly-black?style=for-the-badge&logoColor=white&logo=plotly&color=3F4F75" alt="plotly" />
    <img src="https://img.shields.io/badge/-Dash-black?style=for-the-badge&logoColor=white&logo=dash&color=008CCF" alt="dash" />
  </div>

  <h3 align="center">Twitter Violence Extremism Data Analytics Dashboard</h3>

  <div align="center">
    Analyze and visualize Twitter data related to violence extremism from 2012 to 2015. This web application leverages various Python libraries for data processing, sentiment analysis, and visualization. <a href="" target="_blank"><b>Twitter Violence Extremism Data Analytics Dashboard</b></a>
  </div>
</div>

## 📋 <a name="table">Table of Contents</a>

1. 🤖 [Introduction](#introduction)
2. ⚙️ [Tech Stack](#tech-stack)
3. 🔋 [Features](#features)

## 🚨 About

This project is a comprehensive web application built with Dash and Flask, which analyzes Twitter data related to violence extremism. It includes functionalities like sentiment analysis, data visualization with Plotly, word cloud generation, and geolocation mapping. The data spans from 2012 to 2015 and offers insights into user activities, sentiment trends, and more.

![Twitter Violence Extremism Data Analytics Demo](https://github.com/zulfiqarAlibalti/voilenceanalytics/blob/master/assets/img/demo.gif)

## <a name="introduction">🤖 Introduction</a>

This application simplifies the analysis of Twitter data related to violence extremism. It leverages Python libraries such as Pandas, Plotly, and NLTK for data processing and visualization. The app provides an intuitive dashboard for exploring sentiment trends, user activities, and more.

## <a name="tech-stack">⚙️ Tech Stack</a>

- Python
- Pandas
- Plotly
- Dash
- Flask
- TextBlob
- NLTK
- WordCloud
- Geopy
- PDFKit

## <a name="features">🔋 Features</a>

👉 **Sentiment Analysis**: Analyzes the sentiment of tweets using TextBlob, classifying them as positive, negative, or neutral.

👉 **Timeline Visualization**: Displays sentiment trends over time using line charts.

👉 **Donut Chart for Sentiment Distribution**: Visualizes the distribution of sentiments in a donut chart.

👉 **Top Users and Followers**: Identifies and displays the top users by tweet count and follower count.

👉 **Word Cloud Generation**: Creates a word cloud from the tweet text data.

👉 **Geolocation Mapping**: Maps the locations of tweets using geolocation data.

👉 **Top Hashtags and City-wise Sentiment**: Displays the most popular hashtags and sentiment distribution across top cities.

👉 **PDF Report Generation**: Allows users to download the visualizations as a PDF report.

## 🚀 Quick Start

1. **Clone the repository**:
    ```bash
    git clone <https://github.com/zulfiqarAlibalti/voilenceanalytics.git>
    cd <voilenceanalytics>
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python app.py
    ```

## 🔗 Links

- [YouTube Demo]()
- [Project Repository](https://github.com/zulfiqarAlibalti/voilenceanalytics.git)

## 🛠️ Additional Notes

- Ensure that NLTK data is downloaded before running the application:
    ```python
    import nltk
    nltk.download('punkt')
    ```
- Make sure to update the path to `wkhtmltopdf` in the `pdfkit` configuration if running on a different system.

Feel free to customize and expand this README as needed for your specific project requirements.
