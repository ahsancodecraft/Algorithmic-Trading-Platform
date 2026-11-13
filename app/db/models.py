from sqlalchemy import Column, Integer, String, Boolean, Float, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class DBStrategy(Base):
    __tablename__ = "strategies"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    symbol = Column(String, nullable=False)
    timeframe = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with trades
    trades = relationship("Trade", back_populates="strategy", cascade="all, delete-orphan")


class Trade(Base):
    __tablename__ = "trades"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String, nullable=False)
    entry_price = Column(Numeric(10, 2), nullable=False)
    exit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Float, nullable=False)
    pnl = Column(Numeric(10, 2), nullable=False)  # Net Profit and Loss for the trade
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to strategy
    strategy = relationship("DBStrategy", back_populates="trades")

# --- Aliases ---
DBTrade = Trade
DBTradeExecution = Trade