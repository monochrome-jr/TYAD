from IPython.core.interactiveshell import InteractiveShell
import plotly.figure_factory as ff
from plotly.offline import iplot
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from matplotlib import pyplot
import plotly.offline as pyo
import plotly.plotly as py
import matplotlib as mpl
import pandas as pd
import numpy as np
import os

pyo.init_notebook_mode()

%load_ext autoreload
%autoreload 2

plt.rcParams['font.family']='SimHei'

pd.set_option('max_rows', 200)
pd.set_option('max_columns', 50)

InteractiveShell.ast_node_interactivity = 'all'


# these functions are modified from "https://github.com/WillKoehrsen/Data-Analysis/tree/master/medium"

# create histogram to show distribution of given variable
def make_hist(df, x, category=None):

    # decide whether a hue column is given
    if category is not None:
        data = []
        for name, group in df.groupby(category):
            data.append(go.Histogram(dict(x=group[x], name=name)))
    
    # if not, just plot an normal histogram
    else:
        data = [go.Histogram(dict(x=df[x]))]

    # construct layout of the plot
    layout = go.Layout(yaxis = dict(title="Count"), xaxis = dict(title=x.replace('_', ' ').title()))
    
    # plot histogram
    figure = go.Figure(data=data, layout=layout)
    
    return figure


# create cumulative plot for temporal variable
def make_cum_plot(df, y, category=None, ranges=False):

    # decide whether a hue column is given
    if category is not None:
        data = []
        for i, (name, group) in enumerate(df.groupby(category)):
            group.sort_values("發佈日期", inplace=True)
            data.append(go.Scatter(x=group["發佈日期"], y=group[y].cumsum(),
                                   mode="lines+markers", text=group["文章標題"], name=name,
                                   marker=dict(size=10, opacity=0.8, symbol=i + 2)))
    
    # decide whether plotting two variables is needed
    else:
        df.sort_values("發佈日期", inplace=True)
        if len(y) == 2:
            data = [go.Scatter(x=df["發佈日期"], y=df[y[0]].cumsum(),
                               mode="lines+markers", text=df["文章標題"], name=y[0].title(),
                               marker=dict(size=10, color='blue', opacity=0.6, line=dict(color='black'))),
                    
                    go.Scatter(x=df["發佈日期"], y=df[y[1]].cumsum(), yaxis='y2',
                               mode="lines+markers", text=df["文章標題"], name=y[1].title(),
                               marker=dict(size=10, color='red', opacity=0.6, line=dict(color='black')))]
        else:
            data = [go.Scatter(x=df["發佈日期"], y=df[y].cumsum(),
                               mode="lines+markers", text=df["文章標題"],
                               marker=dict(size=12, color='blue', opacity=0.6, line=dict(color='black')))]
    
    # construct layout of the plot
    if len(y) == 2:
        layout = go.Layout(xaxis=dict(title="發佈日期", type="date"),
                           yaxis=dict(title=y[0].replace('_', ' ').title(), color='blue'),
                           yaxis2=dict(title=y[1].replace('_', ' ').title(), color='red', overlaying='y', side='right'),
                           font=dict(size=14),
                           title=f"Cumulative {y[0].title()} and {y[1].title()}")
    else:
        layout = go.Layout(xaxis=dict(title="發佈日期", type="date"),
                           yaxis=dict(title=y.replace('_', ' ').title()),
                           font=dict(size=14),
                           title=f"Cumulative {y.replace('_', ' ').title()} by {category.replace('_', ' ').title()}"
                           if category is not None
                           else f"Cumulative {y.replace('_', ' ').title()}")
    
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
        layout['width'] = 1000
        layout['height'] = 600

    # plot cumulative plot
    figure = go.Figure(data=data, layout=layout)
    
    return figure


