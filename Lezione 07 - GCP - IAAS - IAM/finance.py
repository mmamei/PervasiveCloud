import yfinance as yf
import datetime
start_ts = datetime.date.today() - datetime.timedelta(days = 2)
ticker = 'PHAU.L'
data = yf.download(ticker, start=start_ts).reset_index()
print(data)


