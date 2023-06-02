from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

TEMPLATE_REPR = ('{name}, Требуемая сумма: {full_amount}, '
                 'Внесённая сумма: {invested_amount},  Cобрана ли нужная сумма '
                 'для проекта: {fully_invested}, Дата создания проекта: '
                 '{create_date}, Дата закрытия проекта: {close_date}')


class CharityDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount',
        ),
    )

    def __repr__(self):
        return TEMPLATE_REPR.format(
            name=self.__class__.__name__,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date,
        )
