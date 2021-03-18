from xml.etree.ElementTree import parse

from pykrx import stock


class CorpCode:
    def __init__(self, useCorpCodeXml=True):
        self.useCorpCodeXml = useCorpCodeXml
        if useCorpCodeXml == True:
            tree = parse("interface/CORPCODE.xml")
            root = tree.getroot()
            self.corpList = root.findall("list")
        else:
            self.tickerList = stock.get_market_ticker_list()

    def getAllCorpCode(self):
        if self.useCorpCodeXml == True:
            return self.corpList
        else:
            return self.tickerList

    def getCorpCodeByCorpName(self, corpName):
        if self.useCorpCodeXml == True:
            for corpList in self.corpList:
                if corpList.findtext("corp_name") == corpName:
                    return corpList.findtext("corp_code")
        else:
            for ticker in self.tickerList:
                name = stock.get_market_ticker_name(ticker)
                if name == corpName:
                    return ticker

        return None


if __name__ == "__main__":
    corpCode = CorpCode(useCorpCodeXml=False)
    # print(corpCode.getAllCorpCode())
    print(corpCode.getCorpCodeByCorpName("삼성전자"))
    print(corpCode.getCorpCodeByCorpName("POSCO"))
