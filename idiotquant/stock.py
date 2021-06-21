# -*- coding: utf-8 -*-
'''
	Stock class
	
	주식 종목을 나타내는 객체입니다. 
'''


class Stock:
    INVALID_VALUE = 0xFFFFFFFFFFFFFFFF
    # code
    # name
    # isETF
    # market
    # manage
    # bestPrice
    # capLevel
    # sector
    # json

    def __init__(self, json):
        self.json = json
        # TODO 종목 코드가 필요함
        # self.code = json['종목코드']
        # print('json: ', json['종목명'])
        self.name = json['종목명']
        # TODO 기준가 = 전일종가
        self.bestPrice = json['종가']
        # TODO 구분 코드 입니다. 1:대형, 2:중형, 4:소형, 8:Kospi200 (비트연산 허용. 예. 9: 대형 & Kospi200)
        # self.capLevel = json['종가']
        # TODO KRX에서 제공하는 업종코드입니다.
        # self.sector = json['업종코드']

    def getFundamentalSalesCost(self):
        # TODO 매출원가
        pass

    def setScore(self, key, value):
        self.score = value

    def getScore(self, key):
        return self.score

    def setRank(self, rank):
        self.rank = rank

    # TODO we need to implement order
    # Order is optional
    def getRank(self, universe, key, order):
        return self.rank

    def getOpen(self):
        try:
            return float(self.json['시가'])
        except KeyError:
            return float(0)

    def getHigh(self):
        try:
            return float(self.json['고가'])
        except KeyError:
            return float(0)

    def getLow(self):
        try:
            return float(self.json['저가'])
        except KeyError:
            return float(0)

    def getClose(self):
        try:
            return float(self.json['종가'])
        except KeyError:
            return float(0)

    def getTradingVolume(self):
        try:
            return float(self.json['거래량'])
        except KeyError:
            return float(0)

    def getMarketCapital(self):
        try:
            return float(self.json['시가총액'])
        except KeyError:
            return float(0)

    def getTradingValue(self):
        try:
            return float(self.json['거래대금'])
        except KeyError:
            return float(0)

    def getFundamentalTotalAsset(self):
        try:
            return float(self.json['자산총계'])
        except KeyError:
            return float(0)

    def getFundamentalCurrentAsset(self):
        try:
            if self.json['유동자산'] == '-':
                return float(0)
            else:
                return float(self.json['유동자산'])
        except KeyError:
            return float(0)

    def getFundamentalTotalLiability(self):
        try:
            return float(self.json['부채총계'])
        except KeyError:
            return float(self.INVALID_VALUE)

    def getFundamentalTotalEquity(self):
        try:
            return float(self.json['자본총계'])
        except KeyError:
            return float(0)

    def getFundamentalRevenue(self):
        try:
            if self.json['매출액'] == '-':
                return float(0)
            else:
                return float(self.json['매출액'])
        except KeyError:
            return float(0)

    def getPER(self):
        try:
            return float(self.json['PER'])
        except KeyError:
            return float(self.INVALID_VALUE)

    def getPBR(self):
        try:
            return float(self.json['PBR'])
        except KeyError:
            return float(self.INVALID_VALUE)

    def getFundamentalNetProfit(self):
        try:
            return float(self.json['당기순이익'])
        except KeyError:
            return float(0)

    def getEPS(self):
        try:
            return float(self.json['EPS'])
        except KeyError:
            return float(0)

    def getOperatingIncome(self):
        try:
            return float(self.json['영업이익'])
        except KeyError:
            return float(0)
