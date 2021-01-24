from interface.opendart import OpenDart
from interface.krx import Krx
from interface.corpcode import CorpCode
import interface.common as Common

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

def extractLatestStockInfoToLatestJsonFile():
    '''
    TODO: latest date 가져오는 기능은 다른 feature 에서 구현 예정.
    현재는 수동으로 businessYear, businessQuarter, date 를 입력해야 합니다.
    '''
    businessYear = 2020
    businessQuarter = 3
    date = "20210122"

    marketValue = Krx().getMarketValue(date)
    financialInfoAll = OpenDart().getFinancialInformationAll(businessYear, businessQuarter)


    for corp in CorpCode().corpList:
        corpName = corp.findtext("corp_name")
        try:
            marketValue["data"][corpName].update(financialInfoAll[corpName])
        except KeyError:
            continue

    Common.extractJson(marketValue, "./data/latest.json")

if __name__ == "__main__" :
    extractLatestStockInfoToLatestJsonFile()


