from fastapi import APIRouter, Depends, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import sensor_table
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy import select

router = APIRouter()


# Get sensors using any combination of filters
@router.get("/api/sensors/")
async def get_sensors(
    id: Optional[str] = Query(None),
    coords: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    note: Optional[str] = Query(None),
    attached: Optional[str] = Query(None),
    install_date_from: Optional[date] = Query(None),
    install_date_to: Optional[date] = Query(None),
    fields: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    valid_fields = set(sensor_table.columns.keys())

    if fields:
        invalid_fields = [f for f in fields if f not in valid_fields]
        if invalid_fields:
            raise HTTPException(
                status_code=400, detail=f"Invalid fields: {', '.join(invalid_fields)}"
            )
        selected_fields = [sensor_table.c[f] for f in fields]
    else:
        selected_fields = [sensor_table]

    query = select(*selected_fields)
    filters = []
    if id:
        filters.append(sensor_table.c.id == id)

    if coords:
        filters.append(sensor_table.c.coords == coords)

    if type:
        filters.append(sensor_table.c.type == type)

    if note:
        filters.append(sensor_table.c.note == note)

    if attached:
        filters.append(sensor_table.c.attached == attached)

    if install_date_from:
        filters.append(sensor_table.c.install_date >= install_date_from)

    if install_date_to:
        filters.append(sensor_table.c.install_date <= install_date_to)

    if install_date_from and install_date_to and install_date_from > install_date_to:
        raise HTTPException(
            status_code=400, detail="install_date_from must be before install_date_to"
        )

    if filters:
        query = query.where(*filters)

    result = await db.execute(query)
    sensors = result.mappings().all()
    return [dict(row) for row in sensors]
