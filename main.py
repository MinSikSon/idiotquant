from interface.opendart import OpenDart
from interface.krx import Krx

if __name__ == "__main__" :
    corpName = "삼성전자"

    stOpenDart = OpenDart()
    resFinancialInfo = stOpenDart.getFinancialInformation(corpName, 2020, 3)
    print(resFinancialInfo[corpName])

    stKrx = Krx()
    resFundamental = stKrx.getMarketFundamentalByTicker(date="20201222")
    print(resFundamental[corpName])

    resOhlcv = stKrx.getMarketOhlcvByTicker(date="20201222")
    print(resOhlcv[corpName])