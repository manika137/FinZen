# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:24:52 2022

@author: manika
"""

import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from streamlit_option_menu import option_menu

from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
from io import BytesIO
import base64
import datetime

from nsetools import Nse
nse = Nse()

import streamlit.components.v1 as components
# components.html(
#     """
#        <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div class="tradingview-widget-container__widget"></div>
#   <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/EURUSD/?exchange=FX" rel="noopener" target="_blank"><span class="blue-text">EUR USD rates</span></a> by TradingView</div>
#   <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
#   {
#   "symbol": "FX:EURUSD",
#   "autosize": true,
#   "height" : "100%",
#   "locale": "in",
#   "dateRange": "12M",
#   "colorTheme": "light",
#   "trendLineColor": "rgba(41, 98, 255, 1)",
#   "underLineColor": "rgba(41, 98, 255, 0.3)",
#   "underLineBottomColor": "rgba(41, 98, 255, 0)",
#   "isTransparent": false,
#   "autosize": false,
#   "largeChartUrl": ""
# }
#   </script>
# </div>
# <!-- TradingView Widget END -->""")

# components.html(
#     """
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_a9d26"></div>
#   <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL stock chart</span></a> by TradingView</div>
#   styles={"height": "100vh"}
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "autosize": true,
#   "height" : "100%",
#   "symbol": "NASDAQ:AAPL",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "theme": "light",
#   "style": "1",
#   "locale": "en",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "allow_symbol_change": true,
#   "container_id": "tradingview_a9d26"
# }
#   );
#   </script>
# </div>
# <!-- TradingView Widget END -->""")

with st.sidebar:
        choose = option_menu(menu_title="CitiBulletin", options=["Data", "Charts", "News"],
                             menu_icon="app-indicator", default_index=0,
        #                      styles={
        #                          "menu-title": {"color": "orange"},
        #     "container": {"padding": "5!important", "background-color": "#00000"},
        #     "icon": {"color": "orange", "font-size": "25px"},
        #     "nav-link": {"color": "orange", "background-colour": "red", "font-size": "16px", 
        #                  "text-align": "left", "margin": "0px", "--hover-color": "#fae5df"},
        #     "nav-link-selected": {"background-color": "#fae5df"},
        # }
        )
        
if choose == "Data":    
        st.title('Dashboard')
        # ticker = st.sidebar.text_input('Ticker')
        
        
        #data = yf.download(ticker, start=start_date,end=end_date)
        # data
        # y_axis = data['Adj Close']
        # fig=px.line(data, x= data['Adj Close'], y= data['Adj Close'], title = ticker)
        # st.plotly_chart(fig)
        
        
        all_stock_codes = nse.get_stock_codes()
        res = [key for key in all_stock_codes]
        # res = list(all_stock_codes.values())
        stock_name = st.selectbox('SEARCH FOR NSE STOCK', res)
        
        start_date = st.date_input('Start Date')
        end_date = st.date_input('End Date')
        
        if st.button('Search'):
        
            pricing_data, fundamental_data = st.tabs(["Pricing data", "Fundamental Data"])
            
            with pricing_data:
                st.header('Price Movements')
                
                q = nse.get_quote(stock_name)
                dff= pd.DataFrame([q])
                dff
                # dff = pd.DataFrame.from_dict(q)
                # dff
                
                # data2=data
                # data2['%Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                # data2.dropna(inplace = True)
                # st.write(data2)
                # annual_return = data2["%Change"].mean()*252*100
                # st.write('Annual Return is', annual_return, '%')
                # stdev = np.std(data2['%Change'])*np.sqrt(252)
                # st.write('Standard Deviation is', stdev*100, '%')
            
            from alpha_vantage.fundamentaldata import FundamentalData
            with fundamental_data:
                key = 'OZTB2UTTJMFNA8UU'
                fd = FundamentalData(key, output_format = 'pandas')
                st.subheader('Balance Sheet')
                balance_sheet = fd.get_balance_sheet_annual(stock_name)[0]
                bs = balance_sheet.T[2:]
                bs.columns = list(balance_sheet.T.iloc[0])
                st.write(bs)
                st.subheader('Income Statement')
                income_statement = fd.get_income_statement_annual(stock_name)[0]
                is1 = income_statement.T[2:]
                is1.columns = list(income_statement.T.iloc[0])
                st.write(is1)
                st.subheader('Cash Flow Statement')
                cash_flow = fd.get_cash_flow_annual(stock_name)[0]
                cf = cash_flow.T[2:]
                cf.columns = list(cash_flow.T.iloc[0])
                st.write(cf)
            
