#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick2_ohlc, volume_overlay
from datetime import datetime as dt
import datetime



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

        exec_date = df_btc['exec_date']

        date_list = []
        date_list = self.format_date(exec_date, date_list)
        one_minute_date_list = self.get_one_minute_datetime(date_list)

        adjust_df_btc = df_btc.drop('exec_date', axis=1)
        adjust_df_btc['datetime'] = one_minute_date_list

        summary = self.generate_candle_data(adjust_df_btc)

        self.plot_btc(summary)

    def get_one_minute_datetime(self, date_list):
        return [x.replace(second=0) for x in date_list]

    def load_data(self):
        """
        Load btc data.
        :return: btc data frame
        """

        input_path = os.path.join(self.input_dir, self.file_name)
        df_btc = pd.read_csv(input_path)
        print('load {}'.format(input_path))
        return df_btc

    def generate_candle_data(self, adjust_df_btc):
        """

        :param adjust_df_btc:
        :return:
        """

        # ref http://www.madopro.net/entry/bitcoin_chart
        summary = adjust_df_btc[['datetime', 'price']].groupby(['datetime']).min().rename(columns={'price': 'min'})
        summary = summary.merge(
            adjust_df_btc[['datetime', 'price']].groupby(['datetime']).max().rename(columns={'price': 'max'}),
            left_index=True, right_index=True)
        summary = summary.merge(
            adjust_df_btc[['datetime', 'price']].groupby(['datetime']).last().rename(columns={'price': 'first'}),
            left_index=True, right_index=True)
        summary = summary.merge(
            adjust_df_btc[['datetime', 'price']].groupby(['datetime']).first().rename(columns={'price': 'last'}),
            left_index=True, right_index=True)
        summary = summary.merge(
            adjust_df_btc[['datetime', 'size']].groupby(['datetime']).sum(),
            left_index=True, right_index=True)

        return summary

    def plot_btc(self, summary):
        """

        :param summary:
        :return:
        """
        df2 = summary[-1000:]

        # ローソク足をプロット
        fig = plt.figure(figsize=(18, 9))
        ax = plt.subplot(1, 1, 1)
        candlestick2_ohlc(ax, df2["first"], df2["max"], df2["min"], df2["last"], width=0.9, colorup="b", colordown="r")
        ax.set_xticklabels([(df2.index[int(x)] if x < df2.shape[0] else x) for x in ax.get_xticks()], rotation=90)
        ax.set_xlim([0, df2.shape[0]])
        ax.set_ylabel("Price")
        ax.grid()

        # ローソク足を上側75%に収める
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom - (top - bottom) / 4, top)

        # 出来高のチャートをプロット
        ax2 = ax.twinx()
        volume_overlay(ax2, df2["first"], df2["last"], df2["size"], width=1, colorup="g", colordown="g")
        ax2.set_xlim([0, df2.shape[0]])

        # 出来高チャートは下側25%に収める
        ax2.set_ylim([0, df2["size"].max() * 4])
        ax2.set_ylabel("Volume")

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
            # Adjust ISO format to Japan time
            date = date + datetime.timedelta(hours=9)
            date_list.append(date)
        return date_list


if __name__ == '__main__':
    draw_chart = DrawChart()
    draw_chart.run()
