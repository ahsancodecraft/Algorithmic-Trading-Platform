# 🚀 Algorithmic Trading Strategy & Performance Analytics Platform

An institutional-grade engineering project blueprint covering relational databases, SQLAlchemy ORM, Alembic migrations, advanced SQL aggregations (`SUM`, `AVG`, `COUNT`, `GROUP BY`), ACID transaction safety, and FastAPI execution pipelines for MT5, cTrader, and Pine Script models.

---

## 🛠️ Technology Stack

| Layer | Suggested Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.12+ | Application logic, OOP domain models, and quantitative math |
| **API Framework** | FastAPI | HTTP routes, request/response validation, interactive Swagger docs |
| **Validation** | Pydantic | Validate API payloads and configuration schemas |
| **Database** | PostgreSQL | Durable relational storage for high-frequency logs and strategies |
| **ORM / Migrations** | SQLAlchemy 2.x / Alembic | Map Python classes to relational tables; version-control schema changes safely |
| **Testing** | pytest | Unit, integration, and aggregation accuracy tests |
| **Environment** | venv + .env + python-dotenv | Isolate dependencies and secure database connection strings |

---

## 📊 Core Features & Functional Requirements

* **Strategy Registry:** Create, edit, activate, or deactivate trading strategies (e.g., EMA Crossover, MACD, cBots, Pine Scripts).
* **Backtest Management:** Store historical simulation results linked directly to strategy definitions.
* **Execution Logging:** Capture every individual buy/sell trade ticket securely with exact `Decimal` precision.
* **Performance Analytics & Grouping:** Expose aggregated metrics (`SUM`, `AVG`, `COUNT`, `GROUP BY`) for single strategies and multi-strategy summary leaderboards.
* **Server Restart Resilience:** Durable PostgreSQL relational storage ensuring session history survives server restarts.

---

## 📂 Project Structure

```text
Algorithmic-Trading-Platform/
├── alembic/              # Database migration versions and config
├── app/
│   ├── api/              # FastAPI routers (strategies.py, trades.py, analytics.py)
│   ├── db/               # Database session & models
│   ├── services/         # Business & quantitative logic (analytics service)
│   └── main.py           # FastAPI application entry point
├── tests/                # Automated pytest suite (unit & integration tests)
├── .env                  # Environment variables (Database URL)
├── .gitignore            # Ignored files (venv, pycache, .env)
└── alembic.ini           # Alembic configuration

⚙️ Getting Started & Installation
1. Clone the Repository
Bash
git clone [https://github.com/ahsancodecraft/Algorithmic-Trading-Platform.git](https://github.com/ahsancodecraft/Algorithmic-Trading-Platform.git)
cd Algorithmic-Trading-Platform
2. Create and Activate Virtual Environment
Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
3. Install Dependencies
Python
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic alembic pytest httpx python-dotenv
4. Configure Environment Variables (.env)
Create a .env file in the root directory and add your PostgreSQL connection string:

Code snippet
DATABASE_URL=postgresql+psycopg2://postgres:your_password@127.0.0.1:5433/Algorithmic_Trading_Platform_db
5. Run Database Migrations
Bash
alembic upgrade head
6. Run the FastAPI Server
Bash
python -m uvicorn app.main:app --reload --port 8080
Access Interactive Swagger Documentation at: http://127.0.0.1:8080/docs

🧪 Running Automated Tests
Execute the comprehensive test suite using pytest:

Bash
python -m pytest -v
🛡️ Institutional Compliance & Safety
Exact Financial Math: Utilizes Python's Decimal and SQL NUMERIC types to completely prevent compounding floating-point rounding errors in PnL calculations.

ACID Transactions: Ensures multi-step trade execution logging and state consistency.

Developed as part of Titan Quant Research Lab Quantitative Backend Masterclass.