from django.http import request
from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime,timedelta
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format

def index(request):
    return render(request, 'index.html') 

def return_page(request):
    return render(request, 'demo-plot.html') 

#prediction ETH

def get_prediction(request):
    plot_div = None
    if request.method == 'POST':
        moedas = request.POST.get('moedas')
        today = datetime.today().strftime('%Y-%m-%d')
        next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = '2016-01-01'
        eth_df = yf.download(moedas,start_date, today)
        eth_df.reset_index(inplace=True)
        df = eth_df[["Date", "Open"]]
        new_names = {"Date": "ds", "Open": "y",}
        df.rename(columns=new_names, inplace=True)
        m = Prophet(seasonality_mode="multiplicative")
        m.fit(df)

        future = m.make_future_dataframe(periods = 365)

        forecast = m.predict(future)
        trace = go.Scatter(
        name = 'Preço Atual',
        mode = 'markers',
        x = list(df['ds']),
        y = list(df['y']),
        marker=dict(
            color='black',
            line=dict(width=1)
            )
        )

        trace1 = go.Scatter(
            name = 'Previsão',
            mode = 'lines',
            x = list(forecast['ds']),
            y = list(forecast['yhat']),
            marker=dict(
                color='red',
                line=dict(width=3)
            )
        )
        data = [trace, trace1]

        layout = dict(title=f'Previsão de preço {moedas.upper()}',
                    xaxis=dict(title = 'Datas', ticklen=2, zeroline=True))

        figure=dict(data=data,layout=layout)

        plot_div = plot(figure,output_type='div', include_plotlyjs=False)
        
    
    return render(request, 'prediction.html', 
                  context={'plot_div': plot_div})
