from sqlalchemy import create_engine
from store.stockpricehistoricaldata import stock_price_historical_data
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
dburl = os.environ.get('dburl')

engine = create_engine(f'mysql+pymysql://{dburl}')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

query = session.query(stock_price_historical_data)
result = query.all()

print(result)

