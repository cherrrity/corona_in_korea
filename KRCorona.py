#-*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from datetime import datetime


"""
확진일자
성별
생년
상세지역
"""
seoul_html = 'http://www.seoul.go.kr/coronaV/coronaStatus.do'
gyeonggi_html = 'https://www.gg.go.kr/bbs/boardView.do?bsIdx=464&bIdx=2296956&menuId=1535'
busan_html = 'http://www.busan.go.kr/corona/index.jsp'

chungnam_html = 'http://www.chungnam.go.kr/coronaStatus.do'

def chungnam():
    chungnam_json = OrderedDict()
    
    html = requests.get(chungnam_html).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('div.multiTabContents > div > div > ul > li.tabContents.active > table > tbody > tr:not(.detail)')

    cnt = len(datas)

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
                    dump["상세지역"] = area
                    
        sorted(dump.keys())        
        chungnam_json[str(cnt)] = dump
        cnt = cnt - 1
 
    print("chungnam is done..")
    return chungnam_json


def busan():
    busan_json = OrderedDict()
    
    html = requests.get(busan_html).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#contents > div > div.list_body > ul > li:first-child')

    cnt = len(datas)

    
    
    for data in datas:
        dump = OrderedDict()
        for da in data:
            d = da.text.split('\'',1)[1].split('/')
            
            dump["확진일"] = ''
            dump["성별"] = d[1].strip()
            
            if(int(d[0][:2]) > 20):
                dump["생년"] = int('19'+d[0].strip()[:2])
            else:
                dump["생년"] = int('20'+d[0].strip()[:2])

            dump["상세지역"] = d[2].strip()[:-1]

        sorted(dump.keys())  
        busan_json[str(cnt)] = dump
        cnt = cnt - 1
 
    print("busan is done..")
    return busan_json


def gyeonggi():
    """
    연번, 확진자 번호, 성별, 출생연도, 확진일자, 퇴원일자, 상세지역
    """
    gyeonggi_json = OrderedDict()
    
    html = requests.get(gyeonggi_html).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#quick3 > div > div:nth-child(3) > div > div > table > tbody > tr')

    
    cnt = len(datas)

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
            dump["상세지역"] = area
            
        sorted(dump.keys())  
        gyeonggi_json[str(cnt)] = dump
        cnt = cnt - 1
        
    print("gyeonggi is done..")
    return gyeonggi_json

def seoul():
    seoul_json = OrderedDict()
    
    html = requests.get(seoul_html).text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#move-cont1 > div:nth-child(2) > table > tbody > tr')

    cnt = len(datas)
    
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
                dump["상세지역"] = da.text
                if(da.text == '\xa0'):
                    dump["상세지역"] = "null"
                    
        sorted(dump.keys())  
        seoul_json[str(cnt)] = dump
        cnt = cnt - 1

    print("seoul is done..")
    return seoul_json




def main():
    total_json = OrderedDict()
    total_json["updated"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")


    #각 지역의 확진자 정보를 리턴받아 저장
    total_json["seoul"] = seoul()
    total_json["gyeonggi"] = gyeonggi()
    total_json["busan"] = busan()
    total_json["chungnam"] = chungnam()
    
    #print test
    #print(json.dumps(total_json, ensure_ascii=False, indent="\t") )
    
    #파일 생성
    with open('corona_in_korea.json','w', encoding="utf-8") as make_file:
        json.dump(total_json, make_file, ensure_ascii=False, indent="\t") 
    



if __name__ == "__main__":
	main()
