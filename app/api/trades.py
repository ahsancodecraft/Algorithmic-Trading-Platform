from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

from app.db.session import get_db
from app.db.models import Trade, DBStrategy  # <-- Yahan models import ho rahe hain, define nahi!

router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)

class TradeCreate(BaseModel):
    strategy_id: int
    symbol: str = Field(..., max_length=20)
    entry_price: Decimal
    exit_price: Decimal
    quantity: float
    pnl: Decimal

class TradeResponse(TradeCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    """
    Record a new trade execution for a strategy.
    """
    # Verify if strategy exists
    strategy = db.query(DBStrategy).filter(DBStrategy.id == trade.strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found."
        )
    
    db_trade = Trade(
        strategy_id=trade.strategy_id,
        symbol=trade.symbol,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        quantity=trade.quantity,
        pnl=trade.pnl
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

@router.get("/", response_model=List[TradeResponse])
def list_trades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all recorded trades.
    """
    trades = db.query(Trade).offset(skip).limit(limit).all()
    return trades