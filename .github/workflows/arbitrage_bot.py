import ccxt, os, requests, time

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def alert(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")

exchange = ccxt.binance()
triangles = [('BTC', 'USDT', 'ETH'), ('ETH', 'BNB', 'BTC')]

while True:
    for a, b, c in triangles:
        try:
            ab = exchange.fetch_ticker(f'{a}/{b}')['ask']
            bc = exchange.fetch_ticker(f'{b}/{c}')['ask']
            ca = exchange.fetch_ticker(f'{c}/{a}')['bid']
            profit = (1/ab)*(1/bc)*ca - 1
            if profit > 0.005:
                alert(f"🚀 {a}→{b}→{c}→{a}: {profit:.2%}")
        except:
            pass
    time.sleep(60)
