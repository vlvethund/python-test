from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()
dburl = os.environ.get('dburl')

engine = create_engine(f'mysql+pymysql://{dburl}')

connect = engine.connect()

cursor = connect.execute(text("select * from auto_stock.stock_price_historical_data where symbol = 'AAPL';"))

result = cursor.fetchall()
print(result[0][1])

