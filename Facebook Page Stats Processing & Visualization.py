# processing section
import pandas as pd
import numpy as np
import os

pd.set_option('max_columns', 100)
pd.set_option('max_rows', 200)

os.chdir("C:/Users/user/Desktop/Coding/TYAD/Facebook")


# load page data
page_data = pd.read_csv("Facebook Insights Data Export - 臺灣青年民主協會 TYAD - 2019-07-05.csv")

# define columns to be retrieved
# be really careful when modifing!!!
columns_to_be_retrieved = ['Date',
                           'Lifetime Total Likes',
                           'Daily New Likes',
                           'Daily Page Engaged Users',
                           # the number of people who had any content from your Page or about your Page enter their screen
                           'Daily Total Reach',
                           'Daily Organic Reach',
                           'Daily Viral Reach',
                           # the number of times any content from your Page or about your Page entered a person's screen
                           'Daily Total Impressions',
                           'Daily Organic impressions',
                           'Daily Viral impressions',
                           # the number of people who had any of your Page's posts enter their screen
                           'Daily Reach Of Page Posts',
                           'Daily Organic Reach of Page posts',
                           'Daily Viral Reach Of Page Posts',
                           # the number of times your Page's posts entered a person's screen
                           'Daily Total Impressions of your posts',
                           'Daily Organic impressions of your posts',
                           'Daily Viral Impressions Of Your Posts',
                           # the number of people your Page reached broken down by how many times people saw any content about your Page
                           'Daily Total Frequency Distribution - 1',
                           'Daily Total Frequency Distribution - 2',
                           'Daily Total Frequency Distribution - 3',
                           'Daily Total Frequency Distribution - 4',
                           'Daily Total Frequency Distribution - 5',
                           'Daily Total Frequency Distribution - 6-10',
                           'Daily Total Frequency Distribution - 11-20',
                           'Daily Total Frequency Distribution - 21+',
                           # the number of people who saw your Page posts, broken down by how many times people saw your posts
                           'Daily Page Posts Frequency Distribution - 1',
                           'Daily Page Posts Frequency Distribution - 2',
                           'Daily Page Posts Frequency Distribution - 3',
                           'Daily Page Posts Frequency Distribution - 4',
                           'Daily Page Posts Frequency Distribution - 5',
                           'Daily Page Posts Frequency Distribution - 6-10',
                           'Daily Page Posts Frequency Distribution - 11-20',
                           'Daily Page Posts Frequency Distribution - 21+',
                           # aggregated demographic data about the people who like your Page based on the age and gender information they provide in their user profiles
                           'Lifetime Likes by Gender and Age - F.13-17',
                           'Lifetime Likes by Gender and Age - F.18-24',
                           'Lifetime Likes by Gender and Age - F.25-34',
                           'Lifetime Likes by Gender and Age - F.35-44',
                           'Lifetime Likes by Gender and Age - F.45-54',
                           'Lifetime Likes by Gender and Age - F.55-64',
                           'Lifetime Likes by Gender and Age - F.65+',
                           'Lifetime Likes by Gender and Age - M.13-17',
                           'Lifetime Likes by Gender and Age - M.18-24',
                           'Lifetime Likes by Gender and Age - M.25-34',
                           'Lifetime Likes by Gender and Age - M.35-44',
                           'Lifetime Likes by Gender and Age - M.45-54',
                           'Lifetime Likes by Gender and Age - M.55-64',
                           'Lifetime Likes by Gender and Age - M.65+',
                           # the number of People Talking About the Page by user age and gender
                           'Daily Demographics: People Talking About This - F.13-17',
                           'Daily Demographics: People Talking About This - F.18-24',
                           'Daily Demographics: People Talking About This - F.25-34',
                           'Daily Demographics: People Talking About This - F.35-44',
                           'Daily Demographics: People Talking About This - F.45-54',
                           'Daily Demographics: People Talking About This - F.55-64',
                           'Daily Demographics: People Talking About This - F.65+',
                           'Daily Demographics: People Talking About This - M.13-17',
                           'Daily Demographics: People Talking About This - M.18-24',
                           'Daily Demographics: People Talking About This - M.25-34',
                           'Daily Demographics: People Talking About This - M.35-44',
                           'Daily Demographics: People Talking About This - M.45-54',
                           'Daily Demographics: People Talking About This - M.55-64',
                           'Daily Demographics: People Talking About This - M.65+']

