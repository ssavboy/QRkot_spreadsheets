from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.sevices.google_api import (set_user_permissions, spreadsheets_create,
                                    spreadsheets_update_value)

router = APIRouter()


@router.get(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service),
):
    closed_projects = (
        await charity_project_crud.get_projects_by_completion_rate(
            session=session
        )
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        report_spreadsheet_url = await spreadsheets_update_value(
            spreadsheet_id, closed_projects, wrapper_services
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return report_spreadsheet_url
