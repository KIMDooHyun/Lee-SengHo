from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, quote_plus, unquote
import xml.etree.ElementTree as ET
#import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GetData:
    illicit_drugs = input("불법약물을 검색합니다. : ")
    itemname_encText = quote(illicit_drugs)
    decode_key = unquote('94G9o%2FpVMOcY%2F65ihjY%2FbXHetzaOK0ESh4bHnwaZPOrWDw0H5sGloaLcMRG2KRs70iLxGdPRDuZBNvLc%2BsG3fQ%3D%3D')
    baseurl = 'http://apis.data.go.kr/1470000/MdcinSdefctInfoService/getMdcinSdefctInfoList'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('col_001') : itemname_encText, quote_plus('col_002') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '3' })
    url = baseurl + queryParams
    #webbrowser.open_new(url)
    print(url)
    
    def main(self):
        data = urlopen(self.url).read()
        f = open('MdcinSdefct-db.xml','wb')
        f.write(data)
        f.close()
        tree = ET.parse('MdcinSdefct-db.xml')
        root = tree.getroot()
        ITEM_NAME = root.findtext('body/items/item/COL_001')
        period_NAME = root.findtext('body/items/item/COL_004')
        information = root.findtext('body/items/item/COL_005')
        information1 = root.findtext('body/items/item/COL_005')
        print('약품명 : ', ITEM_NAME)
        print('판매 기간 : ', period_NAME)
        print('증상 : ', information)
        print("증상 : ",information1)

getdata=GetData()
getdata.main()
