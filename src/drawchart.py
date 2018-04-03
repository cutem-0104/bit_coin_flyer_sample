#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt


class DrawChart(object):
    """
    This class draw the btc price.
    """

    def __init__(self):
        """
        Define about data path.
        """
        self.input_dir = '../data/'
        self.file_name = 'bit_data.csv'

    def run(self):
        """
        This pipeline read btc data frame and draw btc price.
        :return:
        """

        df_btc = self.load_data()
        btc_price = df_btc['price']
        exec_date = df_btc['exec_date']

        date_list = []
        date_list = self.format_date(exec_date, date_list)

        self.plot_btc(btc_price, date_list)

    def load_data(self):
        """
        Load btc data.
        :return: btc data frame
        """

        input_path = os.path.join(self.input_dir, self.file_name)
        df_btc = pd.read_csv(input_path)
        print('load {}'.format(input_path))
        return df_btc

    def plot_btc(self, price, date):
        """
        Draw btc price.
        :param price: btc price
        :param date: btc execute date
        :return:
        """

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(date, price)
        ax.set_title('btc price')
        ax.grid()

        hour = mdates.HourLocator()
        hour_format = mdates.DateFormatter("%Y:%D:%H:%M")
        ax.xaxis.set_major_locator(hour)
        ax.xaxis.set_major_formatter(hour_format)

        plt.show()

    def format_date(self, df_date, date_list):
        """
        Format string date as datetime.
        :param df_date: btc execute date data frame
        :param date_list: empty list
        :return: datetime formatted string date
        """
        for str_date in df_date:
            tmp_date = str_date.replace('T', ' ')
            tmp_date = tmp_date.split('.')
            tmp_date = tmp_date[0]
            date = dt.strptime(tmp_date, '%Y-%m-%d %H:%M:%S')
            date_list.append(date)
        return date_list


if __name__ == '__main__':
    draw_chart = DrawChart()
    draw_chart.run()
