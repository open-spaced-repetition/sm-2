"""
sm_2.sm_2

This module defines each of the classes used in the sm_2 package.

Classes:
    Card: Represents a flashcard in the SM-2 scheduling system.
    ReviewLog: Represents the log entry of a Card object that has been reviewed.
    SM2Scheduler: The SM-2 scheduler.
"""

from datetime import datetime, timezone, timedelta
from typing import Any
from copy import deepcopy
from math import ceil

class Card:
    """
    Represents a flashcard in the SM-2 scheduling system.

    Attributes:
        card_id (int): The id of the card. Defaults to the epoch miliseconds of when the card was created.
        n (int): The number of times the card has been correctly recalled in a row, excluding any extra reviews (see needs_extra_review below).
        EF (float): The easiness factor of the card.
        I (int): The interval length in days between when the card is next due and when it was last reviewed.
        due (datetime): When the card is due for review.
        needs_extra_review (bool): In the SM-2 system, if a card has been rated less than 4, it must be reviewed again in the same day until it's rated 4 or 5. This is a flag variable that determines if the card needs to reviewed once more.
    """

    card_id: int
    n: int
    EF: float
    I: int
    due: datetime
    needs_extra_review: bool

    def __init__(self, created_at: datetime | None = None, card_id: int | None = None, n: int=0, EF: float=2.5, I: int=0, due: datetime | None = None, needs_extra_review: bool=False) -> None:

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        if card_id is None:
            card_id = int(created_at.timestamp() * 1000)
        self.card_id = card_id

        self.n = n
        self.EF = EF
        self.I = I

        if due is None:
            due = created_at
        self.due = due

        self.needs_extra_review = needs_extra_review

    def to_dict(self) -> dict[str, int | float | str | bool]:

        return_dict: dict[str, int | float | str | bool] = {
            "card_id": self.card_id,
            "n": self.n,
            "EF": self.EF,
            "I": self.I,
            "due": self.due.isoformat(),
            "needs_extra_review": self.needs_extra_review
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "Card":

        card_id = int(source_dict['card_id'])
        n = int(source_dict['n'])
        EF = float(source_dict['EF'])
        I = int(source_dict['I'])
        due = datetime.fromisoformat(source_dict['due'])
        needs_extra_review = bool(source_dict['needs_extra_review'])

        return Card(card_id=card_id, n=n, EF=EF, I=I, due=due, needs_extra_review=needs_extra_review)


class ReviewLog:
    """
    Represents the log entry of a Card object that has been reviewed.

    Attributes:
        card (Card): Copy of the card object that was reviewed.
        rating (int): The rating given to the card during the review.
        review_datetime (datetime): The date and time of the review.
        review_duration (int | None): The amount of time in miliseconds it took to review the card, if specified.
    """

    card: Card
    rating: int
    review_datetime: datetime
    review_duration: int | None

    def __init__(self, card: Card, rating: int, review_datetime: datetime, review_duration: int | None = None) -> None:

        self.card = deepcopy(card)
        self.rating = rating
        self.review_datetime = review_datetime
        self.review_duration = review_duration

    def to_dict(self) -> dict[str, dict | int | str | None]:

        return_dict: dict[str, dict | int | str | None] = {
            "card": self.card.to_dict(),
            "rating": self.rating,
            "review_datetime": self.review_datetime.isoformat(),
            "review_duration": self.review_duration
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "ReviewLog":

        card = Card.from_dict(source_dict['card'])
        rating = int(source_dict['rating'])
        review_datetime = datetime.fromisoformat(source_dict['review_datetime'])
        review_duration = source_dict['review_duration']

        return ReviewLog(card=card, rating=rating, review_datetime=review_datetime, review_duration=review_duration)


class SM2Scheduler:
    """
    The SM-2 scheduler.

    Enables the reviewing and future scheduling of cards according to the SM-2 algorithm.

    Note: This class has no attributes and only provides static methods. The reason the scheduler exists
    as a class is to be consistent with other spaced repetition python packages.
    """

    @staticmethod
    def review_card(card: Card, rating: int, review_datetime: datetime | None = None, review_duration: int | None = None) -> tuple[Card, ReviewLog]:
        """
        Reviews a card with a given rating at a specified time.

        Args:
            card (Card): The card being reviewed.
            rating (int): The chosen rating for the card being reviewed. Possible values are 0,1,2,3,4,5.
            review_datetime (datetime | None): The date and time of the review.
            review_duration (int | None): The amount of time in miliseconds it took to review the card, if specified.

        Returns:
            tuple: A tuple containing the updated, reviewed card and its corresponding review log.

        Raises:
            RuntimeError: If the given card is reviewed at a time where it is not yet due.
        """

        card = deepcopy(card)

        if review_datetime is None:
            review_datetime = datetime.now(timezone.utc)

        card_is_due = review_datetime >= card.due

        if not card_is_due:
            raise RuntimeError(f"Card is not due for review until {card.due}.")
        
        review_log = ReviewLog(card=card, rating=rating, review_datetime=review_datetime, review_duration=review_duration)

        if card.needs_extra_review:

            if rating >= 4:
                card.needs_extra_review = False
                card.due += timedelta(days=card.I)

        else:

            if rating >= 3: # correct response

                # note: EF increases when rating = 5, stays the same when rating = 4 and decreases when rating = 3
                card.EF = card.EF + (0.1-(5-rating)*(0.08+(5-rating)*0.02))
                card.EF = max(1.3, card.EF)
                
                if card.n == 0:

                    card.I = 1

                elif card.n == 1:

                    card.I = 6

                else:

                    card.I = ceil(card.I * card.EF)

                card.n += 1

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