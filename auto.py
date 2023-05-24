import requests
import json
import time
import main
import datetime
# import schedule  # pip install schedule

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def postMarketInfoInRange():
    # _url = 'http://221.163.190.38:3000/stock/market-info'
    _url = 'http://localhost:3000/stock/market-info'
    print('_url', _url)

    datetime_start = datetime.datetime(2017, 1, 1)
    datetime_end = datetime.datetime.now()

    delta = datetime.timedelta(days=1)
    print(datetime_start)
    print(datetime_end)
    # for diff in range(440, 450): # 250: 2020-04-20
    # for diff in range(450, 470):  # 470: 2020-03-30
    for diff in range(580, 600):  #
        print('diff:', diff)
        # 2017-10-09 : 한글날
        target_date = datetime_end - (delta * diff)
        _date = target_date.strftime('%Y%m%d')
        # print(_date)
        _dayOfWeekend = target_date.weekday()
        if _dayOfWeekend == 5 or _dayOfWeekend == 6:  # datetime 에서 0 은 월요일, 6은 일요일.
            continue
        # print(target_date, target_date.weekday(), target_date < datetime_start)
        print(target_date.weekday(), target_date)
        # time.sleep(10)  # [NOTE] post 를 너무 빨리 보내니, 서버가 죽음

        # exit()
        main.extractMarketInformationAllOnly(_date)

        _file_name = 'marketInformation_%s.json' % _date
        print('_file_name', _file_name)
        _file_path = 'data/%s' % _file_name
        print('_file_path', _file_path)
        with open(_file_path, 'r', encoding='utf-8') as raw:
            json_data = json.load(raw)
            res = requests.post(_url, json=json_data)
            print(res)

    exit()


def postTodayMarketInfo():
    # _url = 'http://221.163.190.38:3000/stock/market-info'
    # _url = 'http://localhost:3000/stock/market-info'
    _url = 'https://localhost:3000/database/market-info'
    # _url = 'https://15.164.210.174:3000/stock/market-info'
    
    print('_url:', _url)

    time.strftime('%c', time.localtime(time.time()))
    _date = time.strftime('%Y%m%d', time.localtime(time.time()))
    _dayOfWeekend = time.strftime('%w', time.localtime(time.time()))
    print(_date, _dayOfWeekend)
    if _dayOfWeekend == "6" or _dayOfWeekend == "0":
        print('Today is the weekend. (%s)', _dayOfWeekend)
        # return

    # _date = "20210817"
    # _date = "20210908"
    # _date = "20210910"
    # _date = "20210915"
    # _date = "20210917"
    # _date = "20210924"
    # _date = "20210927"
    # _date = "20210930"
    # _date = "20211006"
    # _date = "20211013"
    # _date = "20211029"

    # _date = "20211119"
    # _date = "20211126"
    # _date = "20211203"
    # _date = "20211210"
    # _date = "20211126"
    # _date = "20220331"
    # _date = "20220405"
    # _date = "20220420"
    # _date = "20220427"
    # _date = "20220518"
    # _date = "20220525"
    # _date = "20220526"
    # _date = "20220603"
    # _date = "20220608"
    # _date = "20220615"
    # _date = "20220622"
    # _date = "20220629"
    # _date = "20220630"
    # _date = "20220712"
    # _date = "20220713"
    # _date = "20220718"
    # _date = "20220725"
    # _date = "20220804"
    # _date = "20220808"
    # _date = "20220824"
    # _date = "20220914"
    # _date = "20220923"
    # _date = "20220926"
    # _date = "20220929"
    # _date = "20221004"
    # _date = "20221006"
    # _date = "20221012"
    # _date = "20221013"
    # _date = "20221014"
    # _date = "20221017"
    # _date = "20221019"
    # _date = "20221020"
    # _date = "20221021"
    # _date = "20221024"
    # _date = "20221025"
    # _date = "20221026"
    # _date = "20221027"
    # _date = "20221028"
    # _date = "20221103"
    # _date = "20221109"
    # _date = "20221115"
    # _date = "20221116"
    # _date = "20221121"
    # _date = "20221124"
    # _date = "20221129"
    # _date = "20221130"
    # _date = "20221213"
    # _date = "20221220"
    # _date = "20221226"
    # _date = "20230103"
    # _date = "20230111"

    # _date = "20221214"
    # _date = "20211214"
    # _date = "20201214"
    # _date = "20191213"
    # _date = "20191214"

    # _date = "20230302"
    # _date = "20230324"
    # _date = "20230417"
    # _date = "20230426"
    _date = "20230524"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    print(_date, _dayOfWeekend)
    main.extractMarketInformationAllOnly(_date)

    exit()

    _file_name = 'marketInformation_%s.json' % _date
    _file_path = 'data/%s' % _file_name
    print('_file_name', _file_name, ', _file_path', _file_path)
    with open(_file_path, 'r', encoding='utf-8') as raw:
        json_data = json.load(raw)
        res = requests.post(_url, json=json_data, verify=False)
        # res = session.post(_url, json=json_data, verify=False)
        print('res:', res)


if __name__ == "__main__":
    postTodayMarketInfo()
    exit()


    postTime = '16:00:00'
    print('[postTodayMarketInfo]', 'postTime: every', postTime)
    schedule.every().day.at(postTime).do(postTodayMarketInfo)

    while True:
        schedule.run_pending()
        time.sleep(1)
