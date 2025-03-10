from sqlalchemy import Table, Column, TEXT, TIMESTAMP, MetaData
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import DATE
from datetime import datetime

Base = declarative_base()

metadata_obj = MetaData(schema="weather")

sensor_table = Table(
    "sensors",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("location", TEXT),
    Column("type", TEXT),
    Column("note", TEXT),
    Column("attached", TEXT),
    Column("install_date", DATE),
)

sensordata_table = Table(
    "sensordata",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("time", TIMESTAMP),
    Column("humidity", TEXT),
    Column("temperature", TEXT),
    Column("sensor", TEXT),
)


class SensorDataInput(BaseModel):
    time: datetime
    humidity: float = Field(..., ge=0, le=100)  # Humidity must be between 0-100%
    temperature: float
    sensor: str  # Sensor ID must match an existing sensor
