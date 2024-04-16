from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Date, BIGINT

Base = declarative_base()


class MarketCapHistoricalData(Base):
    __tablename__ = 'market_cap_historical_data'

    symbol = Column(Text, primary_key=True)
    date = Column(Date, primary_key=True)
    market_cap = Column(BIGINT)
