# -*- coding: utf-8 -*-
'''
	CustomFunction class

	User need to change only this part
'''
class CustomFunction:

	# stockBasket;     # 주식 종목들을 관리하는 Basket 객체
	stockWeight = .95;     # 주식 비중
	#나머지 5% 현금 보유 (수수료, 세금 등 거래비용 고려)
	stockNum = 30;       # 주식 종목 수

	'''
		main fuction
	'''
	def stockFilter(self, stock):
		# if stock.getPER() == 'None' or stock.getPER() == '0.0':
		# 	return False
		# if float(stock.getPER()) > 3.0:
		# 	return False

		# TODO stock.capLevel isn't implemented yet
		# filterSmallMarketCaptial = (stock.capLevel == 4);
		filterSmallMarketCaptial = True
		filterMarketCapital = (int(stock.getMarketCapital()) < 200000000000);   # 시가총액 2000억 이하 기준
		#filterTradingValue = (stock.getTradingValue() > 100);     # 일거래대금 1억 이상 기준
		if stock.getPER() == 'None' or stock.getPER() == '0.0':
			return False

		filterPBR = ((stock.getPBR() == 'None' or stock.getPBR() == '0.0') or float(stock.getPBR()) > 0.0);                            
		# GPA 값이 마이너스인 경우 제외
		# TODO stock.getFundamentalSalesCost isn't implemented yet
		# filterGPA = (self.getGPA(stock) > 0)     
		filterGPA = True         
			
		return (filterPBR and filterGPA and filterSmallMarketCaptial and filterMarketCapital) 

	def stockPortfolioBuilder(self, stockList):

		sortedList = []

		perSorted = sorted(stockList, key=lambda x: float(x.getPER()), reverse=False)
		pbrSorted = sorted(stockList, key=lambda x: float(x.getPBR()), reverse=False)

		sortedList.append(perSorted) 
		sortedList.append(pbrSorted) 

		self.calculateRank(sortedList, stockList)

		# return None
		return sorted(stockList, key=lambda x: int(x.getScore(None)), reverse=False)
	

	'''
		custom private fuction
	'''
	# GP/A (매출총이익/총자산) 매출총이익(매출액- 매출원가) 팩터 정의
	def getGPA(stock):
		# 해당 종목의 종가 또는 당기순이익이 0인 경우에는 제외합니다.
		if stock.getClose() == 0 or stock.getFundamentalTotalAsset() == 0:
		    return -1;

		#stock.getFundamentalRevenue();  //현재분기 매출액을
		#stock.getFundamentalSalesCost();  //현재분기 매출원가를
		#stock.getFundamentalTotalAsset();  //현재분기 자산총계를

		# 매출 총이익
		fundamentalProfit = stock.getFundamentalRevenue() - stock.getFundamentalSalesCost()

		# 주가수익비율을 계산한 결과를 getPER(stock) 함수를 호출한 곳으로 넘겨줍니다.
		return fundamentalProfit / stock.getFundamentalTotalAsset()

	def calculateRank(self, universe, stockList):
		rankDic = {}
		
		for universeItem in universe:
			for idx, universeItemItem in enumerate(universeItem):
				if universeItemItem in rankDic.keys():
					rankDic[universeItemItem] += idx
				else:
					rankDic[universeItemItem] = idx

		rankDic = dict(sorted(rankDic.items(), key=lambda item: item[1]))

		rank = 0
		for key in rankDic:
			print(key.name, '->', rankDic[key])
			key.setScore(None, rankDic[key])
			rank += 1
			key.setRank(rank)

		# for stock in stockList:
		# 	stock.setScore(None, rankDic[stock])

		# rank dic key to list
		# return [*rank]
