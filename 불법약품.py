from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, quote_plus, unquote
import xml.etree.ElementTree as ET
#import webbrowser
import webbrowser

class GetData:
    illicit_drugs = input("불법약품을 검색합니다. : ")
    itemname_encText = quote(illicit_drugs)
    decode_key = unquote('94G9o%2FpVMOcY%2F65ihjY%2FbXHetzaOK0ESh4bHnwaZPOrWDw0H5sGloaLcMRG2KRs70iLxGdPRDuZBNvLc%2BsG3fQ%3D%3D')
    baseurl = 'http://apis.data.go.kr/1470000/MdcinSdefctInfoService/getMdcinSdefctInfoList'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('col_001') : itemname_encText, quote_plus('col_002') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '3' })
    url = baseurl + queryParams
    print(url)
    
    def main(self):
        data = urlopen(self.url).read()
        f = open('MdcinSdefct-db.xml','wb')
        f.write(data)
        f.close()
        tree = ET.parse('MdcinSdefct-db.xml')
        root = tree.getroot()

        items = root.findall('body/items/item')
        
        ITEM_NAME = root.findtext('body/items/item/COL_001')
        period_NAME = root.findtext('body/items/item/COL_004')

        print('약품명 : ', ITEM_NAME)
        print('판매기간 : ', period_NAME)
        
        
        for item in items:
            information = item.findtext('COL_005')
            print("증상 : ",information)

        wiki_url = 'https://ko.wikipedia.org/wiki/' + self.itemname_encText
        new = 2 # open in a new tab, if possible
        webbrowser.open(wiki_url,new=new)



getdata=GetData()
getdata.main()