# retrieve data
retrieved_data = page_data[columns_to_be_retrieved]

# remove first row, the description of variable
retrieved_data = retrieved_data.drop(retrieved_data.index[0])

# fill NaN with value 0
retrieved_data = retrieved_data.fillna(value = 0)

# change value's type to int
retrieved_data[retrieved_data.columns[1:]] = retrieved_data[retrieved_data.columns[1:]].applymap(np.int64)

# save to csv file if needed
# retrieved_data.to_csv("retrieved_data.csv")


# visualization section (need to be executed squentially)
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

%matplotlib inline

sns.set_style("darkgrid",{"font.sans-serif":['simhei', 'Arial']})


# create barplot for Lifetime Likes by Gender and Age

# set index of lastest record without value 0
lastest_valid_record_index = len(retrieved_data) - 2

# set index of needed columns
column_range = range(32, 46)

# get data
data_for_barplot = retrieved_data.iloc[[lastest_valid_record_index - 1], column_range]

# prepare dataframe for plotting
df_for_barplot = pd.DataFrame()
df_for_barplot['count'] = data_for_barplot.iloc[0].values
df_for_barplot['gender'] = pd.Series( ['female']*7 + ['male']*7 )
df_for_barplot['age'] = pd.Series( ['13-17', '18-24', '24-34', '35-44', '45-54', '55-64', '65+']*2 )

# plot the barplot
fig = plt.figure(figsize=(10, 6))
fig = sns.barplot(x='age', y='count', hue='gender', data=df_for_barplot, palette="muted")

# get record's date
date = retrieved_data.iloc[lastest_valid_record_index - 1]['Date']

# save barplot
plt.savefig('Lifetime Likes by Gender and Age till ' + str(date) + '.jpeg', dpi=600)


# create barplot for Net Likes by Gender and Age

# get data from first record
first_row_of_data = retrieved_data.iloc[[0], column_range]

# append difference column to dataframe above
df_for_barplot['difference'] = data_for_barplot.iloc[0].values - first_row_of_data.iloc[0].values

# plot the barplot
fig = plt.figure(figsize=(10, 6))
fig = sns.barplot(x='age', y='difference', hue='gender', data=df_for_barplot)

# get date difference
date_difference = len(retrieved_data) - 2

# save barplot
plt.savefig('Net Likes by Gender and Age within ' + str(date_difference) + ' Days.jpeg', dpi=600)


# create barplot for Daily Demographics: People Talking About This

# set index of lastest record without value 0
lastest_valid_record_index = len(retrieved_data) - 3

# set index of needed columns
column_range = range(46, 60)

# get data
data_for_barplot = retrieved_data.iloc[[lastest_valid_record_index - 1], column_range]

# prepare dataframe for plotting
df_for_barplot = pd.DataFrame()
df_for_barplot['count'] = data_for_barplot.iloc[0].values
df_for_barplot['gender'] = pd.Series( ['female']*7 + ['male']*7 )
df_for_barplot['age'] = pd.Series( ['13-17', '18-24', '24-34', '35-44', '45-54', '55-64', '65+']*2 )

# plot the barplot
fig = plt.figure(figsize=(10, 6))
fig = sns.barplot(x='age', y='count', hue='gender', data=df_for_barplot, palette="GnBu")

# get record's date
date = retrieved_data.iloc[lastest_valid_record_index - 1]['Date']

# save barplot
plt.savefig('People Talking About This on ' + str(date) + '.jpeg', dpi=600)


# create barplot for Sum of Daily Demographics: People Talking About This

# append sum column to dataframe above
df_for_barplot['sum'] = retrieved_data.iloc[:, column_range].sum().values

# plot the barplot
fig = plt.figure(figsize=(10, 6))
fig = sns.barplot(x='age', y='sum', hue='gender', data=df_for_barplot, palette="BuGn")

# get date difference
date_difference = len(retrieved_data) - 3

# save barplot
plt.savefig('Sum of People Talking About This in ' + str(date_difference) + ' Days.jpeg', dpi=600)


# create catplot for Mean of Daily Frequency Distribution

# set index of needed columns
column_range = range(16, 32)

