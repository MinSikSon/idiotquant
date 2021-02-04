# -*- coding: utf-8 -*-
'''
	CustomFunction class

	User need to change only this part
'''

class AbstractCustomFunction():
	def stockFilter(self, stock):
		raise NotImplementedError
	def stockPortfolioBuilder(self, stockList):
		raise NotImplementedError

class CustomFunction__sample(AbstractCustomFunction):
	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == None or stock.getPER() == 0:
			return False
		if stock.getPER() > 3.0:
			return False

		return True

	def stockPortfolioBuilder(self, stockList):
		return sorted(stockList, key=lambda x: x.getPER(), reverse=False)
		# return None

class CustomFunction__NCAV_strategy(AbstractCustomFunction):
	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == None or stock.getPER() == 0: return False
		if stock.getPER() > 15.0: return False
		if stock.getPER() == stock.INVALID_VALUE: return False
		# 당기순이익 > 0
		if stock.getFundamentalNetProfit() < 0: return False
		# 유동자산 - 총부채 > 시가총액
		filter0 = (stock.getFundamentalCurrentAsset() - stock.getFundamentalTotalLiability()) > stock.getMarketCapital()

		return filter0

	def stockPortfolioBuilder(self, stockList):
		# 유동자산 기준으로 정렬
		return sorted(stockList, key=lambda x: int(x.getFundamentalCurrentAsset()), reverse=True)

class CustomFunction__sample2(AbstractCustomFunction):
	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30       # 주식 종목 수

	def stockFilter(self, stock):
		if stock.getPER() == None or stock.getPER() == 0: return False
		# 거래량 90000 이상
		if float(stock.getTradingVolume()) < 90000: return False
		# 시가 대비 종가 10% 상승
		if (float(stock.getClose()) - float(stock.getOpen())) / float(stock.getOpen()) < 0.1: return False
		# PER 10 이상
		if (float(stock.getPER())) > 10: return False

		return True

	def stockPortfolioBuilder(self, stockList):
		# 거래량 기준으로 정렬
		return sorted(stockList, key=lambda x: int(x.getTradingVolume()), reverse=True)

# NOTE: CustomFunction_x 생성 이후 아래 List 에 추가해주세요.
customFunction = [
		CustomFunction__sample,
		CustomFunction__NCAV_strategy,
		CustomFunction__sample2
	]