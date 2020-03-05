#-*- coding: utf-8 -*-


import requests
import urllib3
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from datetime import datetime
from requests import get

"""
확진일자
성별
생년
상세지역
"""
#서울
seoul_url = 'http://www.seoul.go.kr/coronaV/coronaStatus.do'
#경기
gyeonggi_url = 'https://www.gg.go.kr/bbs/boardView.do?bsIdx=464&bIdx=2296956&menuId=1535'
#부산
busan_url = 'http://www.busan.go.kr/corona/index.jsp'
#충남
chungnam_url = 'http://www.chungnam.go.kr/coronaStatus.do'
#경남
gyeongnam_url = 'http://www.gyeongnam.go.kr/corona.html'
#울산
ulsan_url = 'http://www.ulsan.go.kr/corona.jsp'

#강원도
chuncheon_url = 'https://www.chuncheon.go.kr/index.chuncheon?menuCd=DOM_000000599001000000' #춘천
wonju_url = 'https://www.wonju.go.kr/intro.jsp' #원주
gn_url = 'https://www.gn.go.kr/' #강릉
sokcho_url = 'http://www.sokcho.go.kr/portal/openinfo/sokchonews/corona19news' #속초

#제주
jeju_url = 'https://jeju.go.kr/api/article.jsp?board=corona_copper'
#대전
daejeon_url = 'https://www.daejeon.go.kr/corona19/index.do?tab=2&subTab=2'
#인천
incheon_url = 'https://www.incheon.go.kr/health/HE020409'
#전남광주
gwangju_url = 'https://www.gwangju.go.kr/'

def gwangju():
    gwangju_json = OrderedDict()
    gwangju_array = []


    html = requests.get(gwangju_url)
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, 'html.parser')
    datas = soup.select('body > table > tbody > tr:nth-child(odd)')

    cnt = len(datas)
    gwangju_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        data = data.text.strip().split('\n')
        dump = OrderedDict()

        if(data[3] != "-"):
            date = data[3].split(" ")
            month = date[0].replace("월","")
            day = date[1].replace("일","")
        
            if(len(day) < 2):
                day = "0"+day
            
            date = "2020.0"+month+"."+day
        else:
            date = "null"

        da = data[1].split(',')
        
        sex = da[0][-1]
        birth = 2020 - int(da[1].replace(' ', '')[:2])

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "광주광역시"
        dump["상세지역"] = "null"

        gwangju_array.append(dump)

    gwangju_json["patient"] = gwangju_array
    print("광주광역시 완료..")
    return gwangju_json

