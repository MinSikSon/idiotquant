import requests
import json
import time
import main

if __name__ == "__main__":
    _url = 'http://221.163.190.38:3000/stock/market-info'
    # _url = 'http://localhost:3000/stock/market-info'
    print('_url', _url)

    time.strftime('%c', time.localtime(time.time()))
    _dayOfWeekend = time.strftime('%w', time.localtime(time.time()))
    print(_dayOfWeekend)
    if _dayOfWeekend is "5" or _dayOfWeekend is "6":
        exit()

    _date = time.strftime('%Y%m%d', time.localtime(time.time()))
    main.extractMarketInformationAllOnly(_date)

    _file_name = 'marketInformation_%s.json' % _date
    print('_file_name', _file_name)
    _file_path = 'data/%s' % _file_name
    print('_file_path', _file_path)
    with open(_file_path, 'r', encoding='utf-8') as raw:
        json_data = json.load(raw)
        res = requests.post(_url, json=json_data)
        print(res)
