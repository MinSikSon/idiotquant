from interface.opendart import OpenDart

if __name__ == "__main__" :
    stOpenDart = OpenDart()
    res = stOpenDart.getFinancialInformation("삼성전자", 2020, 3)
    
    print(res)