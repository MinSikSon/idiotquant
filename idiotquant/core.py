# -*- coding: utf-8 -*-
import json
from stock import *

stockList = []  

with open('sample/202101072325_NCAV.json') as f:
    d = json.load(f)
    for item in d['list']:
    	stock = Stock(item);
    	print(stock.getClose())
    	stockList.append(stock) 