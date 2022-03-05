##########   SETUP   ##########
# Imports
import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
from get_data import get_weekly_eth_data, get_current_price, get_day_interval
from cryptoapi import get_prediction, get_backtest
import streamlit.components.v1 as components
import datetime
import csv
from datetime import timedelta
import requests

st.set_page_config(
    page_title="709 CryptoView", # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

#Getting the updated Ethereum Value
url = 'https://api.coinbase.com/v2/prices/ETH-USD/spot'
response = requests.get(url)
eth_value_now = float(response.json()['data']['amount'])

# Constants
LOGO_IMAGE = "./images/logo_1.png"
IMAGE = "./images/2.png"
IMAGE1 = "./images/5.png"
IMAGE2 = "./images/3.webp"
# Settings
# sns.set_theme(style="lightgrid")


##########   APP   ##########
# Sidebar
page_selection = st.sidebar.radio("Navigation",["Home","Making Predictions", "Past Performance", "Your Investments"])


# Page Selection
if page_selection == "Home":
    header = st.container()
    about = st.container()  

    with header:
        col1, col2, col3= st.columns([1, 2, 7])
        with col2:
            # st.markdown("<img src='/images/logo_1.png'>" , unsafe_allow_html=True)
            image = Image.open(LOGO_IMAGE)
            st.image(image, width=150)
        with col3:
             st.markdown("<h1 style='text-align: left; color: black; font-size: 5rem; font-weight: 600'>Cryptoview</h1>",
            unsafe_allow_html=True)
        st.markdown("")

    with about:
        st.markdown(
            "<h2 style='text-align: center; color: black; font-weight: normal'>A platform to predict crypto prices in advance and test trading strategies.</h2>",
            unsafe_allow_html=True)

        st.markdown("")
        image = Image.open(IMAGE)
        st.image(image)
        # image1 = Image.open(IMAGE1)
        # st.image(image1)
        image2 = Image.open(IMAGE2)
        st.image(image2)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: left; color: black;'>The 709 CryptoView Trading App</h3>",
            unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: left; color: black;'>Don't leave your investment up to chance. Here, we'll:</p>",
            unsafe_allow_html=True)
        st.markdown(
            "<ul>\
                <li>Help take calculated decision based on historical data and sentiment analysis:\
                <li>Keep track of all your investments and how they're doing over time\
            </ul>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

elif page_selection == "Making Predictions":
    title = st.container()
    plot = st.container()
    output1 = st.container()
    output2 = st.container()

    with title:
        st.markdown("""# Making Predictions""")
        st.markdown("")
        st.markdown("<h3 style='text-align: left'>Ethereum prices this week (USD)</h3>", unsafe_allow_html=True) 

    with plot:
        prediction_form = st.form(key="prediction_form")

        with prediction_form:
            # plot update plot to show prediction
            submitted = st.form_submit_button("Predict")
            # get weekly ethereum data
            df = get_weekly_eth_data()

            if submitted:
                # make prediction
                prediction = 100 * get_prediction()
                current_price = get_current_price()
                expected_price = round(
                    ((prediction + 100) / 100) * current_price)

                fig = px.line(df,
                              x='datetime',
                              y=['eth_price_usd'],
                              color_discrete_map={"eth_price_usd": "#4e79a7"})
                if prediction > 0:
                    fig.add_traces(
                        list(
                            px.line(x=get_day_interval(),
                                    y=[current_price, expected_price],
                                    color_discrete_sequence=['#38d93e'],
                                    line_dash_sequence=['dash']).select_traces()))
                elif prediction < 0:
                    fig.add_traces(
                        list(
                            px.line(x=get_day_interval(),
                                    y=[current_price, expected_price],
                                    color_discrete_sequence=['#e63939'],
                                    line_dash_sequence=['dash'
                                                        ]).select_traces()))
                else:
                    fig.add_traces(
                        list(
                            px.line(x=get_day_interval(),
                                    y=[current_price, expected_price],
                                    color_discrete_sequence=['blue'],
                                    line_dash_sequence=['dash'
                                                        ]).select_traces()))

                fig.update_xaxes(visible=True)
                fig.update_layout(legend=dict(
                    yanchor="bottom", y=-0.3, xanchor="left", x=0.80))
                st.plotly_chart(fig, use_container_width=True)

                # plot current ethereum price
                with output1:
                    st.info(
                        f'The current Ethereum price is **${current_price}** (USD)'
                    )

                if prediction > 0:
                    with output2:
                        st.success(
                            f'Ethereum price is expected to be **${round(((prediction + 100)/100)*current_price)}** tomorrow, an increase of **{round(prediction,2)}%**.'
                        )
                elif prediction < 0:
                    with output2:
                        st.error(
                            f'Ethereum price is expected to be **${round(((prediction + 100)/100)*current_price)}** tomorrow, a decrease of **{round(prediction,2)}%**.'
                        )
                else:
                    with output2:
                        st.info(
                            'Ethereum price is expected to remain stable tomorrow.'
                        )

            else:
                fig = px.line(df,
                            x='datetime',
                            y=['eth_price_usd'],
                            color_discrete_map={
                                "eth_price_usd": "#4e79a7"
                            })

                fig.update_xaxes(visible=True)
                fig.update_layout(
                    legend=dict(yanchor="bottom",
                                y=-0.3, xanchor="left",
                                x=0.80))
                st.plotly_chart(fig, use_container_width=True)

                # get current ethereum price
                current_price = get_current_price()
                # plot current ethereum price
                with output1:
                    st.info(
                        f'The current Ethereum price is **${current_price}** (USD)')



elif page_selection == "Past Performance":
    title = st.container()
    plot = st.container()
    output = st.container()

    with title:
        st.markdown("""# Past Performance""")
        st.markdown("")

    with plot:
        input_form = st.form(key="input_form")
        with input_form:
            amount = st.number_input('Enter an amount (USD)', 0, 1000000)
            deposit_date = st.date_input('Deposit date')
            trading_strategy = st.selectbox('Trading Strategy',
                                  ('Buy and Hold', 'Cryptoview Algorithm'))
            st.markdown("")
            see_performance = st.form_submit_button("See Performance")

            if see_performance == True and trading_strategy == 'Buy and Hold':
                backtest_data = get_backtest(amount, deposit_date)
                fig = px.line(backtest_data,
                              x='date',
                              y=['buy-and-hold'],
                              color_discrete_map={
                                  "buy-and-hold": "#4e79a7"
                              })
                fig.update_xaxes(visible=True,
                    rangeselector=dict(buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])))
                fig.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="left",
                    x=0.80
                ))
                st.plotly_chart(fig, use_container_width=True)

                # get final values for both time series
                bah_final_amount = int(backtest_data.iloc[-1, :]['buy-and-hold'])
                # get % difference = strat / bah
                pct_diff_bah = round(((bah_final_amount-amount)/amount)*100, 1)

                if pct_diff_bah > 0:
                    with output:
                        st.success(
                            f'If you made this investment, you would now have **${bah_final_amount}**, an increase of **{pct_diff_bah}%**'
                        )
                elif pct_diff_bah < 0:
                    with output:
                        st.error(
                            f'If you made this investment, you would now have **${bah_final_amount}**, a decrease of **{pct_diff_bah}%**'
                        )
                else:
                    with output:
                        st.info(
                            'No change.'
                        )

            if see_performance == True and trading_strategy == 'Cryptoview Algorithm':
                backtest_data = get_backtest(amount, deposit_date)
                fig = px.line(backtest_data,
                              x='date',
                              y=['buy-and-hold', 'strategy'],
                              color_discrete_map={
                                  "buy-and-hold": "#4e79a7",
                                  "strategy": "#f28e2b"
                              })
                fig.update_xaxes(visible=True,
                    rangeselector=dict(buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])))
                fig.update_layout(legend=dict(
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="left",
                    x=0.80
                ))
                st.plotly_chart(fig, use_container_width=True)

                # get final values for both time series
                bah_final_amount = backtest_data.iloc[-1, :]['buy-and-hold']
                strategy_final_amount = backtest_data.iloc[-1, :]['strategy']
                # get % difference = strat / bah
                pct_diff = int(100 * (strategy_final_amount / bah_final_amount))

                if pct_diff > 0:
                    with output:
                        st.success(
                            f'Using the Cryptoview algorithm, you would now have **${int(strategy_final_amount)}**, beating the market by **{round(pct_diff/100, 1)}** times!'
                        )
                        st.balloons()
                elif pct_diff < 0:
                    with output:
                        st.error(
                            f'Using the Cryptoview algorithm, you would now have **${int(strategy_final_amount)}**, losing to the market by **{round(pct_diff/100, 1)}** times.'
                        )
                else:
                    with output:
                        st.info(
                            'No change.'
                        )
            # TABLE

