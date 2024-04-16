from sqlalchemy import create_engine
from store.stockpricehistoricaldataentity import StockPriceHistoricalData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
dburl = os.environ.get('dburl')

engine = create_engine(f'mysql+pymysql://{dburl}')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

query = session.query(StockPriceHistoricalData)
result = query.all()

print(result)

