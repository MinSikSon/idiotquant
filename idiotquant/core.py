# -*- coding: utf-8 -*-
import json
from idiotquant.stock import Stock
from idiotquant.idiot_quant import IdiotQuant
from idiotquant.custom_function import CustomFunction, CustomFunction_2

def main():
	stockList = []

	with open('data/latest.json') as f:
		d = json.load(f)

		# for item in d['list']:
		print(len(d['data']))
		for item in d['data']:
			# print(item, d['data'][item])
			stock = Stock(d['data'][item])
			stockList.append(stock)

		iq = IdiotQuant(stockList, CustomFunction_2())
		iq.initialize()
		iq.stockFilter()
		iq.stockPortfolioBuilder()

		print("-----------------------------------")
		for stock in iq.stockList:
			print("stock name : " + stock.name)
			# print("stock close : " + stock.getClose())
			# print("stock per : " + stock.getPER())
			print("stock 매출액 : ", stock.getFundamentalRevenue(), ", per: ", stock.getPER())
		print(len(iq.stockList))

		with open('result/result.json', 'w') as fp:
			# pickle.dump(len(data), fp)
			for stock in iq.stockList:
				json.dump(stock.__dict__, fp, ensure_ascii=False, indent=4)


