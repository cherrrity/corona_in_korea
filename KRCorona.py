#-*- coding: utf-8 -*-


import requests
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
seoul_url = 'http://www.seoul.go.kr/coronaV/coronaStatus.do'
gyeonggi_url = 'https://www.gg.go.kr/bbs/boardView.do?bsIdx=464&bIdx=2296956&menuId=1535'
busan_url = 'http://www.busan.go.kr/corona/index.jsp'
chungnam_url = 'http://www.chungnam.go.kr/coronaStatus.do'
gyeongnam_url = 'http://www.gyeongnam.go.kr/corona.html'

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
    datas = soup.select('#contents > div > div.list_body > ul > li:first-child')

    cnt = len(datas)
    busan_json["total"] = cnt

    
    for data in datas:
        dump = OrderedDict()
        for da in data:
            d = da.text.split('(',1)[1].split('/')
            
            dump["확진일"] = ''
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
                   dump["확진일"] = '2020.'+da.text[:-1]
            elif( i == 3):
                dump["성별"] = da.text[:1]
                if(int(da.text[3:5]) > 20):
                    dump["생년"] = int('19'+da.text[3:5])
                else:
                    dump["생년"] = int('20'+da.text[3:5])
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
    total_json["area"] = ["seoul", "gyeonggi" , "busan", "chungnam","gyeongnam"]
    
    #각 지역의 확진자 정보를 리턴받아 저장
    total_json["seoul"] = seoul()
    total_json["gyeonggi"] = gyeonggi()
    total_json["busan"] = busan()
    total_json["chungnam"] = chungnam()
    total_json["gyeongnam"] = gyeongnam()


    
    #print test
    #print(json.dumps(total_json, ensure_ascii=False, indent="\t") )
    
    #파일 생성
    with open('corona_in_korea.json','w', encoding="utf-8") as make_file:
        json.dump(total_json, make_file, ensure_ascii=False, indent="\t") 
    



if __name__ == "__main__":
	main()
