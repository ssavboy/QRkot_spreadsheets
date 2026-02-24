from datetime import datetime
from typing import List

from app.models.base import CharityDonationBase


def investing(
    target: CharityDonationBase,
    sources: List[CharityDonationBase],
) -> List[CharityDonationBase]:
    modified = []
    for source in sources:
        fund_selection = min(
            target.full_amount - (target.invested_amount or 0),
            source.full_amount - (source.invested_amount or 0),
        )
        for donation in source, target:
            donation.invested_amount = (
                donation.invested_amount or 0
            ) + fund_selection
            if donation.full_amount == donation.invested_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
        modified.append(source)
        if target.fully_invested:
            break
    return modified
