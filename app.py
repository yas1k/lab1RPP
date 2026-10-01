import os
from datetime import datetime

from flask import Flask, request
from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visit_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)


database_url = (
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

app = Flask(__name__)


@app.get("/hello")
def hello():
    visit = Visit(
        visit_time=datetime.now(),
        ip_address=request.remote_addr,
    )

    with Session() as session:
        session.add(visit)
        session.commit()

    return "Hello", 200
