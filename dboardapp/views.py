import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from matplotlib import pyplot as plt
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np


def dashboard(request):


	today = datetime.date.today()

	yesterday = today - datetime.timedelta(days=1)
	yesdate = yesterday.strftime("%m-%d-%Y")
	print(yesdate)
	

	covid_data= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+yesdate+'.csv')

	totalcounts = covid_data.sum()

	covid_data['Deathsrate'] = ((covid_data['Deaths'] / covid_data['Confirmed']) * 100)
	covid_data['Recoveredrate'] = ((covid_data['Recovered'] / covid_data['Confirmed']) * 100)
	
	toptenresult = covid_data.groupby('Country_Region')['Country_Region', 'Confirmed', 'Deaths', 'Deathsrate','Recovered','Recoveredrate'].sum().sort_values(by='Confirmed', ascending=False)[:50]
	
	covid_data12 = covid_data.groupby('Country_Region').sum()

	temp_df = pd.DataFrame(covid_data12['Confirmed'])
	temp_df = temp_df.reset_index()

	fig = px.choropleth(temp_df, locations="Country_Region",
                   color=np.log10(temp_df.iloc[:,-1]),
                   hover_name="Country_Region",
                   hover_data=["Confirmed"],
                   color_continuous_scale=px.colors.sequential.Plasma,locationmode="country names")

	fig.update_geos(fitbounds="locations", visible=False)
	fig.update_coloraxes(colorbar_title="Confirmed Cases",colorscale="Blues")

	plt_div = plot(fig, output_type='div')
	#print(plt_div)

	context = dict(
        toptenresult=toptenresult,
        totalcounts=totalcounts,
        pltdiv=plt_div,
    )


	return render(request, "home.html",context)

def graph_view(request):

	return render(request,"graphvw.html")