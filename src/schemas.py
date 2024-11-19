from datetime import date
from decimal import Decimal
from typing import List, Dict

from pydantic import BaseModel, RootModel


class CargoRate(BaseModel):
    cargo_type: str
    rate: float


class DateRates(RootModel):
    root: Dict[date, List[CargoRate]]


class CalcPriceRequest(BaseModel):
    date: date
    cargo_type: str
    price: Decimal


class CalcPriceResponse(BaseModel):
    price: Decimal
