from xml.etree.ElementTree import parse

class CorpCode:
    tree = parse("interface/CORPCODE.xml")
    root = tree.getroot()
    corp_list = root.findall("list")

    def getCorpCodeByCorpName(self, corpName):
        for i in range(0, len(self.corp_list)):
            if self.corp_list[i].findtext("corp_name") == corpName:
                return self.corp_list[i].findtext("corp_code")

        return None