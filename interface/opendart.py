# NOTE: opendart 는 하루 10,000 회 조회 제한이 있습니다.
import datetime

import requests
from ast import literal_eval # parse, string to dictionray

from interface.crtfc_key import CRTFC_KEY
from interface.corpcode import CorpCode

import json


class OpenDart:
    statusCode = {
        '000': '정상',
        '010': '등록되지 않은 키입니다.',
        '013': '*** 어떤 error 인지 확인 필요합니다. *** 아마도 해당 businessQuarter 의 재무제표가 없는 것 같습니다.',
        '011': '사용할 수 없는 키입니다. 오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.',
        '020': '요청 제한을 초과하였습니다. 일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, 요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.',
        '100': '필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.',
        '800': '원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.',
        '900': '정의되지 않은 오류가 발생하였습니다.',
    }
    QUARTER = [
        None,
        "11013",  # 1분기보고서
        "11012",  # 반기보고서
        "11014",  # 3분기보고서
        "11011",  # 사업보고서
    ]
    API_HOST = "https://opendart.fss.or.kr/api/"
    SUCCESS = 200

    def __init__(self):
        self.corpCode = CorpCode()

    # [NOTE] not used
    # https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002
    def getCompanyInformation(self, corpName):
        corpCode = self.corpCode.getCorpCodeByCorpName(corpName)
        if corpCode == None:
            return None
            
        URI = self.API_HOST + "company.json" + "?crtfc_key=" + CRTFC_KEY + "&corp_code=" + corpCode
        res = requests.get(URI)
    
        if res.status_code != 200:
            print("[warn] corpCode 가 잘못되었습니다", corpCode)
            return None

        return res

    # https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
    def getFinancialInformation(self, corpName, businessYear=None, businessQuarter=None):
        if businessYear == None:
            return None
        if businessQuarter == None:
            return None
        if ((businessQuarter == 1) or (businessQuarter == 2) or (businessQuarter == 3) or (businessQuarter == 4)) == False:
            return None

        corpCode = self.corpCode.getCorpCodeByCorpName(corpName)
        if corpCode == None:
            return None
        
        reportCode = self.QUARTER[int(businessQuarter)]

        # [NOTE] 단일회사 주요계정, 다중회사 주요계정?
        URI = self.API_HOST  + "fnlttSinglAcnt.json" + "?crtfc_key=" + str(CRTFC_KEY) + "&corp_code=" + corpCode + "&bsns_year=" + str(businessYear) + "&reprt_code=" + str(reportCode)
        res = requests.get(URI)

        if res.status_code != self.SUCCESS:
            print("[warn] corpCode 가 잘못되었습니다", corpCode, res.status_code)
            return None

        resDecode = res.content.decode("utf-8")
        resRawDictionary = literal_eval(resDecode) # parse, string to dictionray

        # print(resRawDictionary)
        if resRawDictionary["status"] != "000":
            print("[warn]", resRawDictionary["status"], self.statusCode[resRawDictionary["status"]])
            return None


        resDictionary = self.dataCleansing(resRawDictionary["list"])

        tmpDict = dict()
        tmpDict[corpName] = resDictionary

        return tmpDict

    def dataCleansing(self, rawDictionary):
        resDictionary = dict()
        resDictionary["rcept_no"] = str(rawDictionary[0]["rcept_no"])
        resDictionary["reprt_code"] = str(rawDictionary[0]["reprt_code"])
        resDictionary["corp_code"] = str(rawDictionary[0]["corp_code"])
        resDictionary["stock_code"] = str(rawDictionary[0]["stock_code"])
        resDictionary["fs_div"] = str(rawDictionary[0]["fs_div"])
        resDictionary["fs_nm"] = str(rawDictionary[0]["fs_nm"])
        resDictionary["sj_div"] = str(rawDictionary[0]["sj_div"])
        resDictionary["thstrm_nm"] = str(rawDictionary[0]["thstrm_nm"])
        resDictionary["thstrm_dt"] = str(rawDictionary[0]["thstrm_dt"])
        resDictionary["sj_div"] = str(rawDictionary[0]["sj_div"])

        # [NOTE] frmtrm_dt, frmtrm_amount 은 저장하지 않았습니다.
        for i in range(len(rawDictionary)):
            resDictionary[rawDictionary[i]["account_nm"]] = str(rawDictionary[i]["thstrm_amount"].replace(",", ""))

        # return json.dumps(resDictionary, ensure_ascii=False, indent="\t") # dict to json
        return resDictionary