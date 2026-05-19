from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    phone = Column(String)
    booking_date = Column(String)
    service = Column(String)
    service_price = Column(String)
    stylist = Column(String)
    time = Column(String)
    note = Column(String)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    due_date = Column(String, default="")
    priority = Column(Integer, default=3)
    status = Column(String, default="pending")
    is_monitored = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
