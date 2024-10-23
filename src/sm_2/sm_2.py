from datetime import datetime, timezone
from typing import Optional

class Card:

    n: int
    EF: float
    I: int
    due: datetime

    def __init__(self, n=0, EF=2.5, I=None, due=None):

        self.n = n
        self.EF = EF
        self.I = I
        if due is None:
            due = datetime.now(timezone.utc)
        else:
            self.due = due

class ReviewLog:

    rating: int
    review_datetime: datetime
    card: Card

    def __init__(self, rating: int, review_datetime: datetime, card: Card):

        self.rating = rating
        self.review_datetime = review_datetime
        self.card = card

class SM2Scheduler:

#    def __init__(self):
#
#        self.private_var = 1
    @staticmethod
    def review_card(card: Card, rating: int, review_datetime: Optional[datetime]=None) -> tuple[Card, ReviewLog]:
        pass
