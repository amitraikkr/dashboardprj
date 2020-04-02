import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np


def readcsv():
	
	today = datetime.now()

	yesterday = today - timedelta(days=1)
	yesdate = yesterday.strftime("%m-%d-%Y")
	print(yesdate)
	covid_data= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+yesdate+'.csv')

	return covid_data

def dashboard(request):

	covid_data = readcsv()
	
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

def plot_graph(covid_data12,data_type):

	if data_type == 'Confirmed':
		typecolor = 'rgb(11,164,242)'

	elif data_type == 'Deaths':
		typecolor = 'rgb(242,11,49)'

	else:
		typecolor = 'rgb(0,222,0)'


	covid_dataTop = covid_data12.sort_values(by=data_type,ascending=False)[:10]
	index = covid_dataTop.index
	values = covid_dataTop[data_type]
	fig = go.Figure(data=go.Bar(y=values,x=index, marker=dict(color=typecolor)))
	fig.update_layout(
		autosize=False,
		width=700,
		height=500,
		title="Top Ten Countries - ("+data_type+" Cases)",
	)
	fig.update_yaxes(automargin=True)
	plt_div = plot(fig, output_type='div')

	return plt_div

def plot_cntrypttrn():

    df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_confirmed1 = df_confirmed.drop(['Province/State','Lat','Long'],axis=1)
    case_nums_country = df_confirmed1.groupby("Country/Region").sum().apply(lambda x: x[x > 0].count(), axis =0)
    d = [datetime.strptime(date,'%m/%d/%y').strftime("%d %b") for date in case_nums_country.index]

    fig = go.Figure(data=go.Line(y=case_nums_country,x=d,marker=dict(color='rgb(11,164,242)')))
    fig.update_layout(
    	autosize=True,
    	width=900,
    	height=700,
    )
    fig.update_layout(title='Number of countries affected over the time',
    	xaxis_title='Dates',
    	yaxis_title='# of countries')

    plt_div = plot(fig, output_type='div')

    return plt_div    


def graph_confrate():


    df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_confirmed1 = df_confirmed.drop(['Province/State','Lat','Long'],axis=1)
    case_nums_country = df_confirmed1.groupby("Country/Region").sum().apply(lambda x: x[x > 0].count(), axis =0)
    d = [datetime.strptime(date,'%m/%d/%y').strftime("%d %b") for date in case_nums_country.index]

    stats = [df_confirmed1]

    for x,stat in enumerate(stats):
    	cases = np.sum(np.asarray(stat.iloc[:,5:]),axis = 0)[x:]

    fig = go.Figure(data=go.Line(y=cases,x=d,marker=dict(color='rgb(11,164,242)')))
    fig.update_layout(
    	autosize=True,
    	width=900,
    	height=700,
    )

    fig.update_layout(title='Number of cases over the time',
                   xaxis_title='Dates',
                   yaxis_title='# of Cases')
    
    plt_div = plot(fig, output_type='div')

    return plt_div  

def graph_view(request):

	covid_data = readcsv()
	covid_data1 = covid_data[['Country_Region','Confirmed','Deaths','Recovered']]
	covid_data12 = covid_data1.groupby('Country_Region').sum()
	
	plt_divcnf = plot_graph(covid_data12,"Confirmed")
	plt_divdth = plot_graph(covid_data12,"Deaths")
	plt_divrcvr = plot_graph(covid_data12,"Recovered")

	ctrypattrn = plot_cntrypttrn()

	grph_cnfrate = graph_confrate()

	context = dict(
	
		plt_divcnf=plt_divcnf,
		plt_divdth=plt_divdth,
		plt_divrcvr=plt_divrcvr,
		ctrypattrn=ctrypattrn,
		grph_cnfrate=grph_cnfrate

	)

	return render(request,"graphvw.html",context)