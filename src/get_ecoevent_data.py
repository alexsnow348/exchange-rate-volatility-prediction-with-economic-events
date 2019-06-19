"""Key Economic Event Notification Engine.
The engine will notify the impacful infomation to the required agent.
Example:
        $ python main.py
Todo:
    * Get level 3 impactful data (done)
    * Change timezone to locals (done)
    * Get list of time and change it into 3 minutes before timestamp (done)
    * Send twillo message to phone when current time is in the time list. (done)
    * Make one API call per day only
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
        return local.strftime("%Y-%m-%d %H:%M:%S")

    def formatData(self, date, major):
        # impactful_data = self.data_df.loc[self.data_df['impact'] == 3].copy()
        impactful_data = self.data_df
        impactful_data['timestamp_local'] = impactful_data['timestamp'].apply(
            lambda x: self.utc_to_local(x))
        impactful_data['date'] = impactful_data['timestamp_local'].apply(
            lambda x: x[:10])
        impactful_data['major'] = impactful_data['economy'].apply(
            lambda x: True if x in major else False)
        impactful_data = impactful_data.loc[
            impactful_data['major'] == True].copy()
        impactful_data.to_csv("../data/Week_25_2019_Eco_Event.csv", index=False)


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
