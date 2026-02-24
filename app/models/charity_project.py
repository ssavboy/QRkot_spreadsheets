from sqlalchemy import Column, String, Text

from .base import CharityDonationBase

TEMPLATE_REPR = '{name:.15} {description:.15} {base}'


class CharityProject(CharityDonationBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return TEMPLATE_REPR.format(
            name=self.name,
            description=self.description,
            base=super().__repr__()
        )