if choose == "Charts":
    st.title('Charts')
    option = st.selectbox('Select one symbol', ( 'AAPL', 'MSFT',"SPY",'WMT'))
    today = datetime.date.today()
    before = today - datetime.timedelta(days=700)
    start_date = st.date_input('Start date', before)
    end_date = st.date_input('End date', today)
    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')
    
    df = yf.download(option,start= start_date,end= end_date, progress=False)

    # Bollinger Bands
    indicator_bb = BollingerBands(df['Close'])
    bb = df
    bb['bb_h'] = indicator_bb.bollinger_hband()
    bb['bb_l'] = indicator_bb.bollinger_lband()
    bb = bb[['Close','bb_h','bb_l']]
    
    # Moving Average Convergence Divergence
    macd = MACD(df['Close']).macd()
    
    # Resistence Strength Indicator
    rsi = RSIIndicator(df['Close']).rsi()
    
    # Plot the prices and the bolinger bands
    st.subheader('Stock Bollinger Bands')
    st.write('John Bollinger created a specific kind of price envelope known as the Bollinger Bands. They are represented as envelopes at a standard deviation level above and below the price"s simple moving average. The bands width adjusts to changes in the underlying price"s volatility because it is based on standard deviation. Bollinger bands assist in identifying relative price highs and lows.')
    st.line_chart(bb)
    
    progress_bar = st.progress(0)
    
    # Plot MACD
    st.subheader('Stock Moving Average Convergence Divergence (MACD)')
    st.write('The most well-known price oscillator is undoubtedly the MACD, which Gerald Appel created.When the 12-period SMA (simple moving average) is higher than the 26-period SMA, the MACD is positive. When it is lower than the 26-period SMA, the MACD is negative (simple moving average). The MACD is greater range above or lower than its baseline suggests a widening gap between the two SMAs.')
    st.area_chart(macd)
    
    # Plot RSI
    st.subheader('Stock RSI ')
    st.write('The relative strength index (RSI), invented by Welles Wilder Jr., rose to prominence as a momentum indicator. To determine if a market is overbought or oversold, it examines the size of recent price fluctuations. It can read between 0 and 100 and is shown as an oscillator. Generally speaking, they are: the RSI exceeds 70, an investment is considered to be overbought or overvalued and may be ready for a trend reversal or corrective price retreat. RSI = 30 indicates an oversold or undervalued situation.')
    st.line_chart(rsi)
    
    # Data of recent days
    st.write('Recent data ')
    st.dataframe(df.tail(10))
    
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    
    def get_table_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        val = to_excel(df)
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="download.xlsx">Download excel file</a>' # decode b'abc' => abc
    
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)

