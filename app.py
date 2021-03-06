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

# Constants
LOGO_IMAGE = "./images/logo_1.png"
# Settings
# sns.set_theme(style="lightgrid")


##########   APP   ##########
# Sidebar
page_selection = st.sidebar.radio("Navigation",["Home","Making Predictions", "Past Performance"])


# Page Selection
if page_selection == "Home":
    header = st.container()
    about = st.container()

    with header:
        st.markdown(
            "<h1 style='text-align: center; color: black; font-size: 5rem; font-weight: 600'>Cryptoview</h1>",
            unsafe_allow_html=True)
        col1, col2, col3 = st.columns([0.35, 0.3, 0.35])
        with col2:
            image = Image.open(LOGO_IMAGE)
            st.image(image)
        st.markdown("")

    with about:
        st.markdown(
            "<h2 style='text-align: center; color: black; font-weight: normal'>A platform to predict crypto prices in advance and test trading strategies.</h2>",
            unsafe_allow_html=True)

        st.markdown("")

elif page_selection == "Making Predictions":
    title = st.container()
    plot = st.container()
    output1 = st.container()
    output2 = st.container()

    with title:
        st.markdown("""# Making Predictions""")
        st.markdown("")
        st.markdown("""### Ethereum prices this week (USD)""")

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
