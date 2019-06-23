import pandas as pd
import numpy as np
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

    def eurusd_pre_process(self, mins):
        # change timezone to local time
        eurusd_data = self.eurusd_data
        eurusd_data['timestamp'] = eurusd_data['Datetime'].apply(
            lambda x: self.utc_to_local(x))
        eurusd_data = eurusd_data[['timestamp', 'Close']].copy()
        initial = 0
        data_dict_array = []
        while mins <= 6451:  # data points
            one_hour = eurusd_data[initial:mins]
            timestamp = eurusd_data['timestamp'][mins]
            one_hour_array = list(one_hour['Close'])
            one_hour_dict = {}
            for i in range(len(one_hour_array)):
                one_hour_dict.update({
                    str(i): one_hour_array[i]
                })
            one_hour_std = np.std(one_hour_array)
            one_hour_dict.update({
                'timestamp': timestamp,
                'std': one_hour_std
            })
            initial += 1
            mins += 1
            data_dict_array.append(one_hour_dict)
        data_frame = pd.DataFrame(data_dict_array)
        self.eurusd_process_data = data_frame
        data_frame.to_csv('../data/eurusd_pre_process.csv', index=False)

    def ecoevent_pre_process(self):
        focus_data = self.ecoevent_data[['timestamp_local', 'impact']].copy()
        unique_timestamp = focus_data['timestamp_local'].unique()

        # Get the max impact when there is more than one annountment
        # and expand it into 60 mins timeframe (before 30 mins, after 30 mins)
        # of that annountment
        final_impact_df = pd.DataFrame()
        for each in unique_timestamp:
            found = focus_data.loc[focus_data['timestamp_local'] == each]
            impact = max(found['impact'])
            impact_dict_array = [{
                'timestamp': each,
                'impact': impact
            }]
            init_timestamp = each

            # for before 30 mins
            before_diff = init_timestamp - 60
            diff = init_timestamp - before_diff
            while diff <= 1740:
                impact_dict_array.append({
                    'timestamp': before_diff,
                    'impact': impact
                })
                before_diff -= 60
                diff = init_timestamp - before_diff

            # for after 30 mins
            after_diff = init_timestamp + 60
            diff = after_diff - init_timestamp
            while diff <= 1800:
                impact_dict_array.append({
                    'timestamp': after_diff,
                    'impact': impact
                })
                after_diff += 60
                diff = after_diff - init_timestamp
            impact_dataframe = pd.DataFrame(impact_dict_array)
            impact_dataframe_sorted = impact_dataframe.sort_values(
                by=['timestamp'], ascending=False)
            impact_dataframe_sorted = impact_dataframe_sorted.reset_index(drop=True)
            final_impact_df = final_impact_df.append(impact_dataframe_sorted)

        self.ecoevent_process_data = final_impact_df.reset_index(drop=True)
        final_impact_df.to_csv('../data/ecoevent_pre_process.csv', index=False)

    def merge_ecoevent_eurusd(self):
        final_data = pd.merge(self.eurusd_process_data,
                              self.ecoevent_process_data, on='timestamp')
        final_data.fillna(0)
        final_data.to_csv('../data/final_process_data.csv', index=False)


if __name__ == '__main__':

    eurusd_file = '../data/EURUSD_Week_25.csv'
    ecoevent_file = '../data/Eco_Event_Week_25.csv'
    procesing = PreProcessing(eurusd_file, ecoevent_file)
    procesing.eurusd_pre_process(60)
    procesing.ecoevent_pre_process()
    procesing.merge_ecoevent_eurusd()
