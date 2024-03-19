from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Date, Double, DECIMAL

Base = declarative_base()


class stock_price_historical_data(Base):
    __tablename__ = 'stock_price_historical_data'

    symbol = Column(Text, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Double)
    high = Column(Double)
    low = Column(Double)
    close = Column(Double)
    adj_close = Column(Double)
    volume = Column(DECIMAL)
