import requests
import json
import time
import main
import datetime
import schedule  # pip install schedule


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


def postTodayMarketInfo():
    _url = 'http://221.163.190.38:3000/stock/market-info'
    # _url = 'http://localhost:3000/stock/market-info'
    print('_url', _url)

    time.strftime('%c', time.localtime(time.time()))
    _date = time.strftime('%Y%m%d', time.localtime(time.time()))
    _dayOfWeekend = time.strftime('%w', time.localtime(time.time()))
    print(_date, _dayOfWeekend)
    if _dayOfWeekend is "6" or _dayOfWeekend is "0":
        print('Today is the weekend. (%s)', _dayOfWeekend)
        return

    _date = "20210720"

    main.extractMarketInformationAllOnly(_date)

    _file_name = 'marketInformation_%s.json' % _date
    _file_path = 'data/%s' % _file_name
    print('_file_name', _file_name, ', _file_path', _file_path)
    with open(_file_path, 'r', encoding='utf-8') as raw:
        json_data = json.load(raw)
        res = requests.post(_url, json=json_data)
        print(res)


if __name__ == "__main__":
    postTime = '16:00:00'
    print('[postTodayMarketInfo]', 'postTime: every', postTime)
    schedule.every().day.at(postTime).do(postTodayMarketInfo)

    while True:
        schedule.run_pending()
        time.sleep(1)
