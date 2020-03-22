import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from matplotlib import pyplot as plt
import pandas as pd
import datetime

import plotly.express as px


def dashboard(request):


	today = datetime.date.today()

	yesterday = today - datetime.timedelta(days=1)
	yesdate = yesterday.strftime("%m-%d-%Y")
	print(yesdate)
	

	covid_data= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+yesdate+'.csv')

	totalcounts = covid_data.sum()

	toptenresult = covid_data.groupby('Country/Region')['Country/Region', 'Confirmed', 'Deaths', 'Recovered'].sum().sort_values(by='Confirmed', ascending=False)[:10]
	
	canada_data = covid_data[covid_data['Country/Region']=='Canada'].drop(['Country/Region','Latitude', 'Longitude'], axis=1)
	totalcandata = canada_data.sum()
	
	canada_data['Active'] = canada_data['Confirmed'] - canada_data['Deaths'] - canada_data['Recovered']
	canada_data = canada_data[canada_data.sum(axis = 1) > 0]
 
	canada_data=canada_data.values.tolist()
	
	india_data = covid_data[covid_data['Country/Region']=='India'].drop(['Province/State','Latitude', 'Longitude'], axis=1)
	india_data = india_data.sum()
	
	context = dict(
        toptenresult=toptenresult,
        canada_data=canada_data,
        india_data=india_data,
        totalcounts=totalcounts,
        totalcandata=totalcandata
    )


	return render(request, "home.html",context)

