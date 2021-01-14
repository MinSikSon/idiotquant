# -*- coding: utf-8 -*-
import json
from stock import Stock
from idiot_quant import IdiotQuant
from custom_function import CustomFunction

stockList = []  

with open('sample/202101072325_NCAV.json') as f:
	d = json.load(f)

	for item in d['list']:
		stock = Stock(item)
		stockList.append(stock) 

	iq = IdiotQuant(stockList, CustomFunction())
	iq.initialize()
	iq.stockFilter()	
	iq.stockPortfolioBuilder()

	print("-----------------------------------")
	for stock in iq.stockList:
		print("stock name : " + stock.name)
		# print("stock close : " + stock.getClose())
		print("stock per : " + stock.getPER())
	print(len(iq.stockList))

	with open('result/result.json', 'w') as fp:
		# pickle.dump(len(data), fp)
	    for stock in iq.stockList:
	        json.dump(stock.__dict__, fp, ensure_ascii=False, indent=4)


