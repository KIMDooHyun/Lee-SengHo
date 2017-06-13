from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote, quote_plus, unquote
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET
import webbrowser
import mimetypes
import mysmtplib
from appJar import gui

app=gui()   # APP jar지원 GUI을 기본 함수.
app.setGeometry("960x480")      # 프로그램 크기 설정
def setting(rb):            # 설정 버튼 함수
    if app.getRadioButton("drug")=='약품 이름검색': 
        app.setLabel("f2", "약품 이름을 검색합니다.")
        app.updateEntryDefault("searching_option_item", "알약형 약품 이름을 입력하십시오.")
    elif app.getRadioButton("drug")=='건강 식품검색':
        app.setLabel("f2", "건강 식품을 검색합니다.")
        app.updateEntryDefault("searching_option_item", "건강 식품을 입력하십시오.")
    elif app.getRadioButton("drug")=="부작용보고 약물검색":
        app.setLabel("f2", "부작용보고 약물을 검색합니다.")
        app.updateEntryDefault("searching_option_item", "부작용보고 약물을 입력하십시오.")
def searching(rb):          # 검색 버튼 함수
    if app.getRadioButton("drug")=='약품 이름검색':
        itemname=app.getEntry("searching_option_item")
        if app.getEntry("searching_option_item")=='':
            app.errorBox("경고", "검색창에 약물을 입력해주세요.")
        else:
            decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')    # 의약품 API 인증
            baseurl = 'http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'              # 의약품 기본 URL
            queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('item_name') : itemname, quote_plus('entp_name') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
            url = baseurl+queryParams
            def main():
                global ITEM_NAME
                global ITEM_SEQ
                global ENTP_NAME
                global CLASS_NAME
                global ImageUrl
                data=urlopen(url).read()
                f=open("drug-db-itemname.xml","wb")     # 의약물 XML파일 열기
                f.write(data)
                f.close()
                tree = ET.parse('drug-db-itemname.xml')
                root=tree.getroot()
                ITEM_NAME = root.findtext('body/items/item/ITEM_NAME')
                # 의약품의 데이터가 잘못된 경우. 경고문구 출력.
                if ITEM_NAME==None:
                    app.errorBox("경고","이름을 다시한번 확인해 주십시오.")

                # 의약품 내용을 출력.
                else:
                    ITEM_SEQ = root.find('body/items/item/ITEM_SEQ').text
                    CLASS_NAME = root.findtext('body/items/item/CLASS_NAME')
                    ENTP_NAME = root.findtext('body/items/item/ENTP_NAME')
                    ImageUrl = root.findtext('body/items/item/ITEM_IMAGE')
                    app.setLabel("등록번호-1", "약물등록번호 : ")
                    app.setLabel("등록번호-2", ITEM_SEQ)
                    app.setLabel("이름-1", "약물명 : ")
                    app.setLabel("이름-2", ITEM_NAME)
                    app.setLabel("제조사/증상-1", "제조사 : ")
                    app.setLabel("제조사/증상-2", ENTP_NAME)
                    app.setLabel("용도/복용방법-1", "용도 : ")
                    app.setLabel("용도/복용방법-2", CLASS_NAME)
            main()
    # 건강식품 보조제 검색.       
    elif app.getRadioButton("drug")=='건강 식품검색':
        if app.getEntry("searching_option_item")=='':
            app.errorBox("경고", "검색창에 식품 이름을 입력해주세요.")
        else:
            itemname=app.getEntry("searching_option_item")
            decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')    # 건강식품 API인증키 
            baseurl = 'http://apis.data.go.kr/1470000/HtfsTrgetInfoService/getHtfsInfoList'     # 건강식품 기본 URL
            queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('prdlst_nm') : itemname, quote_plus('bssh_nm') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
            url = baseurl+queryParams
            def main():
                global PRMS_DT
                global PRDLST_NM
                global BSSH_NM
                global NTK_MTHD
                data=urlopen(url).read()
                #print(data)
                f=open("htfs-db-itemname.xml","wb")     # 건강식품 보조제 XML파일 열기
                f.write(data)
                f.close()
                tree = ET.parse('htfs-db-itemname.xml')
                root=tree.getroot()
                PRMS_DT = root.findtext('body/items/item/PRMS_DT')

                # 검색한 데이터가 잘못된경우. 경고문구 출력.
                if PRMS_DT==None:
                    app.errorBox("경고","이름을 다시한번 확인해 주십시오.")

                # 검색한 건강식품의 내용을 출력.    
                else:
                    PRDLST_NM = root.find('body/items/item/PRDLST_NM').text
                    BSSH_NM = root.findtext('body/items/item/BSSH_NM')
                    NTK_MTHD = root.findtext('body/items/item/NTK_MTHD')
                    app.setLabel("등록번호-1", "건강식품등록번호 : ")
                    app.setLabel("등록번호-2", PRMS_DT)
                    app.setLabel("이름-1", "식품명 : ")
                    app.setLabel("이름-2", PRDLST_NM)
                    app.setLabel("제조사/증상-1", "제조사 : ")
                    app.setLabel("제조사/증상-2", BSSH_NM)
                    app.setLabel("용도/복용방법-1", "복용 방법 : ")
                    app.setLabel("용도/복용방법-2", NTK_MTHD)
            main()

    # 불범약품 검색        
    elif app.getRadioButton("drug")=="부작용보고 약물검색":
        if app.getEntry("searching_option_item")=='':
            app.errorBox("경고", "검색창에 약물 이름을 입력해주세요.")
        else:
            illicit_drugs=app.getEntry("searching_option_item")
            itemname_encText = quote(illicit_drugs)
            decode_key = unquote('94G9o%2FpVMOcY%2F65ihjY%2FbXHetzaOK0ESh4bHnwaZPOrWDw0H5sGloaLcMRG2KRs70iLxGdPRDuZBNvLc%2BsG3fQ%3D%3D')    # 불법약품 API인증키
            baseurl = 'http://apis.data.go.kr/1470000/MdcinSdefctInfoService/getMdcinSdefctInfoList'            # 불법약품 기본 URL
            queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('col_001') : itemname_encText, quote_plus('col_002') : '', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '3' })
            url = baseurl + queryParams
            print(url)
            def main():
                global ITEM_NAME
                global ITEM_NAME_ENG
                global period_NAME
                global inflist
                data = urlopen(url).read()
                f = open('MdcinSdefct-db.xml','wb')         # 불법약품 XML파일 열기    
                f.write(data)
                f.close()
                tree = ET.parse('MdcinSdefct-db.xml')
                root = tree.getroot()
                items = root.findall('body/items/item')
                ITEM_NAME = root.findtext('body/items/item/COL_001')

                # 불법약품의 데이터가 잘못검색한 경우. 경고 문구 출력.
                if ITEM_NAME==None:
                    app.errorBox("경고","이름을 다시한번 확인해 주십시오.")

                # 검색한 불법약품 데이터 내용을 출력.
                else:
                    period_NAME = root.findtext('body/items/item/COL_004')
                    ITEM_NAME_ENG = root.findtext('body/items/item/COL_002')
                    app.setLabel("등록번호-1", '')
                    app.setLabel("등록번호-2", '')
                    app.setLabel("이름-1", "약품명 : ")
                    app.setLabel("이름-2", ITEM_NAME)
                    app.setLabel("제조사/증상-1", "약물 허용 기간 : ")
                    app.setLabel("제조사/증상-2", period_NAME)
                    app.setLabel("용도/복용방법-1", "부작용 : ")
                    information = tree.findall('.//body/items/item/COL_005')
                    inflist = [t.text for t in information]
                    app.setLabel("용도/복용방법-2", inflist)
            main()