elif page_selection == "Your Investments":
    title = st.container()

    with title:
        st.markdown("<h1 style='text-align: left'>Your Investments</h1>", unsafe_allow_html=True) 
        st.markdown("")

    ##############################Start of Ethereum Graph################################

    # with st.container():
    #     df = pd.read_csv('etheureum_data.csv')
    #     fig = px.line(df[0:500000], x='date', y=['close'])
    #     fig.update_xaxes(visible=True,
    #         rangeselector=dict(buttons=list([
    #             dict(count=1, label="1m", step="month", stepmode="backward"),
    #             dict(count=6, label="6m", step="month", stepmode="backward"),
    #             dict(count=1, label="YTD", step="year", stepmode="todate"),
    #             dict(count=1, label="1y", step="year", stepmode="backward"),
    #             dict(step="all")
    #         ])))
    #     # fig.update_layout(legend=dict(
    #     #     yanchor="bottom",
    #     #     y=-0.3,
    #     #     xanchor="left",
    #     #     x=0.80
    #     # ))
    #     st.plotly_chart(fig, use_container_width=True)
        
        list1 = []
        with open('investments_log.csv') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                time = datetime.datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
                trans_type = row['trans_type']
                investment = int(row['investment'])
                h1 = int(row['12h'])
                h12 = int(row['24h'])
                h18 = int(row['48h'])
                h24 = int(row['now'])
                list1.append([time, trans_type, investment, h1, h12, h18, h24])
        
