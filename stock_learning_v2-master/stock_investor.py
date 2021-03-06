import math
import os
import random
from itertools import product
from shutil import copyfile
from typing import Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

import logging_config as log
from config import InvestConfig
from corp_loader import CorpLoader
from data_analyzer import DataAnalyzer
from utils.data_utils import DataUtils
from utils.date_utils import DateUtils


class StockInvestor:
    """
    주식투자 관련 메소드
    """

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    INVEST_PATH = os.path.join(ROOT_PATH, "results", "invest")

    def __init__(self):
        self.logger = log.get_logger(self.__class__.__name__)
        self.cfg = InvestConfig()

    def invests_mock_all(self, corps=None, sample_cnt=None, **params):
        """
        전 주식을 대상으로 모의 투자를 실시한다.
        :return:
        """
        if corps is None:
            corps = self.get_corps(sample_cnt)
        return self.invests_mock(corps, **params)

    @staticmethod
    def get_corps(sample_cnt=None):
        corp = CorpLoader()
        corps = corp.get_crops_confidence()
        if not (sample_cnt is None):
            corps = corps.sample(sample_cnt, random_state=1)
        return corps

    def mean_investing_mock_all(self, grid_params, **params):
        """
        전 주식을 대상으로 모의 투자를 실시하여 평균 값을 구한다.
        :return:
        """
        values = []
        for key, value in grid_params.items():
            if key == "mean_value":
                continue
            values.append(value)
        params.update(grid_params)
        result = self.invests_mock_all(**params)
        file_name = f"search_gird({'-'.join(map(str, values))}).txt"
        save_path = os.path.join(self.INVEST_PATH, "details", file_name)
        DataUtils.save_csv(result, save_path)
        return result['predict'].mean(), result

    def search_grid_investing_mock_all(self, param_grid, **params):
        """
        전 주식을 대상으로 모의 투자를 실시하여 평균 값을 구한다.
        :return:
        """
        keys = param_grid.keys()
        values = param_grid.values()

        product_len = len(list(product(*values)))
        for idx, instance in enumerate(product(*values)):
            grid_params = dict(zip(keys, instance))
            print(f"{idx + 1}/{product_len} search grid ... params: {grid_params}")
            self.search_investing_mock(grid_params, **params)

    def search_investing_mock(self, grid_params, **params) -> Tuple[float, bool]:
        queries = []
        for key, value in grid_params.items():
            if key == "mean_value":
                continue
            queries.append(f"{key}=={value}")
        query = " and ".join(queries)
        if os.path.exists(self.cfg.searched_file_path):
            result = pd.read_csv(self.cfg.searched_file_path)
            searched = result.query(query)
            if len(searched.index) > 0:
                mean_value = searched['mean_value'].values[0]
                if mean_value > 0:
                    return mean_value
        mean_value, invest_data = self.mean_investing_mock_all(grid_params, **params)
        grid_params['mean_value'] = mean_value
        result = pd.DataFrame([grid_params])
        result = DataUtils.update_csv(result, self.cfg.searched_file_path, sort_by="mean_value", ascending=False)
        self.save_best_invest(result, mean_value, invest_data)
        return mean_value

    def save_best_invest(self, result, mean_value, invest_data):
        if len(result.index) > 0:
            max_mean = result.iloc[0]['mean_value']
            if mean_value == max_mean:
                DataUtils.save_csv(invest_data, self.cfg.best_file_path)
        else:
            DataUtils.save_csv(invest_data, self.cfg.best_file_path)

    def search_auto_samples_investing_mock_all(self, first_sample_cnt=None, **params):
        corps = self.get_corps()
        corps_len = len(corps.index)
        if first_sample_cnt is None:
            sample_cnt = corps_len // 32 + 1
        else:
            sample_cnt = first_sample_cnt
        for _ in range(2):
            print(f"sample_cnt: {sample_cnt}")
            self.search_auto_investing_mock_all(sample_cnt=sample_cnt, init_result=True, stored_model_only=True,
                                                update_stock=False, **params)
            sample_cnt = None

    def search_auto_investing_mock_all(self, rolling_cnt=1, hyper_params: dict = None, sample_cnt=None,
                                       init_result=False, start_divisor=3, **params):
        if hyper_params is None:
            hyper_params = self.get_first_auto_params()
        if init_result:
            self.init_investing_mok_result()
        corps = self.get_corps(sample_cnt)
        print(f"search auto (1) ... params: {hyper_params} ")
        keys = list(hyper_params.keys())
        max_value = self.search_investing_mock(hyper_params, corps=corps, **params)
        divisor = start_divisor
        idx = 1
        basic_start_interval = 15
        for _ in range(rolling_cnt):
            is_stop = False
            while is_stop is False:
                is_stop = True
                random.shuffle(keys)
                basic_interval = math.trunc(basic_start_interval / divisor)
                for param_key in keys:
                    now_value = hyper_params[param_key]
                    interval = max(math.trunc(now_value / divisor), basic_interval, 1)
                    if interval > 1:
                        is_stop = False
                    idx, max_value = self.search_auto_investing_mock_all_param(hyper_params, param_key, interval, idx,
                                                                               max_value, corps=corps, **params)
                divisor *= 2

    @staticmethod
    def get_intervals(interval_start=8):
        intervals = [interval_start]
        interval = interval_start
        while True:
            interval = math.ceil(interval / 2)
            intervals.append(interval)
            if interval == 1:
                break
        return intervals

    def init_investing_mok_result(self):
        invest_cfg = InvestConfig()
        if os.path.exists(invest_cfg.searched_file_path):
            copyfile(invest_cfg.searched_file_path, f"{invest_cfg.searched_file_path}.bak")
            os.remove(invest_cfg.searched_file_path)
        if os.path.exists(invest_cfg.best_file_path):
            copyfile(invest_cfg.best_file_path, f"{invest_cfg.best_file_path}.bak")
            os.remove(invest_cfg.best_file_path)
        dir_path = os.path.join(self.INVEST_PATH, "details")
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            os.remove(file_path)

    @staticmethod
    def get_first_auto_params() -> dict:
        invest_cfg = InvestConfig()
        if os.path.exists(invest_cfg.searched_file_path):
            searched_data = pd.read_csv(invest_cfg.searched_file_path)
            if len(searched_data.index) > 0:
                searched_first = searched_data.iloc[0]
                hyper_params = searched_first.astype(int).to_dict()
                if 'mean_value' in hyper_params:
                    del hyper_params['mean_value']
                return hyper_params

        hyper_params = {"buy_min_ratio": 15,
                        "sell_min_ratio": 15,
                        "take_profit_ratio": 20,
                        "stop_loss_ratio": 10
                        }
        return hyper_params

    def search_auto_investing_mock_all_param(self, hyper_params, param_key, interval, idx, max_value, **params):
        original_value = hyper_params[param_key]
        original_cnt = 0
        arrow = random.sample([1, -1], 1)[0]
        while True:
            now_value = hyper_params[param_key]
            next_value = now_value + arrow * interval
            if original_value == next_value:
                hyper_params[param_key] = next_value
                original_cnt += 1
                if original_cnt == 2:
                    break
                else:
                    continue
            action, arrow = self.check_over_pace(now_value, next_value, original_value, arrow)
            if action == "continue":
                hyper_params[param_key] = next_value
                continue
            elif action == "break":
                break
            hyper_params[param_key] = next_value
            idx += 1
            print(f"search auto ({idx}) ... params: {hyper_params} ")
            mean_value = self.search_investing_mock(hyper_params, **params)
            if mean_value > max_value:
                max_value = mean_value
            else:
                arrow *= -1
                if abs(original_value - next_value) // interval > 1:
                    hyper_params[param_key] = now_value
                    break
        return idx, max_value

    @staticmethod
    def check_over_pace(now_value, next_value, original_value, arrow):
        over_pace = False
        action = ''
        if next_value < 0:
            over_pace = True
        if over_pace:
            if original_value == now_value:
                arrow *= -1
                action = "continue"
            else:
                action = "break"
        return action, arrow

    def search_random_investing_mock_all(self, param_grid, random_cnt: int = 10, **params):
        """
        전 주식을 대상으로 모의 투자를 실시하여 평균 값을 구한다.
        :return:
        """
        keys = param_grid.keys()
        randoms = self.get_random_products(param_grid, random_cnt)
        print(f"parameter values : {randoms}")
        for idx, instance in enumerate(randoms):
            grid_params = dict(zip(keys, instance))
            print(f"{idx + 1}/{random_cnt} search random ... params: {grid_params} ")
            self.search_investing_mock(grid_params, **params)

    @staticmethod
    def get_random_products(param_grid, random_cnt=100):
        values = param_grid.values()
        while True:
            total = 1
            for value in values:
                total = total * len(value)
            if total > random_cnt * 100:
                values_next = []
                for value in values:
                    values_next.append(random.sample(value, len(value) // 2 + 1))
                values = values_next
            else:
                break
        products = list(product(*values))
        randoms = random.sample(products, random_cnt)
        return randoms

    def invests_mock(self, corps: pd.DataFrame, **params):
        """
        전 주식을 대상으로 모의 투자를 실시한다.
        :param corps:
        :return:
        """
        result = []
        for index, row in tqdm(corps.iterrows(), total=len(corps.index)):
            # time.sleep(0.001)
            corp_code = row["종목코드"]
            corp_name = row["회사명"]
            try:
                predict_price, index_price, dates = self.invest_mock(corp_code, **params)
                result.append([corp_code, corp_name, predict_price, index_price, dates[0], dates[1]])
            except Exception as e:
                self.logger.info(e)
        data = pd.DataFrame(result, columns=["code", "name", "predict", "index", "start_date", "end_date"])
        data = data.sort_values(by=["predict"], ascending=False).reset_index(drop=True)
        return data

    def invests_best_mock(self, mock_period: int = 60, cnt_to_divide: int = 3, best_cnt: int = 10,
                          invest_price: int = 100000000, **params):
        """
        모의투자 상위 종목을 다시 모의투자를 실시한다.
        :param mock_period:
        :param cnt_to_divide:
        :param best_cnt:
        :param invest_price:
        :return:
        """
        corp = CorpLoader()
        corps = corp.get_crops_confidence()
        period = mock_period // cnt_to_divide
        for i in range(cnt_to_divide):
            cnt_to_del = (cnt_to_divide - i) * period
            data = self.invests_mock(corps, mock_period=period, **params)
            data = data.sort_values(by=["predict"], ascending=False).reset_index(drop=True)
            tops_data = data[0:best_cnt]
            top_corps = corps[corps['종목코드'].isin(tops_data.code)]
            cnt_to_del -= period
            data = self.invests_mock(top_corps, mock_period=period, mock_price=invest_price / best_cnt, **params)
            invest_price = sum(data['predict'])
        return invest_price

    def invest_mock(self, corp_code: str, mock_period=120, mock_price=10000000, **params):
        """
        모의 투자를 실시한다.
        :param corp_code:
        :param mock_period:
        :param mock_price:
        :return:
        """
        analyzer = DataAnalyzer()
        predict_data = analyzer.predict_period(corp_code, pred_days=mock_period, **params)
        last_close = None
        now_price = mock_price
        now_cnt = 0
        bought_price = 0
        for index, row in predict_data.iterrows():
            if index == 0:
                last_close = row['close']
                continue
            self.logger.debug(f"{row['date']}, now_price:{now_price}, now_cnt:{now_cnt}, last_close:{last_close}")
            now_price, now_cnt, bought_price = self.trade_by_prediction(now_price=now_price, now_cnt=now_cnt,
                                                                        last_close=last_close,
                                                                        bought_price=bought_price,
                                                                        today_data=row, **params)
            last_close = row['close']
        now_price, _ = self.sell_stock(now_price, now_cnt, last_close, **params)
        index_price = self.get_index_price(predict_data, mock_price)
        first_date = DateUtils.series_to_date(predict_data.head(1).date)
        end_date = DateUtils.series_to_date(predict_data.tail(1).date)
        return np.round(now_price), index_price, (first_date, end_date)

    @staticmethod
    def get_index_price(predict_data: pd.DataFrame, mock_price: int = 10000000):
        """
        지수 계산
        :param predict_data:
        :param mock_price:
        :return:
        """
        first_close = predict_data.head(1).close.values[0]
        end_close = predict_data.tail(1).close.values[0]
        index_price = end_close * mock_price / first_close
        return np.round(index_price)

    def trade_by_prediction(self, now_price: int, now_cnt: int, bought_price: int, **params):
        """
        예측 값으로 모의 투자를 실시한다.
        :param now_price: 현재 잔고 금액
        :param now_cnt: 주식 개수
        :param bought_price: 구매한 가격
        :return:
        """
        now_price, now_cnt, bought_price = self.trade_first(now_price=now_price, now_cnt=now_cnt,
                                                            bought_price=bought_price, **params)
        now_price, now_cnt = self.trade_second(now_price=now_price, now_cnt=now_cnt, bought_price=bought_price,
                                               **params)
        return now_price, now_cnt, bought_price

    def trade_first(self, last_close: int, today_data: pd.Series, now_price: int, now_cnt: int, bought_price: int,
                    buy_min_ratio=1.2, sell_min_ratio=1.2, **params):
        """
        예측 값에 의한 최초 매매
        """
        predict = today_data['predict']
        if last_close < predict and now_cnt == 0 and buy_min_ratio != 0:
            pred_ratio = (predict - last_close) / last_close
            if pred_ratio > buy_min_ratio / 100:
                self.logger.debug(f"predict:{predict}, buy_min_ratio:{buy_min_ratio}")
                now_price, now_cnt, bought_price = self.buy_stock(now_price, now_cnt, last_close,
                                                                  bought_price=bought_price, **params)
        elif last_close > predict and now_cnt > 0 and sell_min_ratio != 0:
            pred_ratio = (last_close - predict) / last_close
            if pred_ratio > sell_min_ratio / 100:
                self.logger.debug(f"predict:{predict}, sell_min_ratio:{sell_min_ratio}")
                now_price, now_cnt = self.sell_stock(now_price, now_cnt, last_close, **params)
        return now_price, now_cnt, bought_price

    def trade_second(self, today_data: pd.Series, now_price: int, now_cnt: int, bought_price: int, take_profit_ratio=0,
                     stop_loss_ratio=0, **params):
        """
        예측 값에 의한 장중에 매매
        """
        high = today_data['high']
        low = today_data['low']
        if high != 0 and low != 0 and now_cnt != 0:
            trade_price = 0
            trade_price = self.trade_stop_loss(trade_price, stop_loss_ratio, bought_price, low)
            trade_price = self.trade_take_profit(trade_price, take_profit_ratio, bought_price, high)
            if trade_price != 0:
                now_price, now_cnt = self.sell_stock(now_price, now_cnt, trade_price, **params)
        return now_price, now_cnt

    def trade_take_profit(self, trade_price, take_profit_ratio, bought_price, high):
        if take_profit_ratio != 0 and trade_price == 0:
            take_profit = bought_price * (1 + take_profit_ratio / 100)
            if high >= take_profit:
                self.logger.debug(f"take_profit_ratio:{take_profit_ratio}, take_profit:{take_profit}")
                trade_price = take_profit
        return trade_price

    def trade_preserve_profit(self, trade_price, preserve_profit_ratio, bought_price, last_close, low):
        if preserve_profit_ratio != 0 and trade_price == 0:
            take_profit = bought_price * (1 + preserve_profit_ratio / 100)
            if low <= take_profit <= last_close:
                self.logger.debug(f"take_profit_ratio:{preserve_profit_ratio}, take_profit:{take_profit}")
                trade_price = take_profit
        return trade_price

    def trade_take_profit_day(self, trade_price, take_profit_day_ratio, last_close, high):
        if take_profit_day_ratio != 0 and trade_price == 0:
            take_profit = last_close * (1 + take_profit_day_ratio / 100)
            if high >= take_profit:
                self.logger.debug(f"take_profit_day_ratio:{take_profit_day_ratio}, take_profit:{take_profit}")
                trade_price = take_profit
        return trade_price

    def trade_take_profit_4pred(self, trade_price, take_profit_pred_ratio, last_close, predict, high, bought_price):
        if take_profit_pred_ratio != 0 and predict > last_close >= bought_price and trade_price == 0:
            take_profit = predict * (1 + take_profit_pred_ratio / 100)
            if high >= take_profit:
                self.logger.debug(f"take_profit_pred_ratio:{take_profit_pred_ratio}, take_profit:{take_profit}")
                trade_price = take_profit
        return trade_price

    def trade_stop_loss(self, trade_price, stop_loss_ratio, bought_price, low):
        if trade_price == 0 and stop_loss_ratio != 0:
            stop_loss = bought_price * (1 - stop_loss_ratio / 100)
            if low <= stop_loss:
                self.logger.debug(f"stop_loss_ratio:{stop_loss_ratio}, stop_loss:{stop_loss}")
                trade_price = stop_loss
        return trade_price

    def trade_stop_loss_day(self, trade_price, stop_loss_day_ratio, last_close, low):
        if stop_loss_day_ratio != 0 and trade_price == 0:
            stop_loss = last_close * (1 - stop_loss_day_ratio / 100)
            if low <= stop_loss:
                self.logger.debug(f"stop_loss_day_ratio:{stop_loss_day_ratio}, stop_loss:{stop_loss}")
                trade_price = stop_loss
        return trade_price

    def sell_stock(self, now_price, now_cnt, sell_price, trance_fee_ratio=0.015, tax_fee_ratio=0.3,
                   **params):
        """
        주식을 판매할 때 발생하는 금액
        :param now_price: 현재 금액
        :param now_cnt:
        :param sell_price:
        :param trance_fee_ratio:
        :param tax_fee_ratio:
        :return:
        """
        if now_cnt > 0:
            now_price += now_cnt * sell_price * (1 - tax_fee_ratio / 100 - trance_fee_ratio / 100)
            self.logger.info(f"sell_price={sell_price}, sell_cnt={now_cnt}, now_price={now_price}")
        return now_price, 0

    def buy_stock(self, now_price, now_cnt, buy_price, bought_price, trance_fee_ratio=0.015, **params):
        """
        주식을 구매할 때 발생하는 금액
        :param now_price:
        :param now_cnt:
        :param buy_price:
        :param trance_fee_ratio:
        :param bought_price: 구매한 금액
        :return:
        """
        buy_cnt = now_price // (buy_price * (1 + trance_fee_ratio / 100))
        if buy_cnt > 0:
            now_cnt += buy_cnt
            now_price -= buy_cnt * buy_price * (1 + trance_fee_ratio / 100)
            bought_price = buy_price
            self.logger.info(f"buy_price={buy_price}, buy_cnt={buy_cnt}, now_price={now_price}")
        return now_price, now_cnt, bought_price
