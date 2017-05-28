from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, quote_plus, unquote
import xml.etree.ElementTree as ET
from appJar import gui

app=gui()
def setting(rb):
    if app.getRadioButton("drug")=='약품 이름검색':
        app.setLabel("f2", "약품 이름을 검색합니다.")
        app.updateEntryDefault("searching_option", "약품 이름을 입력하십시오.")
    elif app.getRadioButton("drug")=='건강 식품검색':
        app.setLabel("f2", "건강 식품을 검색합니다.")
        app.updateEntryDefault("searching_option", "건강 식품을 입력하십시오.")
def searching(rb):
    if app.getRadioButton("drug")=='약품 이름검색':
        itemname=app.getEntry("searching_option")
        decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')
        baseurl = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('item_name') : itemname, quote_plus('entp_name') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
        url = baseurl+queryParams
        print(url)
        def main():
            data=urlopen(url).read() 
            #print(data)
            f=open("drug-db-itemname.xml","wb")
            f.write(data)
            f.close()
            tree = ET.parse('drug-db-itemname.xml')
            root=tree.getroot()                
            ITEM_NAME = root.findtext('body/items/item/ITEM_NAME')
            if ITEM_NAME==None:
                print("이름을 다시한번 확인해 주십시오.")
            else:
                CLASS_NAME = root.findtext('body/items/item/CLASS_NAME')
                ITEM_SEQ = root.find('body/items/item/ITEM_SEQ').text
                ENTP_NAME = root.findtext('body/items/item/ENTP_NAME')
                print("약물등록번호 : ", ITEM_SEQ)
                print("약물명 :", ITEM_NAME)
                print("제조사 :", ENTP_NAME)
                print("용도 : ", CLASS_NAME)
        main()
    elif app.getRadioButton("drug")=='건강 식품검색':
        itemname=app.getEntry("searching_option")
        decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')
        baseurl = 'http://apis.data.go.kr/1470000/HtfsTrgetInfoService/getHtfsInfoList'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('prdlst_nm') : itemname, quote_plus('bssh_nm') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
        url = baseurl+queryParams
        print(url)
        def main():
            data=urlopen(url).read()
            #print(data)
            f=open("htfs-db-itemname.xml","wb")
            f.write(data)
            f.close()
            tree = ET.parse('htfs-db-itemname.xml')
            root=tree.getroot()
            PRMS_DT = root.findtext('body/items/item/PRMS_DT')
            if PRMS_DT==None:
                print("이름을 다시한번 확인해 주십시오.")
            else:
                PRDLST_NM = root.find('body/items/item/PRDLST_NM').text
                BSSH_NM = root.findtext('body/items/item/BSSH_NM')
                NTK_MTHD = root.findtext('body/items/item/NTK_MTHD')
                print("건강식품등록번호 :", PRMS_DT)
                print("식품명 :", PRDLST_NM)
                print("제조사 :",BSSH_NM)
                print("복용 방법 :", NTK_MTHD)
        main()
app.addEntry("searching_option")
app.addButton("검색",searching,0,1)
app.setEntryDefault("searching_option", "　")
app.addLabel("f2", "검색할 환경을 선택하십시오.",2,)
app.addButton("설정", setting,2,1)
app.addRadioButton("drug","약품 이름검색",3,)
app.addRadioButton("drug","건강 식품검색",3,1)
app.go()
