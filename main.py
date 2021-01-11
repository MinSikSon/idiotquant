from interface.opendart import OpenDart
from interface.krx import Krx

if __name__ == "__main__" :
    corpName = "금강공업"

    stOpenDart = OpenDart()
    resFinancialInfo = stOpenDart.getFinancialInformation(corpName, 2020, 3)
    print("1. FinancialInfo 전체 출력")
    print(resFinancialInfo)
    print("2. FinancialInfo 에서 corpName 에 해당하는 데이터 출력")
    print(resFinancialInfo[corpName])

    stKrx = Krx()
    resFundamental = stKrx.getMarketFundamentalByTicker(date="20201222")
    print(resFundamental[corpName])

    resOhlcv = stKrx.getMarketOhlcvByTicker(date="20201222")
    print(resOhlcv[corpName])