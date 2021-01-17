# [REF]
# https://wikidocs.net/47449
# [API]
# https://github.com/sharebook-kr/pykrx
# [Terms]
# OHLC: Open High Low Close: 시가, 최고가, 최저가, 종가

from pykrx import stock
import datetime
import json

import os
import pickle

class Krx:
    dirMarketFundamental = os.path.dirname(os.path.abspath(__file__)) + '/data/marketfundamental'
    dirMarketOhlcv = os.path.dirname(os.path.abspath(__file__)) + '/data/marketohlcv'

    def __init__(self):
        pass

    def getMarketOhlcvByTicker(self, date=None, market="ALL"):
        """티커로 ohlcv 조회 (ohlcv: open, high, low, close, volume)
        :param date: 조회 일자 (YYYYMMDD)
        :param market: 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        :return: market 내의 모든 종목의 ohlcv
        """
        if date == None:
            return None

        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.dirMarketOhlcv):
            os.makedirs(self.dirMarketOhlcv)
        # print(path)
        filePath = self.dirMarketOhlcv + '/marketOhlcv_%s_%s.bin' % (market, date)
        # print(filePath)
        if os.path.isfile(filePath):
            # NOTE: file 이 있고, corpName 에 해당하는 데이터 있는지 확인.
            with open(filePath, 'rb') as f:
                marketOhlcv = pickle.load(f)
                return marketOhlcv

        rawOhlcvList = stock.get_market_ohlcv_by_ticker(date, market)
        
        # NOTE: rawOhlcvList 데이터는 pandas.DataFrame 인데, DaraFrame 전체가 empty 면 rawOhlcvList.empty 는 True 를 리턴 함.
        # reref] https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.empty.html
        if rawOhlcvList.empty == True:
            return None

        resOhlcv = dict()
        corpName = rawOhlcvList.columns[0]
        for i in rawOhlcvList.index:
            tmpDict = dict()
            for j in range(1, len(rawOhlcvList.columns)):
                tmpDict[rawOhlcvList.columns[j]] = str(rawOhlcvList.loc[i][rawOhlcvList.columns[j]])

            resOhlcv[rawOhlcvList.loc[i][corpName]]= tmpDict

        # NOTE: 데이터 백업.
        with open(filePath, 'wb') as f:
            pickle.dump(resOhlcv, f)

        return resOhlcv

    def getMarketFundamentalByTicker(self, date=None, market="ALL"):
        """티커로 Fundamental(DIV, BPS, PER, EPS, PBR)
        :param date: 조회 일자 (YYYYMMDD)
        :param market: 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        :return: market 내의 모든 종목의 Fundamental
        """
        if date == None:
            return None

        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.dirMarketFundamental):
            os.makedirs(self.dirMarketFundamental)
        # print(path)
        filePath = self.dirMarketFundamental + '/marketFundamental_%s_%s.bin' % (market, date)
        # print(filePath)
        if os.path.isfile(filePath):
            # NOTE: file 이 있고, corpName 에 해당하는 데이터 있는지 확인.
            with open(filePath, 'rb') as f:
                marketFundamental = pickle.load(f)
                return marketFundamental

        rawFundamentalList = stock.get_market_fundamental_by_ticker(date, market) # pandas form
        if rawFundamentalList.empty == True:
            print("[WARN] please check parameter `date`")
            return None

        resFundamental = {}
        corpName = rawFundamentalList.columns[0]
        for i in rawFundamentalList.index:
            tmpDict = dict()
            for j in range(1, len(rawFundamentalList.columns)):
                tmpDict[rawFundamentalList.columns[j]] = str(rawFundamentalList.loc[i][rawFundamentalList.columns[j]])

            resFundamental[rawFundamentalList.loc[i][corpName]]= tmpDict

        # NOTE: 데이터 백업.
        with open(filePath, 'wb') as f:
            pickle.dump(resFundamental, f)

        # return json.dumps(resFundamental, ensure_ascii=False, indent="\t") # dict to json
        return resFundamental