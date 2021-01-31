# -*- coding: utf-8 -*-
import json
from idiotquant.stock import Stock
from idiotquant.idiot_quant import IdiotQuant
from idiotquant.custom_function import *

def main(strategy=1):
	stockList = []

	with open('data/latest.json') as f:
		d = json.load(f)

		# for item in d['list']:
		print(len(d['data']))
		for item in d['data']:
			# print(item, d['data'][item])
			stock = Stock(d['data'][item])
			stockList.append(stock)
		if strategy == 1:
			customFunction = CustomFunction__NCAV_strategy
		elif strategy == 2:
			customFunction = CustomFunction__sample
		else:
			customFunction = CustomFunction__NCAV_strategy
		iq = IdiotQuant(stockList, customFunction())
		iq.initialize()
		iq.stockFilter()
		iq.stockPortfolioBuilder()

		print("-----------------------------------")
		for stock in iq.stockList:
			print(stock.name, ") 종가:", format(int(stock.getClose()), ','), 
			"| PER:", stock.getPER(), 
			"| 매출액:", format(int(stock.getFundamentalRevenue()), ','),
			"| 당기순이익:", format(int(stock.getFundamentalNetProfit()), ',')
			)
		print(len(iq.stockList))

		with open('result/result.json', 'w') as fp:
			# pickle.dump(len(data), fp)
			for stock in iq.stockList:
				json.dump(stock.__dict__, fp, ensure_ascii=False, indent=4)


