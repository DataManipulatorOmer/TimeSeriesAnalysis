#Libraries
!pip install plotly
import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta
import seaborn as sns
import matplotlib.pyplot as plt
#***********************************************************************************************************************
#Function No.1
#***********************************************************************************************************************
def dataLoader():
    st.subheader("Upload Your Weather Dataset")
#csv
    filee = st.file_uploader("Choose a CSV file", type=["csv"])

    if filee is not None:
# dataset
        df = pd.read_csv(filee)
        return df

#***********************************************************************************************************************
#Function No.2
#***********************************************************************************************************************
def OverviewSection():
    st.write("# Overview Section")
#Function
    df = dataLoader()
    if df is not None:
# Dataset Overview
        st.write("### Dataset Overview:")
        st.write(df.head())
#Dataset Information
        st.write("### Dataset Information:")
        st.write(df.info())
# Summary statistics
        st.write("### Summary Statistics:")
        st.write(df.describe())
#***********************************************************************************************************************
#Function No.3
#***********************************************************************************************************************
def TimeSeriesViz():
    st.write("# Time Series Visualizer")
    df = dataLoader()

    if df is not None:
# 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])
# Separate stacked area charts for each category 
        tempData = df[['Date', 'Temp_max', 'Temp_avg', 'Temp_min']]
        humidityData = df[['Date', 'Hum_max', 'Hum_avg', 'Hum_min']]
        windData = df[['Date', 'Wind_max', 'Wind_avg', 'Wind_min']]
        preciptiData = df[['Date', 'Precipit']]
#temp
        tempFigure = px.area(tempData, x='Date', y=['Temp_max', 'Temp_avg', 'Temp_min'], 
                           labels={'variable': 'Temperature Type'}, title='Temperature Trends Over the Years')
#humdity
        humidityFigure = px.area(humidityData, x='Date', y=['Hum_max', 'Hum_avg', 'Hum_min'], 
                               labels={'variable': 'Humidity Type'}, title='Humidity Trends Over the Years')
#wind
        windFigure = px.area(windData, x='Date', y=['Wind_max', 'Wind_avg', 'Wind_min'], 
                           labels={'variable': 'Wind Speed Type'}, title='Wind Speed Trends Over the Years')
#precipt
        precipitFigure = px.area(preciptiData, x='Date', y='Precipit', 
                               title='Precipitation Trends Over the Years')
# Customizion Of Layout
        tempFigure.update_layout(legend_title='Temperature Type', xaxis_title='Date', yaxis_title='Temperature')
        humidityFigure.update_layout(legend_title='Humidity Type', xaxis_title='Date', yaxis_title='Humidity')
        windFigure.update_layout(legend_title='Wind Speed Type', xaxis_title='Date', yaxis_title='Wind Speed')
        precipitFigure.update_layout(xaxis_title='Date', yaxis_title='Precipitation')
# Display
        st.plotly_chart(tempFigure, use_container_width=True)
        st.plotly_chart(humidityFigure, use_container_width=True)
        st.plotly_chart(windFigure, use_container_width=True)
        st.plotly_chart(precipitFigure, use_container_width=True)

#***********************************************************************************************************************
#Function No.4
#***********************************************************************************************************************
def weatherDistribution():
    st.write("# Weather Distribution")
    df = dataLoader()

    if df is not None:
# Distribution plots 
        tempDistFig = px.histogram(df, x='Temp_avg', nbins=30, title='Temperature Distribution', 
                                             color_discrete_sequence=['skyblue'],
                                             marginal='rug')
        tempDistFig.update_layout(bargap=0.1, showlegend=False)

        humidityDistFig = px.histogram(df, x='Hum_avg', nbins=30, title='Humidity Distribution', 
                                                 color_discrete_sequence=['lightgreen'],
                                                 marginal='rug')
        humidityDistFig.update_layout(bargap=0.1, showlegend=False)

# Distribution plots
        st.plotly_chart(tempDistFig, use_container_width=True)
        st.plotly_chart(humidityDistFig, use_container_width=True)

#***********************************************************************************************************************
#Function No.5
#***********************************************************************************************************************
def storyTellingSect():
    st.write("# Storytelling Section")
    df = dataLoader()

    if df is not None:
# Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Storytelling Questions
        ## (Stacked Area Chart)
        st.write("## Question 1: How has the average temperature changed over the years?")
        TempAvgStack = px.area(df, x='Date', y=['Temp_max', 'Temp_avg', 'Temp_min'], 
                                       labels={'variable': 'Temperature Type'}, 
                                       title='Temperature Trends Over the Years',
                                       line_shape='linear', color_discrete_sequence=['#FFC300', '#FF5733', '#C70039'])
        st.plotly_chart(TempAvgStack, use_container_width=True)

        ## 2. What are the trends in precipitation over different months?
        st.write("## Question 2: What are the trends in precipitation over different months?")
        df['Month'] = df['Date'].dt.month
        precipitationBoxPlot = px.box(df, x='Month', y='Precipit', points="all", 
                                           title='Precipitation Trends by Month')
        st.plotly_chart(precipitationBoxPlot, use_container_width=True)

        ## 3. How does humidity vary between day and night?
        st.write("## Question 3: How does humidity vary between day and night?")
        humidityBoxPlot = px.box(df, x='day_of_week', y=['Hum_max', 'Hum_min'], 
                                        labels={'variable': 'Humidity Type'}, 
                                        title='Humidity Variation: Day vs. Night')
        st.plotly_chart(humidityBoxPlot, use_container_width=True)

        ## Boundaries
        st.write("## Question 4: What is the distribution of wind speed on windy days?")
        windy_days = df[df['Wind_max'] > 15]  # Adjust the threshold for windy days
        windDistHist = px.histogram(windy_days, x='Wind_max', nbins=20, 
                                            title='Wind Speed Distribution on Windy Days',
                                            range_x=[0, 40],  # Set the x-axis range
                                            labels={'Wind_max': 'Wind Speed'})
        st.plotly_chart(windDistHist, use_container_width=True)

        ## 5. Are there any patterns in temperature and humidity during extreme weather events?
        st.write("## Question 5: Are there any patterns in temperature and humidity during extreme weather events?")
        extreme_temp_humidity = df[(df['Temp_max'] > 30) & (df['Hum_max'] > 80)]  # Adjust the thresholds
        fig_extreme_event = px.scatter(extreme_temp_humidity, x='Temp_max', y='Hum_max', 
                                       title='Temperature vs. Humidity during Extreme Events')
        st.plotly_chart(fig_extreme_event, use_container_width=True)
#***********************************************************************************************************************
#Function No.6
#***********************************************************************************************************************
def insightsAnalysis():
    st.write("# Insights and Analysis")
    df = dataLoader()

    if df is not None:
# Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

# Insights and Analysis Content
        ## 1. Compare different years for temperature patterns using stacked bar chart
        st.write("## Insight 1: Compare Different Years for Temperature Patterns")
        yearlyComb = px.bar(df, x='Date', y=['Temp_max', 'Temp_avg', 'Temp_min'], 
                                       labels={'variable': 'Temperature Type'},
                                       title='Temperature Patterns Over Different Years',
                                       color_discrete_sequence=['#FFC300', '#FF5733', '#C70039'],
                                       barmode='stack')
        st.plotly_chart(yearlyComb, use_container_width=True)

## 2. Analyze seasonal variations in humidity with a box plot
        st.write("## Insight 2: Analyze Seasonal Variations in Humidity")
        df['Month'] = df['Date'].dt.month
        seasonalHum = px.box(df, x='Month', y=['Hum_max', 'Hum_min'], 
                                        labels={'variable': 'Humidity Type'}, 
                                        title='Seasonal Variations in Humidity',
                                        color_discrete_sequence=['#4CAF50', '#8BC34A'])
        st.plotly_chart(seasonalHum, use_container_width=True)

## 3. Identify anomalies in precipitation for specific months with a scatter plot
        st.write("## Insight 3: Identify Anomalies in Precipitation for Specific Months")
        precipitationAnomalies = px.scatter(df, x='Month', y='Precipit', color='Precipit',
                                                 title='Precipitation Anomalies for Each Month',
                                                 color_continuous_scale='Viridis')
        st.plotly_chart(precipitationAnomalies, use_container_width=True)

#***********************************************************************************************************************
#Function No.7
#***********************************************************************************************************************
def userInteraction():
    st.sidebar.write("# User Interaction Section")
    df = dataLoader()

    if df is not None:
## Weather Condition Filter
        st.sidebar.write("## Weather Condition Filter")
        selected_weather_condition = st.sidebar.selectbox("Select a Weather Condition", df.columns[2:])

# Display the entire DataFrame
        st.write("## Data Overview")
        st.write(df)

# Create a plot using the entire data
        st.write("## Plot based on User Interaction")
        fig_user_interaction = px.line(df, x='Date', y=selected_weather_condition, 
                                       title=f'{selected_weather_condition} over Time')
        st.plotly_chart(fig_user_interaction, use_container_width=True)

#***********************************************************************************************************************
#Function No.8
#***********************************************************************************************************************
def correlationMatrix():
        df = dataLoader()
        if df is not None:
            st.write("# Correlation Matrix")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            # Calculate correlation matrix
            correlation_matrix = df.corr()

            # Display the correlation matrix using seaborn heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            st.pyplot()

            # Identify the most related columns
            most_related_columns = correlation_matrix.abs().unstack().sort_values(ascending=False).drop_duplicates().head(5)

            st.write("## Most Related Columns:")
            st.write(most_related_columns)

            # Generate a paragraph based on the identified columns
            st.write("## Insight:")
            st.write("The correlation matrix reveals the relationships between different weather parameters. "
                    "Among these, the following columns show the strongest correlations:")
            for pair in most_related_columns.index:
                st.write(f"- {pair[0]} and {pair[1]}")


#***********************************************************************************************************************
#Function No.9
#***********************************************************************************************************************
def main():
    st.title("StreamWeather Insights Generator - Navigation Bar")

# Define the navigation bar
    pages = {
        "Overview Section": OverviewSection,
        "Time Series Vis.": TimeSeriesViz,
        "Weather Distribution": weatherDistribution,
        "Storytelling Section": storyTellingSect,
        "Insights and Analysis": insightsAnalysis,
        "User Interaction Section": userInteraction,
        "Correlation Section":correlationMatrix,
    }

    page = st.sidebar.selectbox("Select a Page", list(pages.keys()))
    pages[page]()  

#***********************************************************************************************************************
#Function No.10
#***********************************************************************************************************************
if __name__ == "__main__":
    main()
