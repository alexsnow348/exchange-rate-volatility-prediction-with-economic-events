"""Get EURUSD data from Yahoo Finance.

The script will get the EURUSD  data from Yahoo Finance.

Example:
        $ python get_currency_data.py
"""

import pandas as pd
import yfinance as yf
# yf.pdr_override()  # <== that's all it takes :-)

CURRCY_PAIR_CODE = "EURUSD=X"
START_DATE = "2019-06-17"
END_DATE = "2019-06-22"

# download
data = yf.download(  # or pdr.get_data_yahoo(...
    # tickers list or string as well
    tickers=CURRCY_PAIR_CODE,
    period="ytd",
    interval="1m",
    auto_adjust=True,
    prepost=True,
    treads=True,
    proxy=None,
    start=START_DATE,
    end=END_DATE
)
# write data to csv file
data.to_csv('../data/EURUSD_20190619_to_20190622.csv')
