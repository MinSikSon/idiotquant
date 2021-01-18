# NOTE: opendart 는 하루 10,000 회 조회 제한이 있습니다.
import datetime

import requests
from ast import literal_eval # parse, string to dictionray

from interface.crtfc_key import CRTFC_KEY
from interface.corpcode import CorpCode

import json

import os

import pickle # key-value 유형의 데이터는 흔히 Dictionary 자료형 저장하는데 유용.


class OpenDart:
    __statusCode = {
        '000': '정상',
        '010': '등록되지 않은 키입니다.',
        '013': '*** 어떤 error 인지 확인 필요합니다. *** 아마도 해당 종목은 이 businessQuarter 의 재무제표가 없는 것 같습니다.',
        '011': '사용할 수 없는 키입니다. 오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.',
        '020': '요청 제한을 초과하였습니다. 일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, 요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.',
        '100': '필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.',
        '800': '원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.',
        '900': '정의되지 않은 오류가 발생하였습니다.',
    }
    __QUARTER = [
        None,
        "11013",  # 1분기보고서
        "11012",  # 반기보고서
        "11014",  # 3분기보고서
        "11011",  # 사업보고서
    ]
    API_HOST = "https://opendart.fss.or.kr/api/"
    __SUCCESS = 200

    __dirFinancialInfo = os.path.dirname(os.path.abspath(__file__)) + '/data/financialinfo'

    def __init__(self):
        self.corpCode = CorpCode()

    # https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
    def getFinancialInformation(self, corpName, businessYear, businessQuarter):
        if self.__checkParameterType(businessYear, businessQuarter) == False:
            return None

        if isinstance(corpName, str) == False:
            return None
        corpCode = self.corpCode.getCorpCodeByCorpName(corpName)
        if corpCode == None:
            return None

        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.__dirFinancialInfo):
            os.makedirs(self.__dirFinancialInfo)
        filePath = self.__dirFinancialInfo + '/' + self.__getFinancialInfoBinaryFileName(businessYear, businessQuarter)
        if os.path.isfile(filePath):
            # NOTE: file 이 있고, corpName 에 해당하는 데이터 있는지 확인.
            with open(filePath, 'rb') as f:
                financialInfo = pickle.load(f)
                if corpName in financialInfo.keys():
                    return financialInfo[corpName]

        reportCode = self.__QUARTER[int(businessQuarter)]

        # NOTE: 단일회사 주요계정, 다중회사 주요계정?
        URI = self.API_HOST  + "fnlttSinglAcnt.json" + "?crtfc_key=" + str(CRTFC_KEY) + "&corp_code=" + str(corpCode) + "&bsns_year=" + str(businessYear) + "&reprt_code=" + str(reportCode)
        res = requests.get(URI)

        if res.status_code != self.__SUCCESS:
            print("[warn] corpCode 가 잘못되었습니다", corpCode, res.status_code)
            return None

        resDecode = res.content.decode("utf-8")
        resRawDictionary = literal_eval(resDecode) # parse, string to dictionray

        # print(resRawDictionary)
        if resRawDictionary["status"] != "000":
            print("[warn] 종목명:",corpName, ", status:", resRawDictionary["status"], self.__statusCode[resRawDictionary["status"]])
            return None

        resDictionary = self.__dataCleansing(resRawDictionary["list"])

        tmpDict = dict()
        tmpDict[corpName] = resDictionary

        # NOTE: 데이터 백업.
        financialInfoDictionary = None
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                financialInfoDictionary = pickle.load(f)
            financialInfoDictionary[corpName] = resDictionary
            with open(filePath, 'wb') as f:
                pickle.dump(financialInfoDictionary, f)
            return financialInfoDictionary[corpName]

        with open(filePath, 'wb') as f:
            pickle.dump(tmpDict, f)
        return tmpDict[corpName]

    def getFinancialInformationAll(self, businessYear, businessQuarter):
        if self.__checkParameterType(businessYear, businessQuarter) == False:
            return None

        filePath = self.__dirFinancialInfo + '/' + self.__getFinancialInfoBinaryFileName(businessYear, businessQuarter)
        if self.__checkFinishMark(businessYear, businessQuarter):
            if os.path.isfile(filePath) == False:
                print("fatal error")
                return None
            with open(filePath, 'rb') as f:
                financialInfoDictionary = pickle.load(f)
                return financialInfoDictionary

        self.__clearExtractFinishMark(businessYear, businessQuarter)

        corpList = self.corpCode.getAllCorpCode()
        for i in range(0, len(corpList)):
            corpName = corpList[i].findtext("corp_name")
            # corpCode = corpList[i].findtext("corp_code")
            stockCode = corpList[i].findtext("stock_code")
            if stockCode == '' or stockCode == ' ':
                continue
            self.getFinancialInformation(corpName, businessYear, businessQuarter)

        self.__setExtractFinishMark(businessYear, businessQuarter)

        with open(filePath, 'rb') as f:
            financialInfoDictionary = pickle.load(f)
            return financialInfoDictionary

        print("fatal error")
        return None

    def __setExtractFinishMark(self, businessYear, businessQuarter):
        filePath = self.__dirFinancialInfo + '/' + self.__getFinancialInfoBinaryFileName(businessYear, businessQuarter)

        financialInfoDictionary = None
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                financialInfoDictionary = pickle.load(f)
            financialInfoDictionary["finish"] = True
            with open(filePath, 'wb') as f:
                pickle.dump(financialInfoDictionary, f)

    def __clearExtractFinishMark(self, businessYear, businessQuarter):
        filePath = self.__dirFinancialInfo + '/' + self.__getFinancialInfoBinaryFileName(businessYear, businessQuarter)

        if os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                financialInfoDictionary = pickle.load(f)
            financialInfoDictionary["finish"] = False
            with open(filePath, 'wb') as f:
                pickle.dump(financialInfoDictionary, f)

    def __getFinancialInfoBinaryFileName(self, businessYear, businessQuarter):
        return 'financialInfo_%s_%sQ.bin' % (businessYear, businessQuarter)

    def __checkFinishMark(self, businessYear=None, businessQuarter=None):
        # NOTE: 백업 데이터 존재 여부 확인.
        if not os.path.isdir(self.__dirFinancialInfo):
            return False
        # print(path)
        filePath = self.__dirFinancialInfo + '/' + self.__getFinancialInfoBinaryFileName(businessYear, businessQuarter)
        # print(filePath)
        if os.path.isfile(filePath) == False:
            return False

        # NOTE: file 이 있고, corpName 에 해당하는 데이터 있는지 확인.
        with open(filePath, 'rb') as f:
            financialInfo = pickle.load(f)
            if "finish" in financialInfo.keys():
                return True

        return False

    def __checkParameterType(self, businessYear, businessQuarter):
        if type(businessYear) is not int:
            return False
        if type(businessQuarter) is not int:
            return False
        if ((businessQuarter == 1) or (businessQuarter == 2) or (businessQuarter == 3) or (businessQuarter == 4)) == False:
            return False
        return True

    def __dataCleansing(self, rawDictionary):
        resDictionary = dict()
        resDictionary["rcept_no"]   = str(rawDictionary[0]["rcept_no"])
        resDictionary["reprt_code"] = str(rawDictionary[0]["reprt_code"])
        resDictionary["corp_code"]  = str(rawDictionary[0]["corp_code"])
        resDictionary["stock_code"] = str(rawDictionary[0]["stock_code"])
        resDictionary["fs_div"]     = str(rawDictionary[0]["fs_div"])
        resDictionary["fs_nm"]      = str(rawDictionary[0]["fs_nm"])
        resDictionary["sj_div"]     = str(rawDictionary[0]["sj_div"])
        resDictionary["thstrm_nm"]  = str(rawDictionary[0]["thstrm_nm"])
        resDictionary["thstrm_dt"]  = str(rawDictionary[0]["thstrm_dt"])
        resDictionary["sj_div"]     = str(rawDictionary[0]["sj_div"])

        # [NOTE] frmtrm_dt, frmtrm_amount 은 저장하지 않았습니다.
        for i in range(len(rawDictionary)):
            resDictionary[rawDictionary[i]["account_nm"]] = str(rawDictionary[i]["thstrm_amount"].replace(",", ""))

        # return json.dumps(resDictionary, ensure_ascii=False, indent="\t") # dict to json
        return resDictionary

    def getEmptyStockFinancialInfo(self):
        return {
            "rcept_no": None,
            "reprt_code": None,
            "corp_code": None,
            "stock_code": None,
            "fs_div": None,
            "fs_nm": None,
            "sj_div": None,
            "thstrm_nm": None,
            "thstrm_dt": None,
            "유동자산": None,
            "비유동자산": None,
            "자산총계": None,
            "유동부채": None,
            "비유동부채": None,
            "부채총계": None,
            "자본금": None,
            "이익잉여금": None,
            "자본총계": None,
            "매출액": None,
            "영업이익": None,
            "법인세차감전 순이익": None,
            "당기순이익": None,
        }