'''
검색한 불법약품의 상세정보를 출력을 위해 wiki의 정보를 출력
불법약품의 XML정보를 찾은 후, 웹브라우저를 통해 상세불법약품의 내용을 출력.
'''
def openwiki(rb):       # 검색한 불법의약품정보를 가져와 wiki백과사전을 들어가기 위한 함수.   
    if app.getRadioButton("drug")=="부작용보고 약물검색":
        if app.getEntry("searching_option_item")=='':
            app.errorBox("경고", "검색창에 약물 이름을 입력해주세요.")
        else:
            searching(rb)

            # 찾은 불법약품의 정보를 한글 / 영문 wiki정보를 보기 위한 선택지.
            if app.getRadioButton("위키한영전환")=="한글위키":
                wiki_url = 'https://ko.wikipedia.org/wiki/' + ITEM_NAME
            elif app.getRadioButton("위키한영전환")=="영문위키":
                wiki_url = 'https://en.wikipedia.org/wiki/' + ITEM_NAME_ENG
            new = 2 # 새로운 웹브라우저를 띄워서 wiki백과사전 검색.
            webbrowser.open(wiki_url,new=new)
    else:
        app.errorBox("경고","부작용이 보고된 약물만 검색해주세요.")

def imagedownload(rb):      # 의약품의 이미지 다운 함수.
    if app.getEntry("searching_option_item")=='':
        app.errorBox("경고", "검색창에 약물을 입력해주세요.")
    else:
        if app.getRadioButton("drug")=='약품 이름검색':
            searching(rb)
            if ImageUrl==None:
                app.errorBox("경고","이름을 다시한번 확인해 주십시오.")
            else:
                print(ImageUrl)
                webbrowser.open_new(ImageUrl)
        else:
            app.errorBox("경고", "약품 이름 검색으로만 가능한 서비스입니다.")

