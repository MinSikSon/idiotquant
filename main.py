from interface.opendart import OpenDart
from interface.krx import Krx
from interface.corpcode import CorpCode
import interface.common as Common

def sample_1():
    print("#####", sample_1.__name__, "#####")

    businessYear = 2020
    businessQuarter = 1
    date = "20201224"

    stOpenDart = OpenDart()
    financialInfoAll = stOpenDart.getFinancialInformationAll(businessYear, businessQuarter)

    stKrx = Krx()
    resFundamental = stKrx.getMarketFundamentalByTicker(date)
    resOhlcv = stKrx.getMarketOhlcvByTicker(date)

    mergeDic = dict()
    corpList = CorpCode().getAllCorpCode()

    for i in range(0, len(corpList)):
        corpName = corpList[i].findtext("corp_name")
        # corpCode = corpList[i].findtext("corp_code")
        stockCode = corpList[i].findtext("stock_code")
        if stockCode == '' or stockCode == ' ':
            continue
        try:
            mergeDic[corpName] = {'종목명' : corpName}
            mergeDic[corpName].update(financialInfoAll[corpName])
            mergeDic[corpName].update(resFundamental[corpName])
            mergeDic[corpName].update(resOhlcv[corpName])
        except KeyError:
            pass

    print(mergeDic["삼양통상"])
    print(mergeDic["SK하이닉스"])
    print(mergeDic["삼성전자"])

def sample_2():
    print("#####", sample_2.__name__, "#####")

    corpName = "삼성전자"
    businessYear = 2020
    businessQuarter = 1

    stOpenDart = OpenDart()
    financialInfo = stOpenDart.getFinancialInformation(corpName, businessYear, businessQuarter)
    financialInfoAll = stOpenDart.getFinancialInformationAll(businessYear, businessQuarter)
    print(financialInfo)
    print(financialInfoAll[corpName])

def sample_3():
    print("#####", sample_3.__name__, "#####")

    corpName = "삼성전자"
    # date = "20201101"
    date = "20201223"
    print(corpName, date)

    stKrx = Krx()
    resOhlcv = stKrx.getMarketOhlcvByTicker(date)
    print(resOhlcv[corpName])

    resFundamental = stKrx.getMarketFundamentalByTicker(date)
    print(resFundamental[corpName])

def sample_4():
    print("#####", sample_4.__name__, "#####")

    aCorpName = ["삼성전자", "SK하이닉스", "롯데정보통신"]
    date = "20201224"

    print(aCorpName, date)

    stKrx = Krx()
    resMarketValue = stKrx.getMarketValue(date)
    for corpName in aCorpName:
        print(corpName, resMarketValue["data"][corpName])

def sample_5():
    print("#####", sample_5.__name__, "#####")

    date = "20201223"
    # date = "20201224"

    stKrx = Krx()
    extractPath = "./market_all_" + date + ".json"
    Common.extractJson(stKrx.getMarketValue(date), extractPath)

if __name__ == "__main__" :
    # sample_1() # NOTE: opendart 및 krx 에서 얻어온 데이터를 하나로 합치는 예.

    # sample_2() # NOTE: OpenDart 사용 예.

    # sample_3() # NOTE: Krx 사용 예.

    # sample_4() # NOTE: Krx 에서 얻을 수 있는 모든 data 를 추출

    sample_5() # NOTE: Krx 에서 데이터 얻어서 json file 로 저장