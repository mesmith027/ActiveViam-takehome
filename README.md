# ActiveViam Take-home

Test instructions:

This exercise will require you to create a notebook (we recommend Jupyter) teaching someone how to do the following:
- Use the yfinance library to get data for 5 or so tickers
- Compute PnL (basic profit and loss based on purchase vs current value)
- Visualize using Matplotlib

Prior knowledge of finance is not required, it should be possible to find out what is required through the internet/reading around.

The exercise should not take more than a couple of hours. Some parts of the exercise are left vague, and it is up to you to decide how to proceed.
We would expect answers to the exercise in Python.

You are given 3 working days to return your solution

## Jupyter notebooks

The good copy of my take home is in the file `Take-Home-Final.ipynb`. 
The python pagkages you need to run this notebook are: yfinance and matplotlib. 

If your interested in some of the random explorations and testing I did to learn about the yfinance package is in `Initia-exploration.ipynb`


## Streamlit app 

I have also re-created this notebook into a Streamlit app. Sicne this kind of teaching/tutorials are very informative if the user can interact with the interface without necessarily ahveing to chage the code itself. It give them an opportunity to get hand on and try out some thigns without beaking snything as they are learning a package, in this case yfinance. 

To try this app yourself, simply download the open source streamlit python package, navigate to this directory and run the app.py file. 

`pip install streamlit`

*Navigate to the directory with the streamilt app python file*

`streamlit run app.py`

Streamlit will automatically open the UI for you at `http://localhost:8501/`. 

If you would like to view this app deployed click the link here: https://marisas-activeviam-takehome.streamlit.app/