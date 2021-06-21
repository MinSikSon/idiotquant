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
    # businessYear = 2020
    # businessQuarter = 3
    # date = "20210201"

    marketValue = Krx().getMarketValue(date)
    financialInfoAll = OpenDart().getFinancialInformationAll(
        businessYear, businessQuarter)

    for corp in CorpCode().corpList:
        corpName = corp.findtext("corp_name")
        try:
            marketValue["data"][corpName].update(financialInfoAll[corpName])
        except KeyError:
            continue

    # NOTE: ./data 폴더가 있어야 latest.json 파일이 생성됩니다.
    Common.extractJson(marketValue, "./data/latest.json")


def extractFinancialInformationAllOnly(businessYear, businessQuarter):
    # businessYear = 2020
    # businessQuarter = 3
    financialInfoAll = OpenDart().getFinancialInformationAll(
        businessYear, businessQuarter)
    Common.extractJson(
        financialInfoAll, "./data/financialInformation_%s_%s.json" % (businessYear, businessQuarter))


def extractMarketInformationAllOnly(date):
    # businessYear = 2020
    # businessQuarter = 3
    marketValue = Krx().getMarketValue(date)

    Common.extractJson(
        marketValue, "./data/marketInformation_%s.json" % (date))


def getBusinessDay():
    lastBusinessDay = datetime.datetime.today()
    nineHoursAgo = lastBusinessDay - datetime.timedelta(hours=9)

    if datetime.date.weekday(lastBusinessDay) == 5:  # 오늘이 토요일 이라면, 금요일 기준으로 변경
        lastBusinessDay -= datetime.timedelta(days=1)
    elif datetime.date.weekday(lastBusinessDay) == 6:  # 오늘이 일요일 이라면, 금요일 기준으로 변경
        lastBusinessDay -= datetime.timedelta(days=2)
    # 오늘이 월요일 이지만 장 열리기 전이라면, 금요일 기준으로 변경
    elif datetime.date.weekday(lastBusinessDay) == 0:
        if datetime.date.weekday(nineHoursAgo) == 6:
            lastBusinessDay -= datetime.timedelta(hours=57)
        else:
            pass  # 오늘 기준
    # 장 열리기 전이라면, 어제 기준으로 변경
    elif lastBusinessDay.strftime("%d") != nineHoursAgo.strftime("%d"):
        lastBusinessDay = nineHoursAgo
    else:
        pass  # 오늘 기준

    return lastBusinessDay.strftime("%Y%m%d")


if __name__ == "__main__":
    # option
    parser = argparse.ArgumentParser(
        description="전략별 종목 추천기능", usage="python3 main.py -h")
    parser.add_argument('--select-strategy', '-s', type=int, default=1,
                        help='0: sample_1, 1: NCAV 전략, 2: sample_2')
    parser.add_argument('-y', '--year', type=int, help='2021', required=True)
    parser.add_argument('-q', '--quarter', type=int,
                        help='1/2/3/4', required=True)
    parser.add_argument('-d', '--date', default=getBusinessDay(),
                        type=str, help='Date in format yyyymmdd')

    # NOTE: quarter 정보만 뽑아내기 위해서, argument 추가
    parser.add_argument('-f', '--function', type=int, default=0,
                        help='0: 오늘 기준 데이터 추출, 1: 현재분기 재무제표 추출, 2: 오늘 주식 시장가 추출')

    args = parser.parse_args()

    if (args.function == 0):
        # main logic
        extractLatestStockInfoToLatestJsonFile(
            args.year, args.quarter, args.date)
        Core.main(strategyNumber=args.select_strategy)
    elif (args.function == 1):
        extractFinancialInformationAllOnly(args.year, args.quarter)
    elif(args.function == 2):
        extractMarketInformationAllOnly(args.date)
    else:
        pass
