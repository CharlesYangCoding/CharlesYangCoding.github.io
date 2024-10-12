import requests
from bs4 import BeautifulSoup
import csv
 
def get_url(city_name):
    url = 'http://www.weather.com.cn/weather/'
    with open('C:/Users/User/Desktop/city.txt','r',encoding='utf-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if(city_name in line):
                code = line.split('=')[0].strip()
                return url + code + '.shtml'
    raise ValueError('invalid city name')
 
 
def get_content(url, data=None):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'
 
 
def get_data(html,city):
    final_list = []
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    lis = ul.find_all('li')
 
    for day in lis:
        temp_list = [city]
 
        date = day.find('h1').string
        temp_list.append(date)
 
        info = day.find_all('p')
        temp_list.append(info[0].string)
 
        if info[1].find('span') is None:
            temperature_highest = ' '
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', ' ')
 
        if info[1].find('i') is None:  #
            temperature_lowest = ' '
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃', ' ')
 
        temp_list.append(temperature_highest)
        temp_list.append(temperature_lowest)
 
        wind_scale = info[2].find('i').string
        temp_list.append(wind_scale)
 
        final_list.append(temp_list)
    return final_list
 
 
 
 
def save_data(data,filename):
    with open(filename,'a',errors='ignore',newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)
 
 
 
if __name__ == '__main__':
    cities = input('city name:').split()
    for city in cities:
        url = get_url(city)
        html = get_content(url)
        result = get_data(html,city)
        save_data(result,'C:/Users/User/Desktop/results.csv')
