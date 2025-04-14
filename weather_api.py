import requests


class WeatherFetcher:
    def __init__(self, api_key):
        self.base_url = "https://api.waqi.info/feed/{}/?token={}"
        self.api_key = api_key

    def get_weather(self, city):
        url = self.base_url.format(city, self.api_key)
        try:
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'ok':
                return data['data']
            else:
                return None
        except Exception as e:
            print("Error fetching weather:", e)
            return None
