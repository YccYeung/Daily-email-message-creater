import random
import csv
from urllib import request
import json
import datetime

def get_random_quote(quotes_file = 'quote.csv'):

    try:
        with open(quotes_file) as csvfile:
            for line in csv.reader(csvfile, delimiter = '|'):
                quote = [{'author': line[0],
                          'quote': line[1]
                          }]

    except Exception as e:
        quote = [{'author': "Justin",
                  'quote': "I am the best in the world"}]


    return random.choice(quote)

def get_weather_forecast(coords = {'lat':43.334705, 'lon':-90.386793}):

    try:
        api_key = '38f6d66be79e5d24c4fc417eb730c9b2'
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {
                'city':data['city']['name'],
                'country':data['city']['country'],
                'periods':list()
        }

        for period in data['list'][0:8]:
            forecast['periods'].append({
                'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                'temp': round(period['main']['temp']),
                'description': period['weather'][0]['description'].title(),
                'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})

        return forecast

    except Exception as e:
        print(e)

def get_wikipedia_article():

    try:

        data = json.load(request.urlopen("https://en.wikipedia.org/api/rest_v1/page/random/summary"))
        return  {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}

    except Exception as e:
        print(e)

if __name__ == '__main__':
    pass