# create scatter plot
def make_scatter_plot(df, x, y, fits=None, xlog=False, ylog=False, category=None, scale=None, sizeref=2, annotations=None, ranges=False, title_override=None):

    # decide whether a hue column is given
    if category is not None:
        title = f"{y.replace('_', ' ').title()} vs {x.replace('_', ' ').title()} by {category.replace('_', ' ').title()}"
        data = []
        for i, (name, group) in enumerate(df.groupby(category)):
            data.append(go.Scatter(x=group[x], y=group[y],
                                   mode='markers', text=group['文章標題'], name=name,
                                   marker=dict(size=8, symbol=i + 2)))

    # decide whether a scale column is given
    else:
        if scale is not None:
            title = f"{y.replace('_', ' ').title()} vs {x.replace('_', ' ').title()} Scaled by {scale.title()}"
            data = [go.Scatter(x=df[x], y=df[y],
                               mode='markers', text=df['文章標題'], 
                               marker=dict(size=df[scale],line=dict(color='black', width=0.5), 
                                           sizemode='area', sizeref=sizeref, opacity=0.8,
                                           colorscale='Viridis', color=df[scale],
                                           showscale=True, sizemin=2))]
        else:
            df.sort_values(x, inplace=True)
            title = f"{y.replace('_', ' ').title()} vs {x.replace('_', ' ').title()}"
            data = [go.Scatter(x=df[x], y=df[y],
                               mode='markers', text=df['文章標題'], 
                               marker=dict(size=12, color='blue', opacity=0.8, 
                                           line=dict(color='black')),
                               name='observations')]
            if fits is not None:
                for fit in fits:
                    data.append(go.Scatter(x=df[x], y=df[fit], text=df['文章標題'],
                                           mode='lines+markers', 
                                           marker=dict(size=8, opacity=0.6),line=dict(dash='dash'), 
                                           name=fit))
                title += ' with Fit'
    
    # construct layout of the plot
    layout = go.Layout(annotations=annotations,
                       xaxis=dict(title=x.replace('_', ' ').title() + (' (log scale)' if xlog else ''), type='log' if xlog else None),
                       yaxis=dict(title=y.replace('_', ' ').title() + (' (log scale)' if ylog else ''), type='log' if ylog else None),
                       font=dict(size=14),
                       title=title if title_override is None else title_override)

    # Add a rangeselector and rangeslider for a data xaxis
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
        layout['width'] = 1000
        layout['height'] = 600

    # plot scatter plot
    figure = go.Figure(data=data, layout=layout)
                           
    return figure
    
    
# create interactive correlation heatmap
corrs = data.corr()
figure = ff.create_annotated_heatmap(z = corrs.round(2).values, 
                                     x = list(corrs.columns), 
                                     y = list(corrs.index), 
                                     colorscale = 'Portland',
                                     annotation_text = corrs.round(2).values)
iplot(figure)


# create interactive scatterplot matrix
figure = ff.create_scatterplotmatrix(data[['拍手數', '瀏覽人數', '閱畢人數', '<tag>三一八學運']],
                                     index = '<tag>三一八學運', colormap='Portland',
                                     diag='histogram', width=800, height=800,
                                     title='')
iplot(figure)


# create interactive histogram
figure = make_hist(data, x='閱畢人數', category='<tag>即時新聞')
iplot(figure)


# create interactive cumulative plot with two variables
figure = make_cum_plot(data, y=['閱畢人數', '拍手數'])
iplot(figure)


# create interactive cumulative plot with range slider
figure = make_cum_plot(data, y='拍手數', category='<tag>專題報導', ranges=True)
iplot(figure)


# create interactive scatter plot
figure = make_scatter_plot(data, x='閱讀文章所需時間', y='閱畢比例', category='<tag>專題報導')
iplot(figure)


# create interactive scatter plot with scalable point
figure = make_scatter_plot(data, x='閱讀文章所需時間', y='瀏覽人數', ylog=True,
                           scale='閱畢比例', sizeref=0.2)
iplot(figure)
