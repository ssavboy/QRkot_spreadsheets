from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        projects = (
            select(
                CharityProject,
                (
                    func.strftime("%s", CharityProject.close_date).__sub__(
                        func.strftime("%s", CharityProject.create_date)
                    )
                ).label("completion_rate"),
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by("completion_rate")
        )
        closed_projects = await session.execute(projects)
        return closed_projects


charity_project_crud = CRUDCharityProject(CharityProject)
