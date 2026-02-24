from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

DETAILS = {
    'duplicate_project_name': 'Проект с таким именем уже существует!',
    'project_not_found': 'Проект не найден!',
    'cannot_update_closed_project': 'Закрытый проект нельзя редактировать!',
    'cannot_change_amount': 'Нельзя установить требуемую сумму меньше уже '
                            'вложенной.',
    'cannot_delete': 'В проект были внесены средства, не подлежит удалению!',
}


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail=DETAILS['duplicate_project_name'],
        )


async def check_charity_project_edit(
    project_id: int,
    session: AsyncSession,
    full_amount: int = None,
    delete: bool = False
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=DETAILS['project_not_found']
        )
    if project.fully_invested and not delete:
        raise HTTPException(
            status_code=400,
            detail=DETAILS['cannot_update_closed_project']
        )
    if full_amount and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=DETAILS['cannot_change_amount']
        )
    if delete and project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail=DETAILS['cannot_delete']
        )
    return project
