#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import pandas as pd
from progressbar import ProgressBar


class PythonBitFlyerApp(object):

    def __init__(self, count=500, count_limit=20):
        # before id
        self.before_id = 0
        # bit data size
        self.count = count
        # loop size
        self.count_limit = count_limit
        # request url
        self.domain_url = 'https://api.bitflyer.jp'
        self.execution_history_url = '/v1/getexecutions'
        self.output_dir = './data/'
        self.output_file_name = 'bit_data.csv'
        # column array
        self.keys = ['id',
                     'side',
                     'price',
                     'size',
                     'exec_date',
                     'buy_child_order_acceptance_id',
                     'sell_child_order_acceptance_id']

    def run(self):
        # params
        execution_history_params = {'count': self.count,
                                    'before': self.before_id}

        # init ProgressBar
        p = ProgressBar(0, self.count_limit)

        # init DataFrame
        df = pd.DataFrame(columns=self.keys)

        for progress_num in range(self.count_limit):
            # request execution history
            response = self.execute_api_request(self.execution_history_url, execution_history_params)
            btc_list = response.json()

            # get latest id and last id
            latest_id = btc_list[0]['id']
            last_id = btc_list[-1]['id']

            # update parameters with last id
            execution_history_params['before'] = last_id

            # TODO use logger
            print('latest id: {}'.format(latest_id))
            print('last_id: {}'.format(last_id))

            # show execution progress
            p.update(progress_num)

            tmp_df = pd.read_json(response.text)
            df = pd.concat([df, tmp_df])

        self.save_result_data(df)

    # execute api request
    def execute_api_request(self, url, params):
        request_url = self.domain_url + url
        return requests.get(request_url, params=params)

    def save_result_data(self, result_df):
        output_path = os.path.join(self.output_dir, self.output_file_name)
        result_df.to_csv(output_path, index=False)
        print('save on {}'.format(output_path))


if __name__ == '__main__':
    python_bit_flyer_app = PythonBitFlyerApp()
    python_bit_flyer_app.run()
