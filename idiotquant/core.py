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
		print("stock score : " + str(stock.getScore(None)))
		print("stock rank : " + str(stock.getRank(None, None, None)))
		# print("stock 시가총액 : " + stock.getMarketCapital())
		# print("stock per : " + stock.getPER())
		# print("stock pbr : " + stock.getPBR())
		# print("stock pbr*per : " + str(float(stock.getPBR()) * float(stock.getPER())))
		
	print(len(io.stockList))


