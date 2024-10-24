from datetime import datetime, timezone, timedelta
from typing import Optional
from copy import deepcopy
from math import ceil

class Card:

    n: int
    EF: float
    I: int
    due: datetime
    needs_extra_review: bool
    # TODO: add optional card id

    def __init__(self, n=0, EF=2.5, I=0, due=None, needs_extra_review=False):

        self.n = n
        self.EF = EF
        self.I = I
        if due is None:
            due = datetime.now(timezone.utc)
        self.due = due
        self.needs_extra_review = needs_extra_review

    def to_dict(self):

        return_dict = {
            "n": self.n,
            "EF": self.EF,
            "I": self.I,
            "due": self.due.isoformat(),
            "needs_extra_review": self.needs_extra_review
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict):

        n = int(source_dict['n'])
        EF = float(source_dict['EF'])
        I = int(source_dict['I'])
        due = datetime.fromisoformat(source_dict['due'])
        needs_extra_review = bool(source_dict['needs_extra_review'])

        return Card(n=n, EF=EF, I=I, due=due, needs_extra_review=needs_extra_review)


class ReviewLog:

    rating: int
    review_datetime: datetime
    card: Card

    def __init__(self, card: Card, rating: int, review_datetime: datetime):

        self.rating = rating
        self.review_datetime = review_datetime
        self.card = card

    # TODO: add serialization

class SM2Scheduler:

    @staticmethod
    def review_card(card: Card, rating: int, review_datetime: Optional[datetime]=None) -> tuple[Card, ReviewLog]:
        
        card = deepcopy(card)

        if review_datetime is None:
            review_datetime = datetime.now(timezone.utc)

        card_is_due = review_datetime >= card.due

        if not card_is_due:
            raise RuntimeError(f"Card is not due for review until {card.due}.")
        
        review_log = ReviewLog(card=card, rating=rating, review_datetime=review_datetime)

        if card.needs_extra_review:

            if rating >= 4:
                card.needs_extra_review = False
                card.due += timedelta(days=card.I)

        else:

            if rating >= 3: # correct response
                
                if card.n == 0:

                    card.I = 1

                elif card.n == 1:

                    card.I = 6

                else:

                    card.I = ceil(card.I * card.EF)

                card.n += 1

                # note: EF increases when rating = 5, stays the same when rating = 4 and decreases when rating = 3
                card.EF = card.EF + (0.1-(5-rating)*(0.08+(5-rating)*0.02))
                card.EF = max(1.3, card.EF)

                if rating >= 4:

                    card.due += timedelta(days=card.I)

                else:

                    card.needs_extra_review = True
                    card.due = review_datetime

            else: # incorrect response

                card.n = 0
                card.I = 0
                card.due = review_datetime
                # EF doesn't change on incorrect reponses

        return card, review_log