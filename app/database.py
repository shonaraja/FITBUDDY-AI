from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from .config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(50))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    original_plan: Mapped[str] = mapped_column(Text)
    updated_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    nutrition_tip: Mapped[str] = mapped_column(Text)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(data: dict) -> User:
    with SessionLocal() as db:
        user = db.query(User).filter(User.user_id == data["user_id"]).first()
        if user:
            user.name = data["name"]
            user.age = data["age"]
            user.weight = data["weight"]
            user.goal = data["goal"]
            user.intensity = data["intensity"]
        else:
            user = User(**data)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user

def save_plan(user_id: str, original_plan: str, nutrition_tip: str) -> Plan:
    with SessionLocal() as db:
        plan = db.query(Plan).filter(Plan.user_id == user_id).first()
        if plan:
            plan.original_plan = original_plan
            plan.updated_plan = None
            plan.nutrition_tip = nutrition_tip
            plan.feedback = None
            plan.updated_at = None
        else:
            plan = Plan(
                user_id=user_id,
                original_plan=original_plan,
                nutrition_tip=nutrition_tip,
            )
            db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

def get_user(user_id: str) -> User | None:
    with SessionLocal() as db:
        return db.query(User).filter(User.user_id == user_id).first()

def get_plan(user_id: str) -> Plan | None:
    with SessionLocal() as db:
        return db.query(Plan).filter(Plan.user_id == user_id).first()

def get_original_plan(user_id: str) -> str | None:
    plan = get_plan(user_id)
    return plan.original_plan if plan else None

def update_plan(user_id: str, updated_plan: str, feedback: str, nutrition_tip: str) -> Plan | None:
    with SessionLocal() as db:
        plan = db.query(Plan).filter(Plan.user_id == user_id).first()
        if not plan:
            return None
        plan.updated_plan = updated_plan
        plan.feedback = feedback
        plan.nutrition_tip = nutrition_tip
        plan.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(plan)
        return plan

def get_all_users():
    with SessionLocal() as db:
        return db.query(User).order_by(User.created_at.desc()).all()

def get_all_plans():
    with SessionLocal() as db:
        return db.query(Plan).all()

def delete_user(user_id: str) -> bool:
    with SessionLocal() as db:
        user = db.query(User).filter(User.user_id == user_id).first()
        plan = db.query(Plan).filter(Plan.user_id == user_id).first()
        if not user:
            return False
        if plan:
            db.delete(plan)
        db.delete(user)
        db.commit()
        return True