def incheon():
    incheon_json = OrderedDict()
    incheon_array = []

    html = requests.get(incheon_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#content > div.content-body > div > article > div > div:nth-child(5) .tbl > table > tbody > tr:nth-child(n+2)')

    cnt = len(datas)
    incheon_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        dump = OrderedDict()
        
        for da, i in zip(data, range(0, len(data))):
            da = da.text.replace(' ','')
            if( i == 2):
                d = da.split('/')
                
                #성별
                sex = d[0]

                #생년
                if(len(d[1]) > 2):
                    birth = 2020 - int(d[1][0:2])

                else:
                    birth = 2020 - int(d[1][0:1])
                    
                
            elif( i == 3):
                if(len(da.replace(' ', '')) > 3):
                    date = da.split('(')
                    date = date[0].split('.')
                    month = date[1]
                    day = date[2]
                    
                    if(len(day) < 2):
                        day = "0"+day
                        
                    date = "2020.0"+month+"."+day

        #상세지역
        area = "null"

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "인천"
        dump["상세지역"] = "null"

        incheon_array.append(dump)
        
    incheon_json["patient"] = incheon_array
    print("인천 완료..")
    return incheon_json


def daejeon():
    daejeon_json = OrderedDict()
    daejeon_array = []

    html = requests.get(daejeon_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#contBox > div.blog_borad > div.story_view > div > div:nth-child(1) > div > table > tbody > tr')

    cnt = len(datas)
    daejeon_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        dump = OrderedDict()
        data = data.text.strip().split('\n')

        #확진일
        date = data[2].split('.')
        month = date[0]
        day = date[1]
        if(len(day) < 2):
             day = "0"+day
        date = "2020.0"+month+"."+day

        da = data[3].split('(')
        
        #성별
        sex = da[0].strip()

        #생년
        birth = 2020 - int(da[1].strip()[:-2]) +5

        #상세지역
        area = data[4].strip()

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "대전"
        dump["상세지역"] = area

        daejeon_array.append(dump)

    daejeon_json["patient"] = daejeon_array
    print("대전 완료..")
    return daejeon_json

def jeju():
    jeju_json = OrderedDict()
    jeju_array = []

    datas = requests.get(jeju_url).text

    jeju_data = json.loads(datas)
    keys = ['add1', 'add3']

    date = ''
    sex = ''
    birth = 0
    area = 'null'

    cnt = len(jeju_data['articles'])
    jeju_json["total"] = cnt
    

    for data in jeju_data['articles']:
        dump = OrderedDict()
        da = data[keys[0]].split(',')
        
        if(len(da) > 1):
            sex = da[0][-1]
            birth = 2020 - int(da[1].strip()[:-1])
        else:
            sex = da[0][-2]
            birth = 2020 - 45

        date = data[keys[1]].split('.')
        day = date[1]
        if(len(day) < 2):
            day = "0"+day
        date = '2020.0' + date[0]+"."+day
        
        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "제주"
        dump["상세지역"] = area
        
        jeju_array.append(dump)
        
    jeju_json["patient"] = jeju_array
    print("제주도 완료..")
    return jeju_json


    


def gangwon():
    gangwon_json = OrderedDict()
    gangwon_array = []

    #확진자 수 합계
    cnt = 0
    
    date = ''
    sex = ''
    birth = 0
    area = ''
    
    #춘천 
    html = requests.get(chuncheon_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('tr.close')

    cnt = cnt + len(datas)
    gangwon_json["total"] = cnt

    

    for data in datas:
        dump = OrderedDict()
        data = data.text.strip().split('\n')

        #확진일
        date = '20'+data[3]

        da = data[1].split(',')
        
        #성별
        sex = da[0][-1]
        

        #생년(추정치)
        birth = 2020 - int(da[1][0:2]) + 5
        

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "강원도"
        dump["상세지역"] = "춘천"
        
        gangwon_array.append(dump)
    
    #원주
    urllib3.disable_warnings()    
    html = requests.get(wonju_url,  verify=False).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('.tab_obj ul li.item')


    cnt = cnt + len(datas)
    gangwon_json["total"] = cnt

    
    for data in datas:
        data = data.text.strip().split('\n')
        dump = OrderedDict()

        for da in data:
            if(da == ''):
                data.remove('')
    
        
        #확진일
        date = data[4].split('.')
        month = date[1]
        day = date[2]
        if(len(day) < 2):
             day = "0"+day
        if(len(month) < 2):
            month = "0"+month
            
        date = "2020."+month+"."+day

        da = data[6].split(',')
        
        #성별
        sex = da[1].replace(' ','')[:1]

        #생년(추정치)
        birth = int(da[0].strip()[:2])
        if( birth > 20):
            birth = 1900 + birth
        else:
            birth = 2000 + birth


        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "강원도"
        dump["상세지역"] = "원주"

        gangwon_array.append(dump)

    
    #강릉
    urllib3.disable_warnings()    
    html = requests.get(gn_url,  verify=False).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('div.itembox > ul > li > div.titlebox > ul')

    cnt = cnt + len(datas)
    gangwon_json["total"] = cnt

    for data in datas:
        data = data.text.strip().split('\n')
        dump = OrderedDict()

        #확진일
        date = data[9]

        da = data[1].split('/')
        
        #성별
        sex = da[1][:1]

        #생년(추정치)
        birth = 2020 - int(da[0][-3:-1]) + 5

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "강원도"
        dump["상세지역"] = "강릉"

        gangwon_array.append(dump)
       

    dump = OrderedDict()
    
    #속초
    dump["확진일"] = "2020.02.22"
    dump["성별"] = "여"
    dump["생년"] = 2020 - 35
    dump["지역"] = "강원도"
    dump["상세지역"] = "속초"
    
    gangwon_array.append(dump)

    dump = OrderedDict()

    dump["확진일"] = "2020.02.22"
    dump["성별"] = "남"
    dump["생년"] = 2020 - 25
    dump["지역"] = "강원도"
    dump["상세지역"] = "속초"
    
    gangwon_array.append(dump)


    dump = OrderedDict()
     #삼척
    dump["확진일"] = "2020.02.22"
    dump["성별"] = "남"
    dump["생년"] = 2020 - 20
    dump["지역"] = "강원도"
    dump["상세지역"] = "삼척"
    
    gangwon_array.append(dump)
    
    cnt = cnt + 3
    gangwon_json["total"] = cnt
    
    gangwon_json["patient"] = gangwon_array
    print("강원도 완료..")
    return gangwon_json


    

def ulsan():
    ulsan_json = OrderedDict()
    ulsan_array = []

    html = requests.get(ulsan_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#patients > tbody > tr#patient4')

    cnt = len(datas)
    ulsan_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        dump = OrderedDict()
        data = data.text.strip().split('\n')

        #확진일
        date = data[2].split('/')
        month = date[0]
        day = date[1]
        if(len(day) < 2):
             day = "0"+day
        date = "2020.0"+month+"."+day

        da = data[1].split('/')
    
        
        #성별
        sex = da[0].strip()

        #생년
        birth = 2020 - int(da[1].strip()[:-1]) 

        #상세지역
        area = da[2].strip()

        dump["확진일"] = date
        dump["성별"] = sex
        dump["생년"] = birth
        dump["지역"] = "울산"
        dump["상세지역"] = area

        ulsan_array.append(dump)

    ulsan_json["patient"] = ulsan_array
    print("울산 완료..")
    return ulsan_json


def gyeongnam():
    gyeongnam_json = OrderedDict()
    gyeongnam_array = []


    html = requests.get(gyeongnam_url)
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, 'html.parser')
    datas = soup.select('#patients > tbody > tr.patient')

    cnt = len(datas)
    gyeongnam_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        data = data.text.strip().split('\n')
        dump = OrderedDict()

        if(len(data[2]) >= 32):
            del data[2]

        for da,i in zip(data, range(0, len(data))):
            if(i == 4):
                date = da.split("/")
                month = date[0]
                day = date[1]
                if(len(day) < 2):
                    day = "0"+day
                date = "2020.0"+month+"."+day

            elif(i == 2):
                d = da.split(',')
                area = d[0].strip()
                sex = d[1].strip()
                birth = int(d[2].strip()[:1])
                if( birth > 20):
                    birth = 1900 + birth
                else:
                    birth = 2000 + birth

            dump["확진일"] = date
            dump["성별"] = sex
            dump["생년"] = birth
            dump["지역"] = "경상남도"
            dump["상세지역"] = area

        gyeongnam_array.append(dump)

    gyeongnam_json["patient"] = gyeongnam_array
    print("경상남도 완료..")
    return gyeongnam_json


def chungnam():
    chungnam_json = OrderedDict()
    chungnam_array = []

    html = requests.get(chungnam_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('div.multiTabContents > div > div > ul > li.tabContents.active > table > tbody > tr:not(.detail)')

    cnt = len(datas)
    chungnam_json["total"] = cnt

    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:
        dump = OrderedDict()
        for da, i in zip(data, range(0, len(data))):
            if(da != "\n"):
                if( i == 7):
                    date = da.text[3:-1]
                    if(len(date) < 2):
                        date = "0"+date

                    date = "2020.0" + da.text[0:1] + "."+ date

                elif( i == 3):
                    d = da.text.split(' ')

                    sex = d[1].strip()

                    if( d[1].find(',') > 0):
                        sex = sex[:-1]

                    birth = 2020 - int(d[2].strip()[:-1])

                    area = d[0].strip()[:-1]

                    dump["확진일"] = date
                    dump["성별"] = sex
                    dump["생년"] = birth
                    dump["지역"] = "충청남도"
                    dump["상세지역"] = area

        chungnam_array.append(dump)

    chungnam_json["patient"] = chungnam_array
    print("충청남도 완료..")
    return chungnam_json


def busan():
    busan_json = OrderedDict()
    busan_array = []

    html = requests.get(busan_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#contents > div:nth-child(1) > div > div.list_body > ul > li:first-child')

    cnt = len(datas)
    busan_json["total"] = cnt


    for data in datas:
        dump = OrderedDict()
        for da in data:
            d = da.text.split('(',1)[1].split('/')

            dump["확진일"] = 'null'
            dump["성별"] = d[1].strip()

            dump["생년"] = int(d[0].strip()[:-2])
            dump["지역"] = "부산"
            dump["상세지역"] = d[2].strip()[:-1]


        busan_array.append(dump)

    busan_json["patient"] = busan_array
    print("부산 완료..")
    return busan_json


def gyeonggi():
    """
    연번, 확진자 번호, 성별, 출생연도, 확진일자, 퇴원일자, 상세지역
    """
    gyeonggi_json = OrderedDict()
    gyeonggi_array = []

    html = requests.get(gyeonggi_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#quick3 > div > div:nth-child(3) > div > div > table > tbody > tr')


    cnt = len(datas)
    gyeonggi_json["total"] = cnt


    date = ''
    sex = ''
    birth = 0
    area = ''

    for data in datas:

        data = data.text.strip().split('\n')
        dump = OrderedDict()

        for da, i in zip(data, range(0, len(data))):
            if( i == 4):
                day = da[2:]
                if(len(day) < 2):
                    day = "0"+day
                date = '2020.0' + da[:1] +"."+ day

            elif( i == 2):
                sex = da
            elif( i == 3 ):
                birth = int(da[1:])
                if( birth > 20):
                    birth = 1900 + birth
                else:
                    birth = 2000 + birth
            elif( i == 6):
                area = da;
                if(da == '\xa0'):
                    area = "null"

            dump["확진일"] = date
            dump["성별"] = sex
            dump["생년"] = birth
            dump["지역"] = "경기도"
            dump["상세지역"] = area

        gyeonggi_array.append(dump)

    gyeonggi_json["patient"] = gyeonggi_array
    print("경기도 완료..")
    return gyeonggi_json


def seoul():
    seoul_json = OrderedDict()
    seoul_array = []

    html = requests.get(seoul_url).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#move-cont1 > div:nth-child(2) > table > tbody > tr')

    cnt = len(datas)
    seoul_json["total"] = cnt

    for data in datas:
        dump = OrderedDict()
        for da, i in zip(data, range(0, len(data))):

            if( i == 2):
                date = da.text.split('.',1)
                if(len(date[1][:-1]) < 2):
                    day = "0"+date[1][:-1]
                date = '2020.0' + date[0] +"."+ day
                dump["확진일"] = date
            elif( i == 3):
                dump["성별"] = da.text[:1]
                if(int(da.text[-3:-1]) > 20):
                    dump["생년"] = int('19'+da.text[-3:-1])
                else:
                    dump["생년"] = int('20'+da.text[-3:-1])
            elif( i == 4):
                dump["지역"] = "서울"
                dump["상세지역"] = da.text
                if(da.text == '\xa0'):
                    dump["상세지역"] = "null"

        seoul_array.append(dump)

    seoul_json["patient"] = seoul_array
    print("서울 완료..")
    return seoul_json




def main():
    total_json = OrderedDict()
    total_json["updated"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    total_json["area"] = ["seoul", "gyeonggi" , "busan", "chungnam","gyeongnam","ulsan","gangwon","jeju","daejeon","incheon","gwangju"]

    #각 지역의 확진자 정보를 리턴받아 저장
    
    total_json["seoul"] = seoul() #서울
    total_json["gyeonggi"] = gyeonggi() #경기
    total_json["busan"] = busan() #부산
    total_json["chungnam"] = chungnam() #충남
    total_json["gyeongnam"] = gyeongnam() #경남
    total_json["ulsan"] = ulsan() #울산
    total_json["gangwon"] = gangwon() # 강원
    total_json["jeju"] = jeju() # 제주
    total_json["daejeon"] = daejeon() # 대전
    total_json["incheon"] = incheon() # 인천
    total_json["gwangju"] = gwangju() # 광주
    
    #print test
    #print(json.dumps(total_json, ensure_ascii=False, indent="\t") )

    #파일 생성
    with open('corona_in_korea.json','w', encoding="utf-8") as make_file:
        json.dump(total_json, make_file, ensure_ascii=False, indent="\t")
    

    print("파일생성 완료...")
    
if __name__ == "__main__":
	main()
