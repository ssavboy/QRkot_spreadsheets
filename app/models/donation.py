from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityDonationBase

TEMPLATE_REPR = '{user} {comment} {base}'


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return TEMPLATE_REPR.format(
            user=self.user_id,
            comment=self.comment,
            base=super().__repr__()
        )
