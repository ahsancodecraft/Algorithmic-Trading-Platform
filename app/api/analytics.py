from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict

from app.db.session import get_db
from app.services.analytics import calculate_strategy_performance, get_all_strategies_summary

router = APIRouter(
    prefix="/analytics",
    tags=["Performance Analytics"]
)

class StrategyPerformanceResponse(BaseModel):
    strategy_id: int
    strategy_name: str
    total_trades: int
    net_profit_loss: Decimal
    win_rate: float
    winning_trades: int
    losing_trades: int
    average_win: Decimal
    average_loss: Decimal

    model_config = ConfigDict(from_attributes=True)

class StrategySummaryResponse(BaseModel):
    strategy_id: int
    strategy_name: str
    symbol: str
    total_trades: int
    net_pnl: Decimal
    avg_pnl: Decimal

    model_config = ConfigDict(from_attributes=True)

@router.get("/strategies/{strategy_id}/performance", response_model=StrategyPerformanceResponse)
def get_strategy_performance(strategy_id: int, db: Session = Depends(get_db)):
    """
    Retrieve aggregated performance analytics report for a specific trading strategy
    computed via database aggregations (SUM, AVG, COUNT).
    """
    performance_data = calculate_strategy_performance(db, strategy_id)
    if not performance_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found."
        )
    return performance_data

@router.get("/strategies/summary", response_model=List[StrategySummaryResponse])
def get_strategies_summary(db: Session = Depends(get_db)):
    """
    Retrieve a performance summary leaderboard for ALL strategies using SQL GROUP BY.
    """
    summaries = get_all_strategies_summary(db)
    return summaries