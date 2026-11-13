from app.db.session import engine, Base
from app.db.models import DBStrategy, Trade  # Models import karna lazmi hai taake Base inhein recognize kare

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()