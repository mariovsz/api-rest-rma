from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...database import get_db
from ..paquetes import schemas, services

router = APIRouter()


@router.get(
    "/paquetes",
    response_model=schemas.PaqueteResponse,
    tags=["Paquetes"],
)
def read_paquetes(
    limit: int = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    nodo_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    data_min: Optional[float] = None,
    data_max: Optional[float] = None,
    order_by: Optional[str] = None,
    type: Optional[int] = None,
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    result = services.listar_paquetes(
        db,
        limit=limit,
        offset=offset,
        nodo_id=nodo_id,
        start_date=start_date,
        end_date=end_date,
        data_min=data_min,
        data_max=data_max,
        order_by=order_by,
        order=order,
        type=type,
    )
    return result


@router.get(
    "/paquetesarchivos",
    response_model=schemas.PaqueteArchivoResponse,
    tags=["Paquetes"],
)
def read_paquetes_archivos(
    limit: int = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    nodo_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    data_min: Optional[float] = None,
    data_max: Optional[float] = None,
    order_by: Optional[str] = None,
    type: Optional[int] = None,
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    result = services.listar_paquetes_archivo(
        db,
        limit=limit,
        offset=offset,
        nodo_id=nodo_id,
        start_date=start_date,
        end_date=end_date,
        data_min=data_min,
        data_max=data_max,
        order_by=order_by,
        order=order,
        type=type,
    )
    return result
