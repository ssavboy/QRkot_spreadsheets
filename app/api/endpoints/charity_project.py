from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_edit, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.sevices.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        obj_in=charity_project, session=session, approved_commit=False
    )
    session.add_all(
        investing(
            target=new_project,
            sources=await donation_crud.get_unclosed(session=session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    full_amount = (
        obj_in.full_amount if obj_in.full_amount is not None else None
    )
    existing_project = await check_charity_project_edit(
        project_id, session, full_amount=full_amount
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if full_amount == existing_project.invested_amount:
        existing_project.full_amount = full_amount
        existing_project.invested_amount = existing_project.full_amount
        existing_project.fully_invested = True
        existing_project.close_date = datetime.now()
    return await charity_project_crud.update(
        existing_project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    existing_project = await check_charity_project_edit(
        project_id, session, delete=True
    )
    return await charity_project_crud.remove(
        existing_project, session
    )
