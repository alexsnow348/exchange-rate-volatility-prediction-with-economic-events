import pandas as pd
from datetime import datetime, timezone, timedelta


class PreProcessing(object):
    """docstring for EURUSD."""

    def __init__(self, eurusd_file, ecoevent_file):
        super(PreProcessing, self).__init__()
        self.eurusd_data = pd.read_csv(eurusd_file)
        self.ecoevent_data = pd.read_csv(ecoevent_file)

    def utc_to_local(self, utc_dt):
        utc_dt = utc_dt[:18]
        utc_dt = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        local = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return local.timestamp()

    def eurusd_pre_process(self):
        # change timezone to local time
        eurusd_data = self.eurusd_data
        eurusd_data['timestamp'] = eurusd_data['Datetime'].apply(
            lambda x: self.utc_to_local(x))
        eurusd_data = eurusd_data[['timestamp', 'Close']].copy()
        print(eurusd_data.head(100))


if __name__ == '__main__':

    eurusd_file = '../data/EURUSD_Week_25.csv'
    ecoevent_file = '../data/Eco_Event_Week_25.csv'
    procesing = PreProcessing(eurusd_file, ecoevent_file)
    procesing.eurusd_pre_process()
