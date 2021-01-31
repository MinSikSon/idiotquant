# -*- coding: utf-8 -*-
from idiotquant.basket import Basket
'''
	IdiotQuant class
	
	IdiotQuant Main class 
'''
class IdiotQuant:

	def __init__(self, stockList, customFunction):
		self.stockList = stockList
		self.customFunction = customFunction
		self.stockNum = customFunction.stockNum
		self.stockWeight = customFunction.stockWeight

	def initialize(self):
		self.stockBasket = Basket(None, self.stockNum, None);

		# 주식 포트폴리오 구성 함수를 지정합니다.
		# self.stockBasket.setPortfolioBuilder(stockPortfolioBuilder);

	def stockFilter(self):
		for stock in self.stockList[:]:
			if not self.customFunction.stockFilter(stock):
				self.stockList.remove(stock)


	def stockPortfolioBuilder(self):
		self.stockList = self.customFunction.stockPortfolioBuilder(self.stockList)
		self.stockList = self.stockList[0:self.stockNum]