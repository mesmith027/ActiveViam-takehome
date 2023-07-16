import yfinance as yf 
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

st.set_page_config(layout="wide")

st.title("yFinance Streamlit App")
st.write("""
### Using yFinance to calculate PnL

This app will show a short example of how to use the yfinance python package to calculate the profit and loss of 5 stocks. The stocks chosen for this example will be: 
- Apple, denoted as "AAPL", 
- Google, denoted as "GOOGL", 
- Microsoft, denoted as "MSFT", 
- Amazon, denoted as "AMZN" and 
- Meta (Facebook), denoted as "META". 

This assumes you have downloaded the Python packages: plotly, yfinance, pandas and Streamlit. 

If you have not installed these packages, open your terminal and run the commands: 

```
pip install yfinance
pip install plotly
pip install pandas
pip install streamlit
```

""")

st.write("""
Let's create a list with the stock names that we are interested in looking at. In the yfinance package, the information about 
a stock is stored or downloaded in a "ticker". So we will call our list "tickers" and use it to download the stock price for all 5 stocks at the same time:""")
with st.echo(): 
    # Define the starting tickers
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']

st.write(""" 
To get options for our `st.multiselect`, we can grab the Ticker names for the top 100 stocks from [Wikipedia](https://en.wikipedia.org/wiki/Nasdaq-100)! 
        """)

with st.echo(): 
    # # Get the top 100 NASDAQ stock symbols from Wikipedia
    payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')

    # data that has the list of the ticker names is the 4th entry in the payload json
    fourth_table = payload[4]

    # make the ticker column a list we can enter into our multiselect
    stocks_list = list(fourth_table["Ticker"])


st.write("""
Time to create our sidebar that will have the multiselect and the date purchased. The multiselct will be for choosing the stocks a user of our app is interested 
in looking at. The Date purchased will be the date that the user wants to "go back to" and pull all the financial information from that date until today. We have used 
the "Adj Close" price, however, you could use any of the available prices that are stored, some examples are: 
         
- "High": Highest price recorded for the day
- "Low": Lowest price recorded for the day
- "Close": Price of the stock at the time the stock exchange closed
- "Open": Price of the stock at the time the stock exchange opened""")
with st.echo():   
    # set the date of today
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # set a default start date for our date input widget
    default_start = datetime.date(2022,1,1)

    # create a sidebar and add the following
    with st.sidebar: 
        # adding all the stocks into the multiselect with the default as our chosen tickers list
        chosen_stocks = st.multiselect("Choose the stocks your interested in", stocks_list, default= tickers, max_selections=8)

        # date that we want to go back to, with the defalut value as the default_start date
        date = st.date_input("Date purchased", value= default_start)

    # Get data for the tickers, "Adj Close", is the adjusted closing price of the stock. 
    #    It takes into account the price after adjustments for all applicable splits and dividend distributions
    data = yf.download(chosen_stocks, start=date, end=today)['Adj Close']

    # write our data to the streamlit app 
    data
###############################################################

st.write("""
## Plot of price over time

First, let's plot the share price over time to see the price fluctuations over the period we downloaded. The data we have downloaded starts 
on %s, and ends on %s, today. The rows represent each day that the stock exchange was open. Our columns are the 5 
stocks we were interested in. (See the pandas dataframe above.)""" % (date, today))

with st.echo():

    # plot data with plotly.express to make an interactive graph

    # plot data 
    fig = px.line(data, x=data.index, y=data.columns)

    # add titles and information
    fig.update_layout(
        title="Share Price Over Time: Adj Close",
        xaxis_title="Date",
        yaxis_title="Value per Share ($ USD)",
        legend_title="Stocks",
    )

    # show the plot at the full width of the app
    st.plotly_chart(fig, use_container_width=True)
