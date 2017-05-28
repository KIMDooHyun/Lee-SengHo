from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, quote_plus, unquote
import xml.etree.ElementTree as ET

class GetData:
    choosenumber=int(input("약품 및 건강식품을 검색합니다. 1을 입력하면 약품이름검색, 2는 건강식품을 검색합니다. :"))
    if choosenumber==1:
        itemname=str(input("약품 이름을 입력합니다 : "))
        decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')
        baseurl = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('item_name') : itemname, quote_plus('entp_name') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
        url = baseurl+queryParams
        def main(self):
            data=urlopen(self.url).read() 
            #print(data)
            f=open("drug-db-itemname.xml","wb")
            f.write(data)
            f.close()
            tree = ET.parse('drug-db-itemname.xml')
            root=tree.getroot()
            ITEM_NAME = root.findtext('body/items/item/ITEM_NAME')
            CLASS_NAME = root.findtext('body/items/item/CLASS_NAME')
            ITEM_SEQ = root.find('body/items/item/ITEM_SEQ').text
            ENTP_NAME = root.findtext('body/items/item/ENTP_NAME')
            print("약물등록번호 : ", ITEM_SEQ)
            print("약물명 :", ITEM_NAME)
            print("제조사 :", ENTP_NAME)
            print("용도 : ", CLASS_NAME)
    elif choosenumber==2:
        itemname=str(input("건강 식품 이름을 입력합니다 : "))
        decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')
        baseurl = 'http://apis.data.go.kr/1470000/HtfsTrgetInfoService/getHtfsInfoList'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('prdlst_nm') : itemname, quote_plus('bssh_nm') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
        url = baseurl+queryParams
        print(url)
        def main(self):
            data=urlopen(self.url).read()
            #print(data)
            f=open("htfs-db-itemname.xml","wb")
            f.write(data)
            f.close()
            tree = ET.parse('htfs-db-itemname.xml')
            root=tree.getroot()
            PRMS_DT = root.find('body/items/item/PRMS_DT').text
            PRDLST_NM = root.findtext('body/items/item/PRDLST_NM')
            DISPOS = root.findtext('body/items/item/DISPOS')
            BSSH_NM = root.findtext('body/items/item/BSSH_NM')
            NTK_MTHD = root.findtext('body/items/item/NTK_MTHD')
            print("건강식품등록번호 :", PRMS_DT)
            print("약물명 :", PRDLST_NM)
            print("제조사 :",BSSH_NM)
            print("생김새 :", DISPOS)
            print("복용 방법 :", NTK_MTHD)
getData=GetData()
getData.main()

