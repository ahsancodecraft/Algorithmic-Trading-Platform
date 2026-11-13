from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Trade, DBStrategy
from decimal import Decimal

def calculate_strategy_performance(db: Session, strategy_id: int):
    """
    Computes advanced aggregated performance metrics for a specific strategy
    using SQL aggregation functions (SUM, AVG, COUNT).
    """
    strategy = db.query(DBStrategy).filter(DBStrategy.id == strategy_id).first()
    if not strategy:
        return None

    total_trades = db.query(func.count(Trade.id)).filter(Trade.strategy_id == strategy_id).scalar() or 0

    if total_trades == 0:
        return {
            "strategy_id": strategy.id,
            "strategy_name": strategy.name,
            "total_trades": 0,
            "net_profit_loss": Decimal("0.00"),
            "win_rate": 0.0,
            "winning_trades": 0,
            "losing_trades": 0,
            "average_win": Decimal("0.00"),
            "average_loss": Decimal("0.00")
        }

    net_pnl = db.query(func.sum(Trade.pnl)).filter(Trade.strategy_id == strategy_id).scalar() or Decimal("0.00")

    winning_trades = db.query(func.count(Trade.id)).filter(
        Trade.strategy_id == strategy_id, 
        Trade.pnl > 0
    ).scalar() or 0

    losing_trades = db.query(func.count(Trade.id)).filter(
        Trade.strategy_id == strategy_id, 
        Trade.pnl < 0
    ).scalar() or 0

    win_rate = (float(winning_trades) / float(total_trades)) * 100.0 if total_trades > 0 else 0.0

    avg_win = db.query(func.avg(Trade.pnl)).filter(
        Trade.strategy_id == strategy_id, 
        Trade.pnl > 0
    ).scalar() or Decimal("0.00")

    avg_loss = db.query(func.avg(Trade.pnl)).filter(
        Trade.strategy_id == strategy_id, 
        Trade.pnl < 0
    ).scalar() or Decimal("0.00")

    return {
        "strategy_id": strategy.id,
        "strategy_name": strategy.name,
        "total_trades": total_trades,
        "net_profit_loss": round(net_pnl, 2),
        "win_rate": round(win_rate, 2),
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "average_win": round(avg_win, 2),
        "average_loss": round(avg_loss, 2)
    }

def get_all_strategies_summary(db: Session):
    """
    Retrieves performance summary for ALL strategies grouped together 
    using SQL GROUP BY and aggregation functions.
    """
    results = db.query(
        DBStrategy.id.label("strategy_id"),
        DBStrategy.name.label("strategy_name"),
        DBStrategy.symbol.label("symbol"),
        func.count(Trade.id).label("total_trades"),
        func.coalesce(func.sum(Trade.pnl), Decimal("0.00")).label("net_pnl"),
        func.coalesce(func.avg(Trade.pnl), Decimal("0.00")).label("avg_pnl")
    ).outerjoin(Trade, DBStrategy.id == Trade.strategy_id)\
     .group_by(DBStrategy.id, DBStrategy.name, DBStrategy.symbol)\
     .all()
    
    summaries = []
    for r in results:
        summaries.append({
            "strategy_id": r.strategy_id,
            "strategy_name": r.strategy_name,
            "symbol": r.symbol,
            "total_trades": r.total_trades,
            "net_pnl": round(r.net_pnl, 2),
            "avg_pnl": round(r.avg_pnl, 2)
        })
    return summaries