###############################################################
st.write("""
This graph gives us an overview of what happened to each stock over the time period of data. 

## PnL: Profits and Losses per Single Stock Price

Now, let's use this data to calculate the profit or loss of each stock. This first one will be per 1 share of the stock. 

We will assume: 

- the purchase date of the stock is the first day in the database.
- the stock sale is the last day in the database. """)

with st.echo(): 
    # Compute the purchase price (assuming its the start date) and current price (assuming its the end date)
    purchase_price = data.iloc[0] # grabs the 1st row
    current_price = data.iloc[-1] # grabs the last row

    # Compute the profit and loss (per share)
    pnl = current_price - purchase_price

    # for fun, let's sort the values higest to lowest profit
    pnl = pnl.sort_values(ascending=False)

    # pnl_position will be used to colour code the graph of profit and loss 
    pnl_positive = pnl >0 

    col1,col2 = st.columns(2)
    with col1:
        # lets look at our values 
        st.write("PnL Values:")
        st.write(pnl)

    with col2: 
        st.write("If the values are positive or negative:")
        st.write(pnl_positive)

###############################################################

st.write("""
Any positive numbers represent profit, and any negative numbers represent losses. 
Time to make a graph of these! 

## Graph of Basic Profit and Loss for Each Company

Let's visualize the profit and loss for each company on a bar graph, giving us a visual comparison of how well the companies have done in comparison to each other. 
         """)

with st.echo(): 

    # make the plot, use the color parameter to map the colour of the bar based on gain or loss
    fig = px.bar(pnl, color=pnl_positive,
                color_discrete_map={
                False: "red",
                True: "green",
                })

    # add titles and information
    fig.update_layout(
        title="Basic Profit and Loss (per Share)",
        xaxis_title="Stock",
        yaxis_title="Profit and Loss ($ USD)", 
        showlegend=False 
    )

    # show the plot at the full width of the app
    st.plotly_chart(fig, use_container_width=True)
###############################################################

st.write("""
Now we can see just how much, in comparison, each stock has lost or gained. Now, this is still per share, so the last thing we may want to do is calculate a 
total loss and profit based on how many stocks you own in each company. 

## Your Personal PnL 

To do this, we will need to take the price per single stock and multiply that by the number of stocks you purchased on our initial purchase date 
for each company. 

This can be interactive feel free to adjust the list `your_shares` to see the effect it has on the profit and loss of each and your total profit 
(or loss) over this time period. 
         """)

with st.echo(): 

    # make an empty list of 0's of all the stocks we have
    your_shares = list(0 for _ in range(len(pnl)))
    #your_shares = list(range(len(pnl)))
    
    # in the side bar we will make number inputs 
    with st.sidebar: 
        for i in range(len(pnl)): 
            # grab the name of the stock
            input_name = pnl.index[i]
            # use the name of the stock as the name for the number input, minimum values of having at least 1 stock
            your_shares[i]= st.number_input(input_name, min_value=1, value=2)

    # calculate your profit/loss for each stock by multiplying the pnl x the number of stocks you bought
    your_pnl = pnl*your_shares

    # write to the Streamlit app the list of your calculated profit/loss
    st.write("Your profit/loss for each stock:", your_pnl)

    # calculate the total
    your_sum = your_pnl.sum()

    # write out your total profit or loss from all your stock investments
    st.write("**Sum of your profits and losses:**", your_sum)

  
###############################################################
st.write("""
Like before, we can visualize our stocks' actual profit and loss.
""")

with st.echo(): 

    # make the plot, use the color parameter to map the colour of the bar based on gain or loss
    fig = px.bar(your_pnl, color=pnl_positive,
                color_discrete_map={
                False: "red",
                True: "green",
                })

    # add titles and information
    fig.update_layout(
        title="Your Basic Profit and Loss Totals",
        xaxis_title="Stock",
        yaxis_title="Profit and Loss ($ USD)", 
        showlegend=False 
    )

    # show the plot at the full width of the app
    st.plotly_chart(fig, use_container_width=True)

