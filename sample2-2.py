from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from xml.etree.ElementTree import parse
class GetData:
    choosenumber=int(input("건강식품을 검색합니다. 1을 입력하면 약품이름검색, 2는 회사로 검색합니다. :"))
    if choosenumber==1:
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
            print("결과 XML을 파싱하였습니다.")
    elif choosenumber==2:
        entpname=str(input("회사 이름을 입력합니다 : "))
        decode_key = unquote('Bw24TtXAIcROPn%2FcAPiatMkvhPRC6KbKXX%2BIaV%2FVN5fy3GgNB8Tj92PS6FNoHDb1GV2W2v%2FtZT4HvX9x3SmWmA%3D%3D')
        baseurl = 'http://apis.data.go.kr/1470000/HtfsTrgetInfoService/getHtfsInfoList'
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : decode_key, quote_plus('prdlst_nm') : '', quote_plus('bssh_nm') : entpname, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1' })
        url = baseurl+queryParams
        print(url)
        def main(self):
            data=urlopen(self.url).read()
            #print(data)
            f=open("htfs-db-entpname.xml","wb")
            f.write(data)
            f.close()
            print("결과 XML을 파싱하였습니다.")
getData=GetData()
getData.main()
