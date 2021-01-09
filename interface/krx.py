# [REF]
# https://wikidocs.net/47449
# [API]
# https://github.com/sharebook-kr/pykrx
# [Terms]
# OHLC: Open High Low Close: 시가, 최고가, 최저가, 종가

from pykrx import stock
import datetime
import json

class Krx:
    def __init__(self):
        pass

    def getMarketOhlcvByTicker(self, date=None, market="ALL"):
        """티커로 ohlcv 조회 (ohlcv: open, high, low, close, volume)
        :param date: 조회 일자 (YYYYMMDD)
        :param market: 조회 시장 (KOSPI/KOSDAQ/KONEX/ALL)
        :return: ?
        """
        if date == None:
            return None
        rawOhlcvList = stock.get_market_ohlcv_by_ticker(date, market)
        if rawOhlcvList.empty == True:
            return None

        resOhlcv = {}
        종목명 = rawOhlcvList.columns[0]
        for i in rawOhlcvList.index:
            tmpDict = dict()
            for j in range(1, len(rawOhlcvList.columns)):
                tmpDict[rawOhlcvList.columns[j]] = str(rawOhlcvList.loc[i][rawOhlcvList.columns[j]])

            resOhlcv[rawOhlcvList.loc[i][종목명]]= tmpDict

        # return json.dumps(resOhlcv, ensure_ascii=False, indent="\t") # dict to json
        return resOhlcv


    def getMarketFundamentalByTicker(self, date=None, market="ALL"):
        if date == None:
            return None

        rawFundamentalList = stock.get_market_fundamental_by_ticker(date, market) # pandas form
        if rawFundamentalList.empty == True:
            print("[WARN] please check parameter `date`")
            return None

        resFundamental = {}
        종목명 = rawFundamentalList.columns[0]
        for i in rawFundamentalList.index:
            tmpDict = dict()
            for j in range(1, len(rawFundamentalList.columns)):
                tmpDict[rawFundamentalList.columns[j]] = str(rawFundamentalList.loc[i][rawFundamentalList.columns[j]])

            resFundamental[rawFundamentalList.loc[i][종목명]]= tmpDict

        # return json.dumps(resFundamental, ensure_ascii=False, indent="\t") # dict to json
        return resFundamental