from interface.opendart import OpenDart
from interface.krx import Krx
from interface.corpcode import CorpCode

def sample_1():
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
    corpName = "삼성전자"
    businessYear = 2020
    businessQuarter = 1

    stOpenDart = OpenDart()
    financialInfo = stOpenDart.getFinancialInformation(corpName, businessYear, businessQuarter)
    financialInfoAll = stOpenDart.getFinancialInformationAll(businessYear, businessQuarter)
    print(financialInfo)
    print(financialInfoAll[corpName])

def sample_3():
    corpName = "삼성전자"
    date = "20201224"

    stKrx = Krx()
    resFundamental = stKrx.getMarketFundamentalByTicker(date)
    print(resFundamental[corpName])

    resOhlcv = stKrx.getMarketOhlcvByTicker(date)
    print(resOhlcv[corpName])

if __name__ == "__main__" :
    sample_1() # NOTE: opendart 및 krx 에서 얻어온 데이터를 하나로 합치는 예.

    sample_2() # NOTE: OpenDart 사용 예.

    sample_3() # NOTE: Krx 사용 예.