def sendemailbutton(rb):        # 검색한 정보를 메일로 전송 함수.
    if app.getRadioButton("drug")=='약품 이름검색':
        if app.getLabel("이름-1")=='':
            app.errorBox("경고","먼저 검색을 하셔야합니다.")
        else:
            senderAddr = "drugdbkpu@gmail.com"
            recipientAddr=app.textBox("email 주소 입력", "이메일 주소를 입력해주세요.")

            # 메일 보내기를 취소한 경우.
            if recipientAddr==None:
                app.infoBox("취소", "전송이 취소되었습니다.")

            # 검색한 데이터가 의약물 일 경우. 보내는 메일의 내용.
            else:
                host = "smtp.gmail.com"
                port = "587"
                text = "약물 등록번호 : %s \n약물명 : %s \n제조사 : %s \n용도 : %s \n이미지 링크 : %s" %(ITEM_SEQ, ITEM_NAME, ENTP_NAME, CLASS_NAME, ImageUrl)
                msg = MIMEText(text)
                msg['To'] = senderAddr
                msg['From'] = recipientAddr
                msg['Subject'] = '약물 정보 공개'
                s = mysmtplib.MySMTP(host,port)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login("drugdbkpu@gmail.com","20152100511!")
                s.sendmail(senderAddr , [recipientAddr], msg.as_string())
                app.infoBox("전송","전송되었습니다.")
                s.close()
    if app.getRadioButton("drug")=='건강 식품검색':
        if app.getLabel("이름-1")=='':
            app.errorBox("경고","먼저 검색을 하셔야합니다.")
        else:
            senderAddr = "drugdbkpu@gmail.com"
            recipientAddr=app.textBox("email 주소 입력", "이메일 주소를 입력해주세요.")

            # 메일 보내기를 취소한 경우.
            if recipientAddr==None:
                app.infoBox("취소", "전송이 취소되었습니다.")

            # 검색한 데이터가 건강식품 보조제 일 경우. 보내는 메일의 내용.
            else:
                host = "smtp.gmail.com"
                port = "587"
                text = "식품 등록번호 : %s \n식품명 : %s \n제조사 : %s \n복용 방법 : %s" %(PRMS_DT, PRDLST_NM, BSSH_NM, NTK_MTHD)
                msg = MIMEText(text)
                msg['To'] = senderAddr
                msg['From'] = recipientAddr
                msg['Subject'] = '건강보조식품 정보 공개'
                s = mysmtplib.MySMTP(host,port)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login("drugdbkpu@gmail.com","20152100511!")
                s.sendmail(senderAddr , [recipientAddr], msg.as_string())
                app.infoBox("전송","전송되었습니다.")
    
    if app.getRadioButton("drug")=='부작용보고 약물검색':
        if app.getLabel("이름-1")=='':
            app.errorBox("경고","먼저 검색을 하셔야합니다.")
        else:
            senderAddr = "drugdbkpu@gmail.com"
            recipientAddr=app.textBox("email 주소 입력", "이메일 주소를 입력해주세요.")
            if recipientAddr==None:
                app.infoBox("취소", "전송이 취소되었습니다.")

            # 검색한 데이터가 불법약품 일 경우. 보내는 메일의 내용.
            else:
                host = "smtp.gmail.com"
                port = "587"
                text = "약물명 : %s \n약물 허용 기간 : %s \n증상 : %s" %(ITEM_NAME, period_NAME, inflist)
                msg = MIMEText(text)
                msg['To'] = senderAddr
                msg['From'] = recipientAddr
                msg['Subject'] = '부작용 약물 정보 공개'
                s = mysmtplib.MySMTP(host,port)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login("drugdbkpu@gmail.com","20152100511!")
                s.sendmail(senderAddr , [recipientAddr], msg.as_string())
                app.infoBox("전송","전송되었습니다.")

app.setFont("12", "맑은 고딕")      # 폰트 지정
app.addLabel("제목","의약품 & 보조식품 조회 App",1,0) # 프로그램 이름.
app.addEntry("searching_option_item",2,0)           # 검색 bar
app.addButton("검색",searching,2,1)                 # 검색 버튼 
app.setEntryDefault("searching_option_item", "　")
app.addLabel("f2", "검색할 환경을 선택하십시오.",3,0)   
app.addButton("설정", setting,3,1)                  # 설정버튼
app.addRadioButton("drug","약품 이름검색",4)
app.addRadioButton("drug","건강 식품검색",5) 
app.addRadioButton("drug","부작용보고 약물검색",6)
app.addLabel("등록번호-1", None,9,0)
app.addLabel("등록번호-2", None,9,1)
app.addLabel("이름-1", None,10,0)
app.addLabel("이름-2", None,10,1)
app.addLabel("제조사/증상-1",None,11,0)
app.addLabel("제조사/증상-2",None,11,1)
app.addLabel("용도/복용방법-1",None,12,0)
app.addLabel("용도/복용방법-2",None,12,1)
app.addButton("약품 이미지 다운로드",imagedownload,13,)
app.addButton("금지약물 위키피디아",openwiki,14,)
app.addRadioButton("위키한영전환", "한글위키",14,1)   # 한글 wiki선택
app.addRadioButton("위키한영전환", "영문위키",14,2)   # 영문 wiki선택
app.addButton("이메일전송",sendemailbutton,15,)       # 이메일 전송 버튼.
app.go()
