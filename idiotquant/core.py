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

	io = IdiotQuant(stockList, CustomFunction())
	io.initialize()
	io.stockFilter()	
	io.stockPortfolioBuilder()

	print("-----------------------------------")
	for stock in io.stockList:
		print("stock name : " + stock.name)
		# print("stock close : " + stock.getClose())
		print("stock per : " + stock.getPER())
	print(len(io.stockList))


