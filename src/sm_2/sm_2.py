from datetime import datetime, timezone, timedelta
from typing import Optional, Union, Any
from copy import deepcopy
from math import ceil

class Card:

    n: int
    EF: float
    I: int
    due: datetime
    needs_extra_review: bool
    # TODO: add optional card id

    def __init__(self, n: int=0, EF: float=2.5, I: int=0, due: Optional[datetime]=None, needs_extra_review: bool=False) -> None:

        self.n = n
        self.EF = EF
        self.I = I
        if due is None:
            due = datetime.now(timezone.utc)
        self.due = due
        self.needs_extra_review = needs_extra_review

    def to_dict(self) -> dict[str, Union[int, float, str, bool]]:

        return_dict: dict[str, Union[int, float, str, bool]] = {
            "n": self.n,
            "EF": self.EF,
            "I": self.I,
            "due": self.due.isoformat(),
            "needs_extra_review": self.needs_extra_review
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "Card":

        n = int(source_dict['n'])
        EF = float(source_dict['EF'])
        I = int(source_dict['I'])
        due = datetime.fromisoformat(source_dict['due'])
        needs_extra_review = bool(source_dict['needs_extra_review'])

        return Card(n=n, EF=EF, I=I, due=due, needs_extra_review=needs_extra_review)


class ReviewLog:

    card: Card
    rating: int
    review_datetime: datetime

    def __init__(self, card: Card, rating: int, review_datetime: datetime) -> None:

        self.card = deepcopy(card)
        self.rating = rating
        self.review_datetime = review_datetime

    def to_dict(self) -> dict[str, Union[dict, int, str]]:

        return_dict: dict[str, Union[dict, int, str]] = {
            "card": self.card.to_dict(),
            "rating": self.rating,
            "review_datetime": self.review_datetime.isoformat()
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "ReviewLog":

        card = Card.from_dict(source_dict['card'])
        rating = int(source_dict['rating'])
        review_datetime = datetime.fromisoformat(source_dict['review_datetime'])

        return ReviewLog(card=card, rating=rating, review_datetime=review_datetime)


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