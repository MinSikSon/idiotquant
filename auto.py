import requests
import json
import time
import main
import datetime


def postMarketInfoInRange():
    _url = 'http://221.163.190.38:3000/stock/market-info'
    # _url = 'http://localhost:3000/stock/market-info'
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
        if _dayOfWeekend is 5 or _dayOfWeekend is 6:  # datetime 에서 0 은 월요일, 6은 일요일.
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


if __name__ == "__main__":
    # postMarketInfoInRange()
    _url = 'http://221.163.190.38:3000/stock/market-info'
    # _url = 'http://localhost:3000/stock/market-info'
    print('_url', _url)

    time.strftime('%c', time.localtime(time.time()))
    _dayOfWeekend = time.strftime('%w', time.localtime(time.time()))
    print(_dayOfWeekend)
    if _dayOfWeekend is "6" or _dayOfWeekend is "0":
        print('Today is the weekend. (%s)', _dayOfWeekend)
        exit()

    _date = time.strftime('%Y%m%d', time.localtime(time.time()))

    # mod
    # _date = "20161214"
    # _date = "20170109"
    # _date = "20170116"
    # _date = "20170126"
    # _date = "20170206"
    # _date = "20170213"
    # _date = "20170220"
    # _date = "20170227"
    # _date = "20170306"
    # _date = "20170313"

    # _date = "20170320"
    # _date = "20170327"
    # _date = "20170403"
    # _date = "20170410"
    # _date = "20170417"
    # _date = "20170424"
    # _date = "20180201"
    # _date = "20180720"
    # _date = "20180721"
    # _date = "20180722"
    # _date = "20180723"
    # _date = "20180724"
    # _date = "20180725"
    # _date = "20180726"
    # _date = "20180727"
    # _date = "20180728"
    # _date = "20180729"
    # _date = "20180730"
    # _date = "20180731"
    # _date = "20190201"
    # _date = "20190213"
    # _date = "20190422"
    # _date = "20190713"
    # _date = "20190714"
    # _date = "20190715"
    # _date = "20190716"
    # _date = "20190717"
    # _date = "20190718"
    # _date = "20190719"
    # _date = "20190720"
    # _date = "20190721"
    # _date = "20200104"
    # _date = "20200131"
    # _date = "20201223"
    # _date = "20210104"
    # _date = "20210118"
    # _date = "20210119"
    # _date = "20210122"
    # _date = "20210201"
    # _date = "20210302"
    # _date = "20210303"
    # _date = "20210413"
    # _date = "20210414"
    # _date = "20210415"
    # _date = "20210416"
    # _date = "20210419"
    # _date = "20210420"
    # _date = "20210421"
    # _date = "20210422"
    # _date = "20210611"
    # _date = "20210622"
    # _date = "20210623"
    # _date = "20210624"
    # _date = "20210625"
    # _date = "20210628"
    # _date = "20210629"
    # _date = "%d" % (20210629)
    # _date = "20210630"
    # _date = "20210705"
    # _date = "20210706"
    # _date = "20210707"
    # _date = "20210708"
    # _date = "20210709"
    # _date = "20210712"
    # _date = "20210713"
    # _date = "20210714"
    # _date = "20210715"
    # _date = "20210719"
    _date = "20210720"

    main.extractMarketInformationAllOnly(_date)

    _file_name = 'marketInformation_%s.json' % _date
    print('_file_name', _file_name)
    _file_path = 'data/%s' % _file_name
    print('_file_path', _file_path)
    with open(_file_path, 'r', encoding='utf-8') as raw:
        json_data = json.load(raw)
        res = requests.post(_url, json=json_data)
        print(res)
