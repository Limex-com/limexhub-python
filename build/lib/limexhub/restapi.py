import requests
import pandas as pd
from typing import Optional,Dict
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
 
class RestAPI:
    def __init__(self, base_url="https://hub.limex.com/v1", token=None):
        self.base_url = base_url
        self.token = token
        self.session = self._create_session()
        
    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  
            backoff_factor=1, 
            status_forcelist=[500, 502, 503, 504], 
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session        
 
    def _get(self, endpoint, params: Dict):
        params['token'] = self.token
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request to {endpoint} failed: {e}")
            raise 

    def instruments(self, assets=None):
        endpoint = "instruments"
        params = {'assets': assets}
        return pd.DataFrame(self._get(endpoint, params=params))
   
    def candles(self, symbols, start='2025-01-01', end=None, interval='1d', pivot=False):
        if end is None:
            end = datetime.today().strftime('%Y-%m-%d')
        if isinstance(symbols, str):
            symbols = [symbols]
        endpoint = "bars"
        params = {
            "symbols": ",".join(symbols),
            "timeframe": interval,
            "from": start,
            "to": end
        }
        raw = self._get(endpoint, params=params)
        columns = raw["columns"]
        index = raw["index"]
        data = raw["data"]
        records = []
        for (symbol, timestamp), row in zip(index, data):
            date = pd.to_datetime(timestamp, unit="ms")
            rec = {"symbol": symbol, "Date": date}
            rec.update(dict(zip(columns, row)))
            records.append(rec)
        df = pd.DataFrame(records)
        df.set_index(["Date", "symbol"], inplace=True)
        df.sort_index(inplace=True)
        if pivot:
            df = df.unstack(level=-1)
            # Переставим уровень колонок для совместимости с yf
            df.columns = pd.MultiIndex.from_tuples([(col[1], col[0]) for col in df.columns])
            df = df.sort_index(axis=1)
        return df
   

    def fundamental(self, symbol='', from_date='2020-01-01',to_date=datetime.today().strftime('%Y-%m-%d'), fields='ebitda', quarter='Q2-2023'):
        endpoint = "fundamental"
        if symbol=='':
            params = {'from': from_date,'to': to_date, 'fields': fields,'quarter': quarter}
        else:
            params = {'symbol': symbol, 'from': from_date,'to': to_date, 'fields': fields}            
        res = pd.DataFrame(self._get(endpoint, params=params))
        if len(res)>0:
            res['date'] = pd.to_datetime(res['date'], utc=True).dt.date
        return res
   
    def news(self, symbol, from_date='2020-01-01',to_date=datetime.today().strftime('%Y-%m-%d')):
        endpoint = "news"
        params = {'symbol': symbol, 'from': from_date,'to': to_date}
        res = pd.DataFrame(self._get(endpoint, params=params))
        res['created'] = pd.to_datetime(res['created'], utc=True)
        return res
   
    def events(self, symbol, from_date='2020-01-01',to_date=datetime.today().strftime('%Y-%m-%d'), event_type='dividends'):
        endpoint = "events"
        params = {'symbol': symbol, 'from': from_date, 'to': to_date,'type': event_type}
        res = pd.DataFrame(self._get(endpoint, params=params))
        res['buy_date'] = pd.to_datetime(res['buy_date'], utc=True).dt.date
        return res
   
    def signals(self, vendor='boosted', model='50678d2d-fd0f-4841-aaee-7feac83cb3a1', symbol='', from_date='2020-01-01',to_date=datetime.today().strftime('%Y-%m-%d')):
        endpoint = "signals"
        if symbol=='':
            params = {'vendor': vendor, 'model': model, 'from': from_date,'to': to_date}
        else:
            params = {'vendor': vendor, 'model': model, 'symbol': symbol, 'from': from_date,'to': to_date}
        res = pd.DataFrame(self._get(endpoint, params=params))
        res['trade_date'] = pd.to_datetime(res['trade_date'], utc=True).dt.date
        res = res.set_index('trade_date')
        res.index.name = 'Date'
        return res
 
    def models(self, vendor='boosted'):
        endpoint = "models"
        params = {'vendor': vendor}
        return pd.DataFrame(self._get(endpoint, params=params))   
    
    def constituents(self, index='SP500'):
        endpoint = "constituents"
        params = {'index': index}
        return pd.DataFrame(self._get(endpoint, params=params))     

    def altercandles(self, symbol, from_date='2020-01-01',to_date=datetime.today().strftime('%Y-%m-%d'), timeframe=3):
        endpoint = "altercandles"
        params = {'symbol': symbol, 'to': to_date, 'from': from_date, 'timeframe': timeframe}
        res = pd.DataFrame(self._get(endpoint, params=params))
        if timeframe>=3:
            res['ts'] = pd.to_datetime(res['ts'], utc=True).dt.date
        else:
            res['ts'] = pd.to_datetime(res['ts'], utc=True)
        return res.sort_values(by=['ts'])
 
# if __name__ == "__main__":    
    # api = RestAPI(token="")
    # tickers = ['AAPL', 'MSFT']
    # candles = api.candles(tickers, from_date="2025-10-12", to_date="2025-10-15" )
    # client.fundamental('')
    # client.signals(symbol="")