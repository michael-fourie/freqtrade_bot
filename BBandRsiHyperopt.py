# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here
import talib.abstract as ta  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib


class BBandRsiHyperopt(IHyperOpt):

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
    
        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
       
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    @staticmethod
    def stoploss_space() -> List[Dimension]:

        return [
            Real(-0.05, -0.01, name='stoploss'),
        ]

    @staticmethod
    def generate_roi_table(params: Dict) -> Dict[int, float]:

        roi_table = {}
        roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9'] + params['roi_p10']
        roi_table[params['roi_t10']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8'] + params['roi_p9']
        roi_table[params['roi_t10'] + params['roi_t9']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7'] + params['roi_p8']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6'] + params['roi_p7']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5'] + params['roi_p6']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4'] + params['roi_p5']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3'] + params['roi_p4']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4']] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3']] = params['roi_p1'] + params['roi_p2']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2']] = params['roi_p1']
        roi_table[params['roi_t10'] + params['roi_t9'] + params['roi_t8'] + params['roi_t7'] + params['roi_t6'] + params['roi_t5'] + params['roi_t4'] + params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

        return roi_table

    @staticmethod
    def roi_space() -> List[Dimension]:

        return [
            Integer(1, 300, name='roi_t10'),
            Integer(1, 300, name='roi_t9'),
            Integer(1, 300, name='roi_t8'),
            Integer(1, 300, name='roi_t7'),
            Integer(1, 300, name='roi_t6'),
            Integer(1, 300, name='roi_t5'),
            Integer(1, 300, name='roi_t4'),
            Integer(1, 300, name='roi_t3'),
            Integer(1, 300, name='roi_t2'),
            Integer(1, 300, name='roi_t1'),

            Real(0.001, 0.005, name='roi_p10'),
            Real(0.001, 0.005, name='roi_p9'),
            Real(0.001, 0.005, name='roi_p8'),
            Real(0.001, 0.005, name='roi_p7'),
            Real(0.001, 0.005, name='roi_p6'),
            Real(0.001, 0.005, name='roi_p5'),
            Real(0.001, 0.005, name='roi_p4'),
            Real(0.001, 0.005, name='roi_p3'),
            Real(0.0001, 0.005, name='roi_p2'),
            Real(0.0001, 0.005, name='roi_p1'),
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe.loc[
            (
                    (dataframe['rsi'].rolling(8).min() < params['buy-rsi-value']) &
                    (dataframe['close'] < dataframe['bb_lowerband'])

            ),
            'buy'] = 1
            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Integer(0, 50, name='buy-rsi-value'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
          dataframe.loc[
            (
                (dataframe['rsi'] > params['sell-rsi-value']) &
                (dataframe['close'] > dataframe['bb_upperband'])
            ),
            'sell'] = 1
          return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            Integer(50, 100, name='sell-rsi-value'),
        ]
        
        
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'].rolling(8).min() < 41) &
                    (dataframe['close'] < dataframe['bb_lowerband'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                  
                    (dataframe['rsi'].rolling(8).max() > 93) &
                    (dataframe['close'] > dataframe['bb_upperband'])

            ),
            'sell'] = 1
        return dataframe