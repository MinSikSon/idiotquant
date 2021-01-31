# -*- coding: utf-8 -*-
'''
	CustomFunction class

	User need to change only this part
'''
from abc import *

class AbstractCustomFunction(metaclass=ABCMeta):
	@abstractmethod
	def stockFilter(self, stock):
		pass
	@abstractmethod
	def stockPortfolioBuilder(self, stockList):
		pass

class CustomFunction__sample(AbstractCustomFunction):

	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == 'None' or stock.getPER() == '0.0':
			return False
		if float(stock.getPER()) > 3.0:
			return False
		return True

	def stockPortfolioBuilder(self, stockList):
		return sorted(stockList, key=lambda x: float(x.getPER()), reverse=False)
		# return None

class CustomFunction__NCAV_strategy(AbstractCustomFunction):
	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == 'None' or stock.getPER() == '0.0': return False
		if float(stock.getPER()) > 15.0: return False

		if float(stock.getPER()) == 0xFFFFFFFF: return False

		if float(stock.getFundamentalNetProfit()) < 0: return False

		filter0 = float(stock.getFundamentalCurrentAsset()) - float(stock.getFundamentalTotalLiability()) > float(stock.getMarketCapital())

		return filter0

	def stockPortfolioBuilder(self, stockList):
		# return sorted(stockList, key=lambda x: float(x.getPER()), reverse=False)
		return sorted(stockList, key=lambda x: int(x.getFundamentalCurrentAsset()), reverse=True)
		# return None