from xml.etree.ElementTree import parse

class CorpCode:
    tree = parse("interface/CORPCODE.xml")
    root = tree.getroot()
    corpList = root.findall("list")

    def getAllCorpCode(self):
        return self.corpList

    def getCorpCodeByCorpName(self, corpName):
        for i in range(0, len(self.corpList)):
            if self.corpList[i].findtext("corp_name") == corpName:
                return self.corpList[i].findtext("corp_code")

        return None