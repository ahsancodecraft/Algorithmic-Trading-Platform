import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, DBStrategy, Trade
from app.services.analytics import calculate_strategy_performance

# Use an in-memory SQLite database for fast isolated unit testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for a test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_calculate_strategy_performance_empty(db_session):
    """Test performance analytics when a strategy has zero trades."""
    strategy = DBStrategy(name="Test Strategy", symbol="EURUSD", timeframe="1H", is_active=True)
    db_session.add(strategy)
    db_session.commit()
    db_session.refresh(strategy)

    result = calculate_strategy_performance(db_session, strategy.id)
    
    assert result["total_trades"] == 0
    assert result["net_profit_loss"] == Decimal("0.00")
    assert result["win_rate"] == 0.0

def test_calculate_strategy_performance_with_trades(db_session):
    """Test aggregated metrics (SUM, AVG, COUNT, Win Rate) with actual trades."""
    strategy = DBStrategy(name="Quant Trend", symbol="XAUUSD", timeframe="4H", is_active=True)
    db_session.add(strategy)
    db_session.commit()
    db_session.refresh(strategy)

    # Add winning trade
    trade1 = Trade(
        strategy_id=strategy.id,
        symbol="XAUUSD",
        entry_price=2000.00,
        exit_price=2050.00,
        quantity=1.0,
        pnl=50.00
    )
    # Add losing trade
    trade2 = Trade(
        strategy_id=strategy.id,
        symbol="XAUUSD",
        entry_price=2050.00,
        exit_price=2030.00,
        quantity=1.0,
        pnl=-20.00
    )
    db_session.add_all([trade1, trade2])
    db_session.commit()

    result = calculate_strategy_performance(db_session, strategy.id)

    assert result["total_trades"] == 2
    assert result["net_profit_loss"] == Decimal("30.00")  # 50.00 - 20.00
    assert result["winning_trades"] == 1
    assert result["losing_trades"] == 1
    assert result["win_rate"] == 50.0  # 1 win out of 2 = 50%
    assert result["average_win"] == Decimal("50.00")
    assert result["average_loss"] == Decimal("-20.00")