###############################End of Ethereum Graph################################

###############################Start of Input Form################################

    # list1 = []
    # with open('investments_log.csv') as csvfile:
    #     reader = csv.DictReader(csvfile, skipinitialspace=True)
    #     for row in reader:
    #         time = datetime.datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
    #         trans_type = row['trans_type']
    #         investment = int(row['investment'])
    #         h1 = int(row['12h'])
    #         h12 = int(row['24h'])
    #         h18 = int(row['48h'])
    #         h24 = int(row['now'])
    #         list1.append([time, trans_type, investment, h1, h12, h18, h24])

    # with st.form("my_form"):
        
    #     # st.write("Inside the form")
    #     # slider_val = st.slider("Form slider")
    #     # checkbox_val = st.checkbox("Form checkbox")
    #     buy_sell_col, investment_col, time_col = st.columns((1,1,1))
        
    #     with buy_sell_col: 
    #         buy_sell = st.selectbox('BUY or SELL?',
    #         ('BUY', 'SELL'))

    #     with investment_col:
    #         investment = st.text_input(label = 'How much (in USD)?', value="0", max_chars=10, placeholder=500)
    #         # components.html("<input name="investment" id="inv" value="" required>")
    #     with time_col:
    #         time = st.time_input(label="When do you want to buy?", value=None)
    #         time_now = datetime.datetime.now()
    #         x = time_now.strftime("%Y-%m-%d %H:%M:%S")
    #         time_now = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

    #     # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")
    #     if submitted:
    #         # st.write("You invested", investment, "$ at", time)
    #         inv = int(investment)
    #         list1.insert(0, [time_now, buy_sell, inv, inv, inv, inv, inv])
        
    #         df1 = pd.DataFrame(
    #             list1,
    #             columns = ['time', 'trans_type', 'investment', '12h', '24h', '48h', 'now']) 
    #             # total_eth_usd, sold_eth, total_inv (annual interest rate of 5%)
    #         # st.dataframe(df1)
    #         df1.to_csv('investments_log.csv', index=False, header=True)
            
###############################End of Input Form################################

##########################Get Datao####################################################################

    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("<h3 style='text-align: left'>Crypto Trading Vs 5% Annual Return:</h3>", unsafe_allow_html=True) 

    data = pd.read_csv('etheureum_data.csv')
    data1 = pd.read_csv('investments_log.csv')

    #Doing a match search, so need to standardize time units to Y-M-D-H-M-S where seconds=00
    data.date = data.date.astype('datetime64')
    data1.time = data1.time.astype('datetime64')
    data1['time'] = data1.time.apply(lambda x: x.strftime("%Y-%m-%d-%H:%M:00"))
    data1.time = data1.time.astype('datetime64')
    # data1.time = pd.to_datetime(data1.time, format='%Y-%m-%d %H:%M:00') #Round to minutes...
    # data.set_index('date', inplace=True)
    # data1.set_index('time', inplace=True)
    df = data.copy()
    df1 = data1.copy()

##########################Get Investment Portfolio####################################################################

    # data_i = pd.read_csv('investments_log.csv')
    # data_i.time = data_i.time.astype('datetime64')
    # data_i['time'] = data_i.time.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:00"))
    # data_i.time = data_i.time.astype('datetime64')
    # inv_df = data_i.sort_values('time', ascending=True)
    # inv_df = inv_df.reset_index()
    # del inv_df['index']

    # eth_data = pd.read_csv('etheureum_data.csv')
    # eth_data.date = data.date.astype('datetime64')
    # df_eth = eth_data.sort_values('date', ascending=True)
    # df_eth = df_eth.reset_index()
    # del df_eth['index']

    # # df3 = pd.DataFrame(None, columns = ['date', 'eth_value', 'change', 'new_invest_value', 'sold_coins_value', 'eth return', '5 % return'])

    # first_trans_date = inv_df.iloc[0].time
    # trans_index_n = df_eth[df_eth.date == first_trans_date].index.values[0]
    # next_trans_date = ''

    # n_value = df_eth.loc[trans_index_n].close
    # invest_value = inv_df.iloc[0].investment
    # sold_coins_value = 0
    # updated_investment_value = 0
    # investment_values = []
    # len_inv_df = len(inv_df)

    # total_invested = invest_value

    # investment_values.append({'date' : first_trans_date, 'eth_value': n_value, 'change' : 0, 'new_invest_value' : invest_value, 'sold_coins_value': sold_coins_value, 'eth return': invest_value + sold_coins_value, '5 % return': invest_value})


    # for i, row in inv_df.iterrows():
    #     if i > 0:
    #         trans_date = row.time
    #         trans_index_n_1 = df_eth[df_eth.date == trans_date].index.values[0]
            
    #         transaction_type = row.trans_type
            
    #         for y, row_eth in df_eth.loc[trans_index_n + 1:trans_index_n_1].iterrows():
    #             date = row_eth['date']
    #             n_1_value = row_eth['close']
    #             change = (n_1_value - n_value) / n_value
    #             if y == trans_index_n_1: 
    #                 if row.trans_type == 'BUY':
    #                     invest_value += row.investment 
    #                 else:
    #                     invest_value -= row.investment
    #                 if row.trans_type == 'BUY':
    #                     total_invested += row.investment 
    #                 else:
    #                     total_invested -= row.investment
    #                 sold_coins_value += row.investment if row.trans_type == 'SELL' else 0
    #             updated_investment_value = invest_value * (1+change)
    # #             total = updated_investment_value + sold_coins_value
    #             total_invested = total_invested * 1.0000001
    #             sold_coins_value = sold_coins_value * 1.0000001
    #             investment_values.append({'date': date, 'eth_value' : n_1_value, 'change': change, 'new_invest_value': updated_investment_value, 'sold_coins_value' : sold_coins_value, 'eth return': updated_investment_value + sold_coins_value, '5 % return': (total_invested + sold_coins_value)})
    #         n_value = n_1_value
            
    #         trans_index_n = trans_index_n_1
    #         invest_value = updated_investment_value
            
    # df4 = pd.DataFrame.from_dict(investment_values, orient='columns')

    # df_portfolio_daily = df4.resample('D', on='date').last()

    # with st.container():
    # fig = px.line(df_portfolio_daily, x='date', y=['eth return', '5 % return'])
    # fig.update_xaxes(visible=True,
    #     rangeselector=dict(buttons=list([
    #         dict(count=1, label="1m", step="month", stepmode="backward"),
    #         dict(count=6, label="6m", step="month", stepmode="backward"),
    #         dict(count=1, label="YTD", step="year", stepmode="todate"),
    #         dict(count=1, label="1y", step="year", stepmode="backward"),
    #         dict(step="all")
    #     ])))
    # fig.update_layout(legend=dict(
    #     yanchor="bottom",
    #     y=-0.3,
    #     xanchor="left",
    #     x=0.80
    # ))
    # st.plotly_chart(fig, use_container_width=True)

    

    #########################End of Get Investment Portfolio####################################################################

    #########################Ethereum Graph####################################################################
    
    df10 = pd.read_csv('investment_graph.csv')

    with st.container():
        fig = px.line(df10, x='date', y=['eth return', '5 percent return'])
        fig.update_xaxes(visible=True,
            rangeselector=dict(buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])))
        fig.update_layout(legend=dict(
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.80
        ))
        st.plotly_chart(fig, use_container_width=True)

