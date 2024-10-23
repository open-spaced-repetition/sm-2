from datetime import datetime, timezone, timedelta
from typing import Optional
from copy import deepcopy
from math import ceil

class Card:

    n: int
    EF: float
    I: int
    due: datetime

    def __init__(self, n=0, EF=2.5, I=0, due=None):

        self.n = n
        self.EF = EF
        self.I = I
        if due is None:
            due = datetime.now(timezone.utc)
        self.due = due

class ReviewLog:

    rating: int
    review_datetime: datetime
    card: Card

    def __init__(self, card: Card, rating: int, review_datetime: datetime):

        self.rating = rating
        self.review_datetime = review_datetime
        self.card = card

class SM2Scheduler:

    @staticmethod
    def review_card(card: Card, rating: int, review_datetime: Optional[datetime]=None) -> tuple[Card, ReviewLog]:
        
        card = deepcopy(card)

        card_is_due = review_datetime >= card.due

        if not card_is_due:
            raise RuntimeError(f"Card is not due for review until {card.due}.")
        
        review_log = ReviewLog(card=card, rating=rating, review_datetime=review_datetime)

        if rating >= 3: # correct response
            
            if card.n == 0:

                card.I = 1

            elif card.n == 1:

                card.I = 6

            else:

                card.I = ceil(card.I * card.EF)

            card.due += timedelta(days=card.I)

            card.n += 1

            # note: EF increases when rating = 5, stays the same when rating = 4 and decreases when rating = 3
            card.EF = card.EF + (0.1-(5-rating)*(0.08+(5-rating)*0.02))

        else: # incorrect response

            card.n = 0
            card.I = 0
            card.due = review_datetime
            # EF doesn't change on incorrect reponses

        return card, review_log