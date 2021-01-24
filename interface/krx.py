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

from interface.corpcode import CorpCode

class Krx:
    dirMarketFundamental = os.path.dirname(os.path.abspath(__file__)) + '/data/marketfundamental'
    dirMarketOhlcv = os.path.dirname(os.path.abspath(__file__)) + '/data/marketohlcv'
    dirMarket = os.path.dirname(os.path.abspath(__file__)) + '/data/market'
    dirMarketCap = os.path.dirname(os.path.abspath(__file__)) + '/data/marketcap'
    def __init__(self):
        pass

    def getMarketOhlcvByTicker(self, date=None, market="ALL"):
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

        rawOhlcvList = None
        try:
            rawOhlcvList = stock.get_market_ohlcv_by_ticker(date, market)
        except:
            print("[param] date 를 확인해주세요.")
            print("[위 사항이 아니라면] [KRX API update 가 필요합니다] stock.get_market_ohlcv_by_ticker")
            exit()

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

        rawFundamentalList = None
        try:
            rawFundamentalList = stock.get_market_fundamental_by_ticker(date, market) # pandas form
        except:
            print("[KRX API update 가 필요합니다] stock.get_market_fundamental_by_ticker")
            exit()

        if rawFundamentalList.empty == True:
            print("[WARN] please check parameter `date`")
            return None

        resFundamental = dict()
        corpName = rawFundamentalList.columns[0]
        for i in rawFundamentalList.index:
            tmpDict = dict()
            for j in range(1, len(rawFundamentalList.columns)):
                tmpDict[rawFundamentalList.columns[j]] = str(rawFundamentalList.loc[i][rawFundamentalList.columns[j]]).replace(" ", "")

            resFundamental[str(rawFundamentalList.loc[i][corpName]).replace(" ", "")] = tmpDict

        # NOTE: 데이터 백업.
        with open(filePath, 'wb') as f:
            pickle.dump(resFundamental, f)

        # return json.dumps(resFundamental, ensure_ascii=False, indent="\t") # dict to json
        return resFundamental

    def getMarketCapByTicker(self, date=None, market="ALL"):
        if date is None:
            return None
        if not os.path.isdir(self.dirMarketCap):
            os.makedirs(self.dirMarketCap)
        filePath = self.dirMarketCap + '/' + 'marketCap_%s_%s.bin' % (market, date)
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                marketCap = pickle.load(f)
                return marketCap

        rawMarketCap = None
        try:
            rawMarketCap = stock.get_market_cap_by_ticker(date, market) # pandas form
        except:
            print("[KRX API update 가 필요합니다] stock.get_market_cap_by_ticker")
            exit()

        if rawMarketCap.empty == True:
            print("[WARN] please check parameter `date`")
            return None

        resMarketCap = dict()
        for ticker in rawMarketCap.index:
            tmpDict = dict()
            종목명 = stock.get_market_ticker_name(ticker)
            tmpDict["종목명"] = 종목명
            for column in rawMarketCap.columns: # 종가, 시가총액, 거래량, 시가총액, 상장주식수
                tmpDict[column] = str(rawMarketCap.loc[ticker][column]).replace(" ", "")

            resMarketCap[종목명] = tmpDict

        # NOTE: 데이터 백업.
        with open(filePath, 'wb') as f:
            pickle.dump(resMarketCap, f)

        return resMarketCap

    def getMarketValue(self, date=None, market="ALL"):
        if date is None:
            return None

        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.dirMarket):
            os.makedirs(self.dirMarket)
        # print(path)
        filePath = self.dirMarket + '/' + 'market_%s_%s.bin' % (market, date)
        # print(filePath)
        if os.path.isfile(filePath):
            # NOTE: file 이 있고, corpName 에 해당하는 데이터 있는지 확인.
            with open(filePath, 'rb') as f:
                marketValue = pickle.load(f)
                return marketValue

        marketOhlcv = self.getMarketOhlcvByTicker(date, market)
        if marketOhlcv is None:
            return None
        marketFundamental = self.getMarketFundamentalByTicker(date, market)
        if marketFundamental is None:
            return None

        corpCode = CorpCode()
        corpList = corpCode.getAllCorpCode()

        resData = {"date": date, "finish": False, "market": market, "data_info": {"ohlcv": True, "fundamental": True}}

        mergedDict = dict()
        for i in range(0, len(corpList)):
            corpName = corpList[i].findtext("corp_name")
            try:
                mergedDict[corpName] = marketOhlcv[corpName]
                mergedDict[corpName].update(marketFundamental[corpName])
                mergedDict[corpName]["종목명"] = corpName
            except KeyError:
                continue
        resData["data"] = mergedDict

        resData["finish"] = True

        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.dirMarket):
            os.makedirs(self.dirMarket)

        filePath = self.dirMarket + '/' + 'market_%s_%s.bin' % (market, date)
        with open(filePath, 'wb') as f:
            pickle.dump(resData, f)

        return resData