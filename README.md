# Citi Bike Optimization - Analysis on stations reliability

[Link to final presentation](https://docs.google.com/presentation/d/1wunxrt0I8V_x03g7h9n1G0RdKat9icyoEUHyc_WEW8E/edit?usp=sharing)
[Tableu Link](https://prod-useast-b.online.tableau.com/#/site/citibikeheatmap/workbooks/270847?:origin=card_share_link)

## Abstract

The goal of this project was to understand which Citi Bike stations can improve their redistribution and be more reliable. Some of these stations can be considered ‘not useful’ because during Rush Hour less than 20% of bikes are available.

Rush Hour was defined between 7.00am - 10:00am and from 5:00pm to 8:00pm

It was determined that stations with higher counts of zero available bikes have a lower bike availability average. 

## Design 
Citi Bike publishes real-time system data in General Bikeshare Feed Specification format. We started by logging the feed, every two minutes for a week using a serverless function hosted in Cloudflare and storing the data in a collection provided by Fauna DB.

Once the data was collected, it was clean using Python and analyzed using Pivot Tables in Microsoft Excel.

## Data

The real time data includes station capacity, bikes available, bikes disabled, last reported time, latitude and longitude among other fields; some fields were dynamically calculated such as if the last time reported is during a weekday and rush hour. 

In total filtered data contains 83,700 rows and 25 columns.

## Tools

* Cloudfare Workers
* Fauna DB
* Python for Data Processing
* Microsoft Excel
* Tableau for interactive visualizations

