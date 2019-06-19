import pandas as pd
import yfinance as yf
# yf.pdr_override()  # <== that's all it takes :-)

CURRCY_PAIR_CODE = "EURUSD=X"
START_DATE = "2019-06-15"
END_DATE = "2019-06-19"

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
data.to_csv('../data/EURUSD_20190615_to_20190619.csv')