##########################Ethereum Graph####################################################################

##########################Start of Investment Portfolio####################################################################

    st.markdown("<h3 style='text-align: left'>Past Transactions:</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True) 

    def get_updated_values(trans_date):

        trans_date = trans_date
        trans_date_12h = trans_date + timedelta(hours=12)
        trans_date_24h = trans_date + timedelta(hours=24)
        trans_date_48h = trans_date + timedelta(hours=48)
        # data now is taking a value from the previous day (as the API doesn't get called all the time)
        date_now = trans_date + timedelta(hours=(datetime.datetime.now() - trans_date).days * 24 - 48 + divmod((datetime.datetime.now() - trans_date).seconds, 3600)[0]) 

        data_row_value = df[df.date == trans_date].index    
        data_row_value_12h = df[df.date == trans_date_12h].index
        data_row_value_24h = df[df.date == trans_date_24h].index
        data_row_value_48h = df[df.date == trans_date_48h].index
        data_row_value_now = df[df.date == date_now].index

        value = df.loc[data_row_value]['close'].values[0] if len(data_row_value)!= 0 else 0
        value_12h = df.loc[data_row_value_12h]['close'].values[0] if len(data_row_value_12h)!= 0 else 0
        value_24h = df.loc[data_row_value_24h]['close'].values[0] if len(data_row_value_24h)!= 0 else 0
        value_48h = df.loc[data_row_value_48h]['close'].values[0] if len(data_row_value_48h)!= 0 else 0
        
        # st.write(eth_value_now)   
        # st.write(value)
        change_12h = 1 + (value_12h - value) / value if value != 0 else 0
        change_24h = 1 + (value_24h - value) / value if value != 0 else 0
        change_48h = 1 + (value_48h - value) / value if value != 0 else 0
        change_now = 1 + (eth_value_now - value) / value if value != 0 else 0
        return {'12h' : change_12h, '24h' : change_24h, '48h' : change_48h, 'now' : change_now}
        #end of get_updated values method

    for i, row in df1.iterrows():
        results = get_updated_values(row['time'])
        # st.write(results)
    #     row['12h'] = results['12h'] * row['12h']
        df1.loc[i, '12h'] = results['12h'] * row['investment'] if results['12h'] != 0 else row['investment']
    #     row['24h'] = results['24h'] * row['24h']
        df1.loc[i, '24h'] = results['24h'] * row['investment'] if results['24h'] != 0 else row['investment']
    #     row['48h'] = results['48h'] * row['48h']
        df1.loc[i, '48h'] = results['48h'] * row['investment'] if results['48h'] != 0 else row['investment']
    #     row['now'] = results['now'] * row['now']
        df1.loc[i, 'now'] = results['now'] * row['investment'] if results['now'] != 0 else row['investment']
    
    # new csv with 3 columns: date & time | investment value | sold items...

    # take total investment
    # get the % change for each minute
    # update total investment for each time and updated investment
    # If something has been sold, update the sold section...

    # total of all the time of the investment and see how much it is changing at all times

    #Making the Date format prettier
    def date_format(date):
        return date.strftime("%d %b %Y%H:%M:00")
    df1.time = df1.time.apply(lambda x : date_format(x))

    df2 = df1.copy()
    
    
    df = pd.DataFrame(
        list1,
        columns = ['time', 'trans_type', 'investment', '12h', '24h', '48h', 'now'])

    def select_col(x):
        c0 = 'background-color: grey'
        # c00 = 'background-color: yellow; color:black'
        # c01 = 'background-color: black; color:yellow'
        c1 = 'background-color: #88CA5E' 
        c2 = 'background-color: #D2FBA4' #light green
        c3 = 'background-color: #EB7E75' #dark red
        c4 = 'background-color: #F7BEC0' #light red
        c5 = ''
        #compare columns
        df1 =  pd.DataFrame(c5, index=x.index, columns=x.columns)
        for col_name in x.columns:
            if col_name != 'investment' and col_name != 'time' and col_name != 'trans_type':
                mask0 = x[col_name] == x['investment']
                mask1 = (x[col_name] > x['investment']) & (x.trans_type == 'BUY')
                mask2 = (x[col_name] > x['investment'] * 1.1) & (x.trans_type == 'BUY')
                mask3 = (x[col_name] < x['investment']) & (x.trans_type == 'BUY')
                mask4 = (x[col_name] < x['investment'] * 0.9) & (x.trans_type == 'BUY')
                mask5 = (x[col_name] > x['investment']) & (x.trans_type == 'SELL')
                mask6 = (x[col_name] > x['investment'] * 1.1) & (x.trans_type == 'SELL')
                mask7 = (x[col_name] < x['investment']) & (x.trans_type == 'SELL')
                mask8 = (x[col_name] < x['investment'] * 0.9) & (x.trans_type == 'SELL')
                df1.loc[mask0, col_name] = c0
                df1.loc[mask1, col_name] = c1
                df1.loc[mask2, col_name] = c2
                df1.loc[mask3, col_name] = c3
                df1.loc[mask4, col_name] = c4
                df1.loc[mask5, col_name] = c4
                df1.loc[mask6, col_name] = c3
                df1.loc[mask7, col_name] = c2
                df1.loc[mask8, col_name] = c1
            # elif col_name != 'investment':
                # mask10 = (x.trans_type == 'buy')
                # mask11 = (x.trans_type == 'sell')
                # df1.loc[mask10, 'trans_type'] = c01
                # df1.loc[mask11, 'trans_type'] = c00
        return df1

    df2 = df2.style.apply(select_col, axis=None)

    st.dataframe(df2)

##########################End of Investment Portfolio####################################################################

###############################################

    # with title:
    #     st.markdown("""# Past Performance""")
    #     st.markdown("")

    # with plot:
    #     input_form = st.form(key="input_form")
    #     with input_form:
    #         st.number_input('Amount (USD)', 0, 1000000)
    #         st.date_input('Deposit Date')
    #         st.markdown("")

    #         check_performance = st.form_submit_button("Check Performance")

    #         if check_performance == True:
    #             df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    #             fig = px.line(df, x='Date', y=['AAPL.High', 'AAPL.Low'])
    #             fig.update_xaxes(visible=True,
    #                 rangeselector=dict(buttons=list([
    #                     dict(count=1, label="1m", step="month", stepmode="backward"),
    #                     dict(count=6, label="6m", step="month", stepmode="backward"),
    #                     dict(count=1, label="YTD", step="year", stepmode="todate"),
    #                     dict(count=1, label="1y", step="year", stepmode="backward"),
    #                     dict(step="all")
    #                 ])))
    #             fig.update_layout(legend=dict(
    #                 yanchor="bottom",
    #                 y=-0.3,
    #                 xanchor="left",
    #                 x=0.80
    #             ))
    #             st.plotly_chart(fig, use_container_width=True)
    #         else:
    #             df = pd.read_csv(
    #                 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
    #             )
    #             fig = px.line(df, x='Date', y=['AAPL.High'])
    #             fig.update_xaxes(visible=True,
    #                              rangeselector=dict(buttons=list([
    #                                  dict(count=1,
    #                                       label="1m",
    #                                       step="month",
    #                                       stepmode="backward"),
    #                                  dict(count=6,
    #                                       label="6m",
    #                                       step="month",
    #                                       stepmode="backward"),
    #                                  dict(count=1,
    #                                       label="YTD",
    #                                       step="year",
    #                                       stepmode="todate"),
    #                                  dict(count=1,
    #                                       label="1y",
    #                                       step="year",
    #                                       stepmode="backward"),
    #                                  dict(step="all")
    #                              ])))
    #             fig.update_layout(legend=dict(
    #                 yanchor="bottom", y=-0.3, xanchor="left", x=0.80))
    #             st.plotly_chart(fig, use_container_width=True)


    #         # dummy code for demonstration purposes


    #     # plot update plot to show prediction
    #     # if submitted:
    #     # make prediction
    #     #   prediction = ...
    #     # update plot with new prediction
    #     #       if prediction > 0 then plot in green
    #     #       if prediction < 0 then plot in red


    # with output:
    #     # output message based on prediction
    #     # if prediction > 0:
    #     #     st.success('Ethereum is expected to increase by ... in the next hour.')
    #     #     st.balloons()
    #     # elif prediction < 0:
    #     #     st.error('Ethereum is expected to decrease by ... in the next hour.')
    #     # else:
    #     #     st.info('Ethereum is expected to remain stable in the next hour.')
    #     st.success('By investing with CryptoBot, you earnt an extra **$2780!**')
    #     st.balloons()
