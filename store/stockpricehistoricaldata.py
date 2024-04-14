from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Date, DECIMAL, Float

Base = declarative_base()


class stock_price_historical_data(Base):
    __tablename__ = 'stock_price_historical_data'

    symbol = Column(Text, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(DECIMAL)
