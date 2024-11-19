from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from database import generate_async_session
from models import RateModel
from schemas import DateRates, CalcPriceRequest, CalcPriceResponse

app = FastAPI()


@app.post("/rates/")
async def create_rates(date_rates: DateRates, db: Session = Depends(generate_async_session)):
    updates = []
    for date_key, cargo_rates in date_rates.root.items():
        for cargo_rate in cargo_rates:
            updates.append({
                "date": date_key,
                "cargo_type": cargo_rate.cargo_type,
                "rate": cargo_rate.rate
            })

    stmt = insert(RateModel).values(updates)
    stmt = stmt.on_conflict_do_update(
        index_elements=['date', 'cargo_type'],
        set_={'rate': stmt.excluded.rate}
    )
    await db.execute(stmt)
    await db.commit()


@app.post("/calculate_rate/")
async def calculate_rate(rate_request: CalcPriceRequest,
                         db: Session = Depends(generate_async_session)) -> CalcPriceResponse:
    result = await db.execute(
        select(RateModel).where(
            and_(RateModel.date == rate_request.date, RateModel.cargo_type == rate_request.cargo_type)
        )
    )
    rate = result.scalar_one_or_none()

    # Если ставка не найдена, поиск ставки для типа "Other"
    if not rate:
        result = await db.execute(
            select(RateModel).where(
                and_(RateModel.date == rate_request.date, RateModel.cargo_type == "Other")
            )
        )
        rate = result.scalar_one_or_none()

    # Если ставка для типа "Other" также не найдена, возвращаем ошибку
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found for the given date and type. Please try latter.")

    price = rate_request.price * rate.rate
    return CalcPriceResponse(price=price)
