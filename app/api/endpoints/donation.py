from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationDBFull,
                                  DonationDBPartial)
from app.sevices.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDBPartial,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation = await donation_crud.create(
        obj_in=donation, session=session, user=user, approved_commit=False
    )
    session.add_all(
        investing(
            target=donation,
            sources=await charity_project_crud.get_unclosed(session=session)
        )
    )
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=List[DonationDBPartial],
    response_model_exclude_none=True
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(user, session)
    return donations
