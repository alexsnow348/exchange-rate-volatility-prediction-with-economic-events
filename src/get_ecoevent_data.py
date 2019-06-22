"""Get Key Economic Event Notification Details.

The script will write the current week economic events details info into csv file.
The economic event details info are being scraping from Investing.com.
(https://sslecal2.forexprostools.com/)

Example:
        $ python get_ecoevent_data.py
"""

import requests as rq
import pandas as pd
import json
from datetime import datetime, timezone, timedelta


class API(object):
    """docstring for API."""

    def __init__(self, url):
        super(API, self).__init__()
        self.url = url
        request = rq.get(self.url)
        data = json.loads(request.text)
        self.data_df = pd.DataFrame(data)
        self.data_df = self.data_df.dropna(how='any', axis=0)

    def utc_to_local(self, utc_dt):
        utc_dt = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        local = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return local.timestamp()

    def formatData(self, date, major):
        # impactful_data = self.data_df.loc[self.data_df['impact'] == 3].copy()
        impactful_data = self.data_df
        impactful_data['timestamp_local'] = impactful_data['timestamp'].apply(
            lambda x: self.utc_to_local(x))
        impactful_data['major'] = impactful_data['economy'].apply(
            lambda x: True if x in major else False)
        impactful_data = impactful_data.loc[
            impactful_data['major'] == True].copy()
        impactful_data = impactful_data[["actual",	"economy",	"forecast",
                                         "impact",	"name",	"previous",
                                         "timestamp_local"]].copy()

        impactful_data.to_csv("../data/Eco_Event_Week_25.csv", index=False)


if __name__ == '__main__':
    major = ['EUR', 'USD']
    url = 'https://eco-event.000webhostapp.com/'
    date_time = datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    print(date)
    date_time = date_time - timedelta(minutes=3)
    date_time = date_time.strftime("%s")
    sample_call = API(url)
    sample_call.formatData(date, major)
