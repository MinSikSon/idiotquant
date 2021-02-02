from interface.opendart import OpenDart
from interface.krx import Krx
from interface.corpcode import CorpCode
import interface.common as Common

import idiotquant.core as Core

import argparse

import datetime

def sample_1():
    ohlcv = Krx().getMarketOhlcvByTicker("20210119")
    print(ohlcv["삼성전자"])
    print(ohlcv["SK하이닉스"])

def sample_2():
    fundamental = Krx().getMarketFundamentalByTicker("20210119")
    print(fundamental["현대차"])
    print(fundamental["CJ"])

def sample_3():
    marketValue = Krx().getMarketValue("20210119")
    print(marketValue["date"])
    print(marketValue["data_info"])
    print(marketValue["data"]["네오위즈홀딩스"])
    print(marketValue["data"]["HDC현대산업개발"])

def sample_4():
    financialInformation = OpenDart().getFinancialInformation("삼성전자", 2020, 3)
    print(financialInformation)

def sample_5():
    financialInformationAll = OpenDart().getFinancialInformationAll(2020, 3)
    print(financialInformationAll["삼성전자"])
    print(financialInformationAll["SK하이닉스"])

def sample_6():
    financialInformationAll = OpenDart().getFinancialInformationAll(2020, 3)
    Common.extractJson(financialInformationAll, './test.json')

def sample_7():
    marketCap = Krx().getMarketCapByTicker("20210119")
    print(marketCap["삼성전자"])
    print(marketCap["SK하이닉스"])

def extractLatestStockInfoToLatestJsonFile(businessYear, businessQuarter, date):
    '''
    TODO: latest date 가져오는 기능은 다른 feature 에서 구현 예정.
    현재는 수동으로 businessYear, businessQuarter, date 를 입력해야 합니다.
    '''
    # businessYear = 2020
    # businessQuarter = 3
    # date = "20210201"

    marketValue = Krx().getMarketValue(date)
    financialInfoAll = OpenDart().getFinancialInformationAll(businessYear, businessQuarter)


    for corp in CorpCode().corpList:
        corpName = corp.findtext("corp_name")
        try:
            marketValue["data"][corpName].update(financialInfoAll[corpName])
        except KeyError:
            continue

    # NOTE: ./data 폴더가 있어야 latest.json 파일이 생성됩니다.
    Common.extractJson(marketValue, "./data/latest.json")

def getBusinessDay():
    lastBusinessDay = datetime.datetime.today()
    if datetime.date.weekday(lastBusinessDay) == 5: # 토요일
        lastBusinessDay -= datetime.timedelta(days=1)
    elif datetime.date.weekday(lastBusinessDay) == 6: # 일요일
        lastBusinessDay -= datetime.timedelta(days=2)
    else: # 다음날 되었는지 확인
        nineHoursAgo = lastBusinessDay - datetime.timedelta(hours=9)
        if lastBusinessDay.strftime("%d") != nineHoursAgo.strftime("%d"):
            lastBusinessDay = nineHoursAgo
    
    return lastBusinessDay.strftime("%Y%m%d")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="전략별 종목 추천기능", usage="python3 main.py -h")
    parser.add_argument('--select-strategy', '-s', type=int, help='0: sample_1, 1: NCAV 전략, 2: sample_2', required=True)
    # TODO: 날짜 입력
    parser.add_argument('-y', '--year', type=int, help='2021', required=True)
    parser.add_argument('-q', '--quarter', type=int, help='1/2/3/4', required=True)
    parser.add_argument('-d', '--date', default=getBusinessDay(), type=str, help='Date in format yyyymmdd')
    # parser.add_argument('-d', '--date', type=str, help='Date in format yyyymmdd', required=True)

    args = parser.parse_args()

    # main logic
    extractLatestStockInfoToLatestJsonFile(args.year, args.quarter, args.date)
    Core.main(strategyNumber=args.select_strategy)

