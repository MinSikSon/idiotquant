# -*- coding: utf-8 -*-
'''
	CustomFunction class

	User need to change only this part
'''
class CustomFunction:

	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95;     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 20;       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == 'None' or stock.getPER() == '0.0':
			return False
		if float(stock.getPER()) > 3.0:
			return False
		return True

	def stockPortfolioBuilder(self, stockList):
		return sorted(stockList, key=lambda x: float(x.getPER()), reverse=False)
		# return None