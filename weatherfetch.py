import requests
import re


def fetch_weather(city):
    url = "http://www.weather.com.cn/weather/{}.shtml?".format(city)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.190 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding

        obj = re.compile(
            r'<li class="sky skyid .*?">.*?<h1>(?P<day>.*?)</h1>.*?'
            r'<p title="(?P<weather>.*?)" class="wea">.*?'
            r'<span>(?P<hightem>.*?)</span>/<i>(?P<lowtem>.*?)</i>.*?'
            r'<span title="(?P<wid>.*?)" class=.*?'
            r'></span>.*?<i><(?P<widlevel>.*?)</i>', re.S)

        result = obj.finditer(response.text)
        # 天气信息存储在一个列表中
        weather_data = []
        for item in result:
            weather_data.append((item.group("day"), item.group("weather"), item.group("hightem"),
                                 item.group("lowtem"), item.group("wid"), item.group("widlevel")))

        return weather_data

    except requests.exceptions.RequestException as e:
        raise Exception("Failed to fetch weather information. Error: " + str(e))


