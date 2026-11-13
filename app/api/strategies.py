from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.db.session import get_db
from app.db.models import DBStrategy

router = APIRouter(
    prefix="/strategies",
    tags=["Strategies"]
)

class StrategyCreate(BaseModel):
    name: str = Field(..., max_length=50)
    symbol: str = Field(..., max_length=20)
    timeframe: str = Field(..., max_length=10)

class StrategyResponse(StrategyCreate):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    """
    Create a new trading strategy.
    """
    # Check if strategy with the same name already exists
    existing = db.query(DBStrategy).filter(DBStrategy.name == strategy.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Strategy with this name already exists."
        )
    
    db_strategy = DBStrategy(
        name=strategy.name,
        symbol=strategy.symbol,
        timeframe=strategy.timeframe,
        is_active=True
    )
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.get("/", response_model=List[StrategyResponse])
def list_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all created trading strategies.
    """
    strategies = db.query(DBStrategy).offset(skip).limit(limit).all()
    return strategies

@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific trading strategy by its ID.
    """
    strategy = db.query(DBStrategy).filter(DBStrategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found."
        )
    return strategy