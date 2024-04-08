import requests
from typing import Optional,Dict
 
class LimexAPI:
    def __init__(self, base_url="https://hub.limex.com/v1", token=None):
        self.base_url = base_url
        self.token = token
 
    def _get(self, endpoint, params: Dict):
        params['token'] = self.token
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def instruments(self, assets=None):
        endpoint = "instruments"
        params = {'assets': assets}
        return self._get(endpoint, params=params)
   
    def candles(self, symbol, to_date, from_date, timeframe):
        endpoint = "candles"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date, 'timeframe': timeframe}
        return self._get(endpoint, params=params)
   
    def fundamental(self, symbol, to_date, from_date, fields):
        endpoint = "fundamental"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date, 'fields': fields}
        return self._get(endpoint, params=params)
   
    def news(self, symbol, to_date, from_date):
        endpoint = "news"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date}
        return self._get(endpoint, params=params)
   
    def events(self, symbol, to_date, from_date, event_type):
        endpoint = "events"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date, 'type': event_type}
        return self._get(endpoint, params=params)
   
    def signals(self, vendor, model, symbol, from_date):
        endpoint = "signals"
        params = {'vendor': vendor, 'model': model, 'symbol': symbol, 'from': from_date}
        return self._get(endpoint, params=params)
 
    def models(self, vendor):
        endpoint = "models"
        params = {'vendor': vendor}
        return self._get(endpoint, params=params)

    def altercandles(self, symbol, to_date, from_date, timeframe):
        endpoint = "altercandles"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date, 'timeframe': timeframe}
        return self._get(endpoint, params=params)      
 