if choose == "News": 
    st.title('News Section')
    nse_data, news, openai1 = st.tabs(["NSE Data", "Top 10 News", "OpenAI ChatGPT"])
    
    with nse_data:
        st.subheader('some NSE detail')
        adv_dec = pd.DataFrame(nse.get_advances_declines())
        adv_dec
        
        # nse_index = st.selectbox('SEARCH FOR NIFTY NSE', nse.get_index_list())
        # # nse_index_df = pd.DataFrame(nse.get_index_quote(nse_index))
        # # nse_index_df
        # nse.get_index_quote(nse_index)['name']
        
        st.subheader('Top Gainers in NSE')
        top_gainers = pd.DataFrame(nse.get_top_gainers())
        top_gainers
        
        st.subheader('Top Losers in NSE')
        top_losers = pd.DataFrame(nse.get_top_losers())
        top_losers
        
        # st.subheader('Preopen NIFTY')
        # preopen_nifty = pd.DataFrame(nse.get_preopen_nifty())
        # preopen_nifty.astype(str)
        
        st.subheader('Preopen Bank NIFTY')
        preopen_niftybank = pd.DataFrame(nse.get_preopen_niftybank())
        preopen_niftybank
        
        # st.subheader('Preopen Fno')
        # preopen_fno = pd.DataFrame(nse.get_preopen_fno())
        # preopen_fno
    
    from stocknews import StockNews
    with news:
        ticker_news = st.text_input('Type the ticker', placeholder='MSFT')
        if st.button('Search'):
            st.header(f'News of {ticker_news}')
            sn = StockNews(ticker_news, save_news=False)
            df_news = sn.read_rss()
            for i in range(10):
                st.subheader(f'News{i+1}')
                st.write(df_news['published'][i])
                st.write(df_news['title'][i])
                st.write(df_news['summary'][i])
                title_sentiment = df_news['sentiment_title'][i]
                st.write(f'Title Sentiment {title_sentiment}')
                news_sentiment = df_news['sentiment_summary'][i]
                st.write(f'News Sentiment {news_sentiment}')
        
        
    
    with openai1:
        from pyChatGPT import ChatGPT
        st.write('Find the buy/sell/SWOT analysis for any company stock')
        ticker = st.text_input('Ticker Name', placeholder='MSFT')
        
        if st.button('Analyse'):
        
            session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..Zhki8Rk9AALgVO0W.t7ZyH0NsURcMv4wN-gYkbqxZ-jaxpSaFPEnYqcl434Ieg0HDtTWdS6kKy5Xx5veqDjtgkEn0ygB3m_QbZ7dcHySW0oakJps3IYuEBiAMRm0nJuFtP6aWjLz3yhsDpnIsMoJVE4U0POx3t93zg67v0dnUlBa0uRbU-Kr0KvMQfyScS3a2kVCA6rPYa4sjCDjxoXZbDYF0pJidfz31VMQPeG32IXErK_PF5bv29_81YmpMQXAALDHX_l2f85Q0te8fnQxyMspebV6MSwDcYQfv5GUlPKFiDbujzq54YxvB8mW9dYxVi9P20Zw7vfb8DLQHpxsCxw1-HolDWw0vgxz9NEhoFZBqbdV0XqLhdbow-wGoy08ZXGxpHlJYs8DBML5SZoIOYy1wrxpwTzMC7Csdu7YP4tABE7dYihkqZ4nz2y8eJMT6WJsymUa27HE0voIFRj6Fyk8Ls_VaClHx5vGlmZPnXso9S_U5nYwrkY632roEsnqRwtltaxqz5aGLDSi2-5W3IJcE6Umu90SoJESGu9JWjtMpF933-2CqmYFYwmmzg6Yv_9ak55eVPO2p_HtsO40BtkN5LaorstUcX_6-415BpP_D5ppuNeTVJhzuxuwgM83hur1tdVXpL13ulMpK1XP-lKp3pH-xXTCTvbr8mmauGnPTW1u1d1SqbEom-DaNriWDbkGyacVz3wkzP6k8tmd71nEydz5lyZNh_d0coZBZFMcwXWM7k6k2PIOLAPZUtSdXKOtAzYUR4clS7dW0pTE5UD6gQj-wWIdU9P3DR5js9IuVIeCX-8pEPHVHPdo_qMDu671x1l1THq1p5C1f-c31ZfLVv4xxmHRwVcdkKeT2ZYbEJ5TqlLODx9O1gOsFf16d1osR-ushUC09NCb1sh1EuNHNzKP2dFQFG-pMzgJZCtBYKFTjtg0rBm5xIDzuHjhzNu-7sNvsKR1g0l9hFNecxj8EgBWjfKnKeIqtawKI7ZsjPZZWB4qn11F6AoLHgx44Ztliia_dkw9uE6KgbmrbGLA-SYaXKxSTrmVQiMrgFKkIWq4aoWeCaYX62FvkUH1PQmLWE5heN9viWS8zpKjYeKBZknDDR46IHi57S4f21xytu_En50waLzwtjJDrwaWPM4bIPQ6qpKsdWu32kQ38rOQ_gwsEUkjxwCIz8GdZorTndMfE71plgW_zaxiJsAzdm24CUGgGIlc2xojBqQDrizQFfeX54H6JVZKUSAxl6qyB4hs_pnOvR4I_HiCszCoZew2bcMjmWTMABito4grJGzWxQqI2iu3AmcUtd_cqwPclueZIrNoZIVsaR4hoCAgOb7q7bwgSFEkEawEevsHZtSb1-GpMCPzKHQ8vpIK2Uy2x4t19B-nBvgzyf-w5JV6RvOuLPf_gGSevXAPgYTh5PoYLfQEPJAyIHbAr4cRnzcABf72CnC_GqTJza09-1EFSVpoTR4hqpPaN9uJq3CcZmHorxkTsXQdiazQKdnz4aVgmerM5CuHDXmylKNkEAS9dCvZBmPX6Wx8_pggDVyO_zm98LtkAF58UtIKp0WEM3-yhtjr6Y0TIbQAzf1UQ-UDY_bGEpmvlpWuclzPl0H8Xx6zBmScaGIMbLq4i31VGFqi96aXMvXAl4BJqWGHkf8beTi1TBoGE8KFx7jGDmsI0-j9WaJ-KOwU8k9Mw5Eljdz7n_1jRE4fY9_QVYxvgPq8IywXcbnH9S336kMDWsb86JZTIzPWwlVxf1MvTG5flG27TGgmajC51O6hNHcydcqPc-G1CbeU5ANJfWdbp0M9cQ5ZmyLpJkCR83735DGye39U-NNds27JdcEW38NeIWIZqTnEospWhp8QVDJCda6inqJQQI8kZf5s56Nh_JArJMROF76JovawL2aqcDUwheY-p_50j7ZoGHq6_qZXMlVqYTzxV6pn06iZFlVfxM5uaOmYH2l9aHefWEbzI4D1XDk-1JtJLCJ6hgRMxAHsj2Mkj5eJ2BGPkFcYLIfcP_6mK57mhF3_Z5YgwRMQytNDlWygDdFdHdOZQKb2uHcFhmZa3DFkaGmMasjo53UikqQ_OjaEOJHPJoafydv2LwGOK0OZSe0j8Bmod_9vkXLLwuCfoZsZJUbWcJnECj2VPdQS0XUTYuzWDeqTHzna_68byQZB7OJSQGiUnwmcRAAnos_dkhHGtZRmq3ySEjakB0kOE4EHXWOBtQ0kSxdnkfI-uHvM2v8Fz71QLujnwCPgVBWYJrf9ADSUEscaNQ10pL2qsE42MRt1tm073VXxv6_VFx7CdUHZDqNvjpEnifX7B-Fh_SWk_ZT6xttGRoagCHjklgqQnNQnquUPKvRTtXj8l73Ip9VfCMhoU4EfS0g.H_5wOAlFWy-7u3OQzCMexA'
            api2 = ChatGPT(session_token)
            buy = api2.send_message(f'3 Reasons to buy {ticker} stock')
            sell = api2.send_message(f'3 Reasons to sell {ticker} stock')
            swot = api2.send_message(f'SWOT analysis of {ticker} stock')
            
            buy_reason, sell_reason, swot_analysis = st.tabs(['3 Reasons to buy', '3 Reasons to sell', 'SWOT analysis'])
            
            with buy_reason:
                st.subheader(f'3 reasons on why to buy {ticker} stock')
                st.write(buy['message'])
            with sell_reason:
                st.subheader(f'3 reasons on why to sell {ticker} stock')
                st.write(sell['message'])
            with swot_analysis:
                st.subheader(f'3 reasons on why to sell {ticker} stock')
                st.write(swot['message'])
#         components.html(
#     """
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_a9d26"></div>
#   <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL stock chart</span></a> by TradingView</div>
#   styles={"height": "100vh"}
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "width": "100%",
#   "height": 500,
#   "symbol": "NASDAQ:AAPL",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "theme": "light",
#   "style": "1",
#   "locale": "en",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "allow_symbol_change": true,
#   "container_id": "tradingview_a9d26"
# }
#   );
#   </script>
# </div>
# <!-- TradingView Widget END -->""")
    
    
    
    
    
    
    
    
























