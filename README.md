# idiotquant

## About Idiotquant

blah blah.. 

## How to run
```
(root 로 이동)
python3 main.py -h
python3 main.py -y 2020 -q 3 -s 0
```

### Idiot Quant
1. modify variable that you want

variable
```
    stockWeight
    stockNum
```

2. implement the method in customeFunction class in custome_function.py file
 
method
```
    stockFilter
    stockPortfolioBuilder
```

3. execute program
 
```
    cd idiotquant
    python3 idiotquant/core.py
```

## Reference
- https://github.com/navdeep-G/samplemod



# interface
interface 는 krx(한국거래소), opendart(금융감독원) 에서 제공하는 정보를 wrapping 한 api(krx: https://github.com/sharebook-kr/pykrx, opendart: https://opendart.fss.or.kr/) 를 한 번 더 wrapping 하여 ***dictionary 타입***으로 얻어오도록 한 api 입니다. 때문에, 실제 거래시 참고용으로만 사용 부탁드립니다.

## 1 환경설정

### 1.1 설치
필요 모듈은 requirements.txt 에 적혀있습니다.

```
(root 로 이동 후)
make
```

### 1.2 Import
interface 모듈은 root 에서 사용하도록 디자인 되어 있습니다. Krx 는 유가 증권시장의 일별 정보를 제공합니다. OpenDart 는 종목별 재무제표를 제공합니다. 

```
(root 로 이동 후)
import interface.krx import Krx
import interface.opendart import OpenDart
...
```

## 2. API 설명
### 2.1 krx
pykrx(코스피 종목의 주가 관련 정보를 얻는 API) 를 wrapping 한 api 입니다.
지정한 일자(YYMMDD)의 코스피 시장에 상장된 ticker를 이용해 ***전종목***의 정보를 얻어 옵니다.
최초 얻어온 데이터는 interface/data/.. 이하에 backup 됩니다.

#### 2.1.1 getMarketOhlcvByTicker
전종목의 시세를 ***dictionary 타입***으로 얻어옵니다.

```python
# main.py - sample_1
import interface.krx import Krx
ohlcv = Krx().getMarketOhlcvByTicker("20210119")
print(ohlcv["삼성전자"])
print(ohlcv["SK하이닉스"])
```
```text
{'시가': '84500', '고가': '88000', '저가': '83600', '종가': '87000', '거래량': '39895044', '거래대금': '3441342754500'}
{'시가': '131000', '고가': '132000', '저가': '128500', '종가': '130500', '거래량': '4513315', '거래대금': '589182407500'}
```

#### 2.1.2 getMarketFundamentalByTicker
전 종목의 DIV/BPS/PER/EPS/PBR 를 ***dictionary 타입***으로 얻어옵니다.

```python
# main.py - sample_2
import interface.krx import Krx
fundamental = Krx().getMarketFundamentalByTicker("20210119")
print(fundamental["현대차"])
print(fundamental["CJ"])
```
```text
{'BPS': '253001', 'PER': '23.12', 'PBR': '1.0337656768155066', 'EPS': '11310', 'DIV': '1.53', 'DPS': '4000'}
{'BPS': '126448', 'PER': '13.23', 'PBR': '0.8619106272934328', 'EPS': '8240', 'DIV': '1.7', 'DPS': '1850'}
```

#### 2.1.3 getMarketValue
전 종목의 시세 및 DIV/BPS/PER/EPS/PBR 를 ***dictionary 타입***으로 얻어옵니다.
얻어온 dictionary 는 아래처럼 구성되어 있습니다.
```json
{
	"date": "20210118",
	"finish": true,
	"market": "ALL",
	"data_info": {
		"ohlcv": true,
		"fundamental": true
	},
	"data": {
		"덕성": {
			"시가": "8260",
			"고가": "8270",
			"저가": "7550",
            "종가": "7550",
```
```python
# main.py - sample_3
import interface.krx import Krx
fundamental = Krx().getMarketFundamentalByTicker("20210119")
marketValue = Krx().getMarketValue("20210119")
print(marketValue["date"])
print(marketValue["data_info"])
print(marketValue["data"]["네오위즈홀딩스"])
print(marketValue["data"]["HDC현대산업개발"])
```
```text
20210119
{'ohlcv': True, 'fundamental': True}
{'시가': '16650', '고가': '16850', '저가': '16350', '종가': '16750', '거래량': '30562', '거래대금': '508024400', 'BPS': '36556', 'PER': '6.62', 'PBR': '0.45805739396405515', 'EPS': '2529', 'DIV': '0.73', 'DPS': '123'}
{'시가': '29000', '고가': '30600', '저가': '28700', '종가': '30600', '거래량': '2965987', '거래대금': '88314675750', 'BPS': '47095', 'PER': '3.5', 'PBR': '0.6488693067204586', 'EPS': '8731', 'DIV': '1.63', 'DPS': '500'}
```

#### 2.1.4 (TBD) getMarketCapByTicker
특정 일자의 종목별 종가/시가총액/거래량/거래대금/상장주식수를 ***dictionary 타입***으로 얻어 옵니다.

```python
# main.py - sample_7
import interface.krx import Krx
marketCap = Krx().getMarketCapByTicker("20210119")
print(marketCap["삼성전자"])
print(marketCap["SK하이닉스"])
```
```text
{'종목명': '삼성전자', '종가': '87000', '시가총액': '519371081850000', '거래량': '39895044', '거래대금': '519371081850000', '상장주식수': '5969782550'}
{'종목명': 'SK하이닉스', '종가': '130500', '시가총액': '95004308632500', '거래량': '4513315', '거래대금': '95004308632500', '상장주식수': '728002365'}
```

### 2.2 opendart
#### 2.2.1 getFinancialInformation
한 종목의 재무제표 정보를 ***dictionary 타입***으로 얻어 옵니다.

```python
# main.py - sample_4
import interface.opendart import OpenDart
financialInformation = OpenDart().getFinancialInformation("삼성전자", 2020, 3)
print(financialInformation)
```
```text
{'rcept_no': '20201116001248', 'reprt_code': '11014', 'corp_code': '00126380', 'stock_code': '005930', 'fs_div': 'CFS', 'fs_nm': '연결재무제표', 'sj_div': 'BS', 'thstrm_nm': '제 52 기3분기말', 'thstrm_dt': '2020.09.30 현재', '유동자산': '80000498000000', '비유동자산': '148286383000000', '자산총계': '228286881000000', '유동부채': '44642243000000', '비유동부채': '2057001000000', '부채총계': '46699244000000', '자본금': '897514000000', '이익잉여금': '176171955000000', '자본총계': '181587637000000', '매출액': '47801234000000', '영업이익': '7036350000000', '법인세차감전 순이익': '6925347000000', '당기순이익': '5270095000000'}
```

#### 2.2.2 getFinancialInformationAll
전 종목의 재무제표 정보를 ***dictionary 타입***으로 얻어 옵니다.
얻어온 dictionary 는 아래처럼 구성되어 있습니다.

```json
{
	"엑세스바이오": {
		"rcept_no": "20201113000683",
		"reprt_code": "11014",
		"corp_code": "00956028",
		"stock_code": "950130",
		"fs_div": "CFS",
		"fs_nm": "연결재무제표",
		"sj_div": "BS",
		"thstrm_nm": "제 19 기3분기말",
		"thstrm_dt": "2020.09.30 현재",
		"유동자산": "24422930",
		"비유동자산": "56801510",
		"자산총계": "81224440",
		"유동부채": "14180242",
		"비유동부채": "697550",
		"부채총계": "14877792",
		"자본금": "1827480",
		"이익잉여금": "12752689",
		"자본총계": "66346648",
		"매출액": "4746182",
		"영업이익": "306216",
		"법인세차감전 순이익": "239662",
		"당기순이익": "681892"
	},
	"글로벌에스엠": {
		"rcept_no": "20201126000338",
		"reprt_code": "11014",
		"corp_code": "00783246",
		"stock_code": "900070",
		"fs_div": "CFS",
```
```python
# main.py - sample_5
import interface.opendart import OpenDart
financialInformationAll = OpenDart().getFinancialInformationAll(2020, 3)
print(financialInformationAll["삼성전자"])
print(financialInformationAll["SK하이닉스"])
```
```text
{'rcept_no': '20201116001248', 'reprt_code': '11014', 'corp_code': '00126380', 'stock_code': '005930', 'fs_div': 'CFS', 'fs_nm': '연결재무제표', 'sj_div': 'BS', 'thstrm_nm': '제 52 기3분기말', 'thstrm_dt': '2020.09.30 현재', '유동자산': '80000498000000', '비유동자산': '148286383000000', '자산총계': '228286881000000', '유동부채': '44642243000000', '비유동부채': '2057001000000', '부채총계': '46699244000000', '자본금': '897514000000', '이익잉여금': '176171955000000', '자본총계': '181587637000000', '매출액': '47801234000000', '영업이익': '7036350000000', '법인세차감전 순이익': '6925347000000', '당기순이익': '5270095000000'}
{'rcept_no': '20201116001609', 'reprt_code': '11014', 'corp_code': '00164779', 'stock_code': '000660', 'fs_div': 'CFS', 'fs_nm': '연결재무제표', 'sj_div': 'BS', 'thstrm_nm': '제 73 기3분기말', 'thstrm_dt': '2020.09.30 현재', '유동자산': '13581565000000', '비유동자산': '47885009000000', '자산총계': '61466574000000', '유동부채': '7166724000000', '비유동부채': '6178915000000', '부채총계': '13345639000000', '자본금': '3657652000000', '이익잉여금': '42781239000000', '자본총계': '48120935000000', '매출액': '7893103000000', '영업이익': '1213523000000', '법인세차감전 순이익': '1117197000000', '당기순이익': '888283000000'}
```

### 2.3 common
#### 2.3.1 extractJson
데이터를 특정 경로에 json 형식으로 추출합니다.

```python
# main.py - sample_6
from interface.common as Common
extractData = OpenDart().getFinancialInformationAll(2020, 3)
extractPath = './test.json'
Common.extractJson(extractData, extractPath)
```
