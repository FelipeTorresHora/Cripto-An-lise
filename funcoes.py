import requests
import pandas as pd
from datetime import datetime

# Função para obter dados históricos de preço da API CoinGecko
def obter_dados_criptomoeda(simbolo, intervalo='daily'):
    url = f'https://api.coingecko.com/api/v3/coins/{simbolo}/market_chart'
    if intervalo == '4h':
        params = {'vs_currency': 'usd', 'days': '365'}  # Intervalo de 4 horas não exige 'interval'
    elif intervalo == 'daily':
        params = {'vs_currency': 'usd', 'days': '365', 'interval': 'daily'}
    else:
        raise ValueError("Intervalo inválido. Escolha entre 'daily' ou '4h'.")

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")
    
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'close'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close']
    df = df[['date', 'close']].sort_values('date')
    
    return df

# Função para calcular bandas de Bollinger
def calcular_bandas_bollinger(df, periodo=20):
    df['SMA'] = df['close'].rolling(window=periodo).mean()
    df['STD'] = df['close'].rolling(window=periodo).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower Band'] = df['SMA'] - (df['STD'] * 2)
    return df

# Função para calcular o RSI com média de 14 períodos
def calcular_rsi(df, periodo=14):
    delta = df['close'].diff()
    ganhos = delta.where(delta > 0, 0)
    perdas = -delta.where(delta < 0, 0)
    
    ganho_medio = ganhos.rolling(window=periodo, min_periods=periodo).mean()
    perda_medio = perdas.rolling(window=periodo, min_periods=periodo).mean()
    
    rs = ganho_medio / perda_medio
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df
