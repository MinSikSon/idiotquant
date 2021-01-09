# -*- coding: utf-8 -*-
class Stock:
	#code
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
		self.name = json['종목명']
		# TODO 기준가 = 전일종가
		self.bestPrice = json['종가']
		# TODO 구분 코드 입니다. 1:대형, 2:중형, 4:소형, 8:Kospi200 (비트연산 허용. 예. 9: 대형 & Kospi200)
		# self.capLevel = json['종가']
		# TODO KRX에서 제공하는 업종코드입니다.
		# self.sector = json['업종코드']


	# def getClose(self, index):
	def getClose(self):
		return self.json['종가']

	def getMarketCapital(self):
		return self.json['시가총액']

	def getTradingValue(self):
		# TODO 거래대금
		return None

	def getFundamentalTotalAsset(self):
		return self.json['자산총계']

	def getFundamentalCurrentAsset(self):
		return self.json['유동자산']

	def getFundamentalTotalLiability(self):
		return self.json['부채총계']

	def getFundamentalTotalEquity(self):
		return self.json['자산총계']

	def getFundamentalRevenue(self):
		return self.json['매출액']

	def getFundamentalSalesCost(self):
		# TODO 매출원가
		return None

	def setScore(self, key, value):
		# TODO set score
		return None

	def getScore(self, key):
		# TODO get score
		return None

	# Order is optional
	def getRank(universe, key, order):
		# TODO order by score
		return None



