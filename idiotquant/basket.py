# -*- coding: utf-8 -*-
'''
	Basket class
	
	여러 종목을 담아서 한번에 주문 낼 수 있는 Basket기능을 제공합니다. 종목을 선정하는 방법은 buildPortfolio함수를 통해 사용자가 직접 설정할 수 있습니다.
'''


class Basket:

    def __init__(self, account, targetSize, budget):
        self.account = account
        self.targetSize = targetSize
        self.budget = budget

    def setPortfolioBuilder(self, func):
        pass
