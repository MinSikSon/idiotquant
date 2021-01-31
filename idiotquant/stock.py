# -*- coding: utf-8 -*-
'''
	Stock class
	
	주식 종목을 나타내는 객체입니다. 
 
'''
class Stock:
	INVALID_VALUE = 0xFFFFFFFF
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


	# def getClose(self, index):
	def getStockName(self):
		return self.json['종목명']

	def getClose(self):
		return self.json['종가']

	def getMarketCapital(self):
		try:
			return self.json['시가총액']
		except KeyError:
			return str(0)

	def getTradingValue(self):
		# TODO 거래대금
		pass

	def getFundamentalTotalAsset(self):
		return self.json['자산총계']

	def getFundamentalCurrentAsset(self):
		try:
			if self.json['유동자산'] is '-':
				return str(0)
			else:
				return self.json['유동자산']
		except KeyError:
			return str(0)

	def getFundamentalTotalLiability(self):
		try:
			return self.json['부채총계']
		except KeyError:
			return str(self.INVALID_VALUE)

	def getFundamentalTotalEquity(self):
		return self.json['자산총계']

	def getFundamentalRevenue(self):
		try:
			if self.json['매출액'] is '-':
				return str(0)
			else:
				return self.json['매출액']
		except KeyError:
			return str(0)
	def getPER(self):
		try:
			return self.json['PER']
		except KeyError:
			return str(self.INVALID_VALUE)

	def getPBR(self):
		return self.json['PBR']

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