# prepare dataframe for plotting
df_for_catplot = pd.DataFrame()
df_for_catplot['count'] = retrieved_data.iloc[:, column_range].mean().values
df_for_catplot['type'] = pd.Series( ['page']*8 + ['posts']*8 )
df_for_catplot['frequency'] = pd.Series( ['1', '2', '3', '4', '5', '6-10', '11-20', '21+']*2 )

# plot the catplot
fig = sns.catplot(x='frequency', y='count', col='type', data=df_for_catplot, kind="bar", palette="colorblind")

# get date difference
date_difference = len(retrieved_data) - 1

# save catplot
plt.savefig('Mean of Daily Frequency Distribution in ' + str(date_difference) + ' Days.jpeg', dpi=600)


# interactive visualization section
from IPython.core.interactiveshell import InteractiveShell
import plotly.figure_factory as ff
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.plotly as py

pyo.init_notebook_mode()

InteractiveShell.ast_node_interactivity = 'all'


# these functions are modified from "https://github.com/WillKoehrsen/Data-Analysis/tree/master/medium"

# create cumulative plot for temporal variable
def make_line_plot(df, y, category=None, ranges=False):
    
    # range is manually set when two y variables are given
    manual_range = [df.loc[:, y].values.min()-500, df.loc[:, y].values.max()+500]

    # decide whether a hue column is given
    if category is not None:
        data = []
        for i, (name, group) in enumerate(df.groupby(category)):
            group.sort_values("發佈日期", inplace=True)
            data.append(go.Scatter(x=group["發佈日期"], y=group[y],
                                   mode="lines+markers", text=group["文章標題"], name=name,
                                   marker=dict(size=10, opacity=0.8, symbol=i + 2)))
    
    # decide whether plotting two variables is needed
    else:
        df.sort_values("Date", inplace=True)
        if len(y) == 2:
            data = [go.Scatter(x=df["Date"], y=df[y[0]],
                               mode="lines+markers", text=df["Date"], name=y[0].title(),
                               marker=dict(size=10, color='blue', opacity=0.6, line=dict(color='black'))),
                    
                    go.Scatter(x=df["Date"], y=df[y[1]], yaxis='y2',
                               mode="lines+markers", text=df["Date"], name=y[1].title(),
                               marker=dict(size=10, color='red', opacity=0.6, line=dict(color='black')))]
        else:
            data = [go.Scatter(x=df["Date"], y=df[y],
                               mode="lines+markers", text=df["Date"],
                               marker=dict(size=12, color='blue', opacity=0.6, line=dict(color='black')))]
    
    # construct layout of the plot
    if len(y) == 2:
        layout = go.Layout(xaxis=dict(title="Date", type="date"),
                           yaxis=dict(range=manual_range, title=y[0].replace('_', ' ').title(), color='blue'),
                           yaxis2=dict(range=manual_range, title=y[1].replace('_', ' ').title(), color='red', overlaying='y', side='right'),
                           font=dict(size=14), showlegend=False,
                           title=f"Trend of {y[0].title()} and {y[1].title()}")
    else:
        layout = go.Layout(xaxis=dict(title="Date", type="date"),
                           yaxis=dict(title=y.replace('_', ' ').title()),
                           font=dict(size=14),
                           title=f"Trend of {y.replace('_', ' ').title()} by {category.replace('_', ' ').title()}"
                           if category is not None
                           else f"Trend of {y.replace('_', ' ').title()}")
    
    # add a range-selector and range-slider
    if ranges:
        rangeselector = dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        )
        rangeslider = dict(visible=True)
        layout["xaxis"]["rangeselector"] = rangeselector
        layout["xaxis"]["rangeslider"] = rangeslider
        layout['width'] = 900
        layout['height'] = 600

    # plot cumulative plot
    figure = go.Figure(data=data, layout=layout)
    
    return figure
    

figure = make_line_plot(retrieved_data, y='Lifetime Total Likes', ranges=True)
iplot(figure)


figure = make_line_plot(retrieved_data, y=['Daily Reach Of Page Posts', 'Daily Page Engaged Users'], ranges=True)
iplot(figure)


figure = make_line_plot(retrieved_data, y=['Daily Total Impressions of your posts', 'Daily Page Engaged Users'], ranges=True)
iplot(figure)


figure = make_line_plot(retrieved_data, y=['Daily Total Impressions of your posts', 'Daily Reach Of Page Posts'], ranges=True)
iplot(figure)
