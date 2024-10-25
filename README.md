# sm-2

Python package implementing the [SM-2](https://super-memory.com/english/ol/sm2.htm) algorithm for spaced repetition scheduling.

## Quickstart

Import and initialize the SM-2 scheduler

```python
from sm_2 import SM2Scheduler, Card, ReviewLog

scheduler = SM2Scheduler()
```

Create a new Card object

```python
card = Card()
```

Choose a rating and review the card

```python
"""
5 - perfect response
4 - correct response after a hesitation
3 - correct response recalled with serious difficulty
2 - incorrect response; where the correct one seemed easy to recall
1 - incorrect response; the correct one remembered
0 - complete blackout.
"""

rating = 5

card, review_log = scheduler.review_card(card, rating)

print(f"Card rated {review_log.rating} at {review_log.review_datetime}")
# > Card rated 5 at 2024-10-24 02:14:20.802958+00:00
```

See when the card is due next
```python
from datetime import datetime, timezone

due = card.due

# how much time between when the card is due and now
time_delta = due - datetime.now(timezone.utc)

print(f"Card due: at {repr(due)}")
print(f"Card due in {time_delta.seconds / 3600} hours")
# > Card due: at datetime.datetime(2024, 10, 25, 2, 14, 20, 799320, tzinfo=datetime.timezone.utc)
# > Card due in 23.99972222222222 hours
```

## Usage

### Timezone

SM-2 uses UTC only. You can still specify custom datetimes, but they must be UTC.

```python
from sm_2 import SM2Scheduler, Card, ReviewLog
from datetime import datetime, timezone

scheduler = SM2Scheduler()

# create a new card on Jan. 1, 2024
card = Card(created_at=datetime(2024, 1, 1, 0, 0, 0, 0, timezone.utc)) # right
#card = Card(created_at=datetime(2024, 1, 1, 0, 0, 0, 0)) # wrong

# review the card on Jan. 2, 2024
card, review_log = scheduler.review_card(card=card, rating=5, review_datetime=datetime(2024, 1, 1, 0, 0, 0, 0, timezone.utc)) # right
#card, review_log = scheduler.review_card(card=card, rating=5, review_datetime=datetime(2024, 1, 1, 0, 0, 0, 0)) # wrong
```

### Serialization

`Card` and `ReviewLog` objects are json-serializable via their `to_dict` and `from_dict` methods for easy database storage:
```python
# serialize before storage
card_dict = card.to_dict()
review_log_dict = review_log.to_dict()

# deserialize from dict
card = Card.from_dict(card_dict)
review_log = ReviewLog.from_dict(review_log_dict)
```

## Versioning

This python package is currently unstable and adheres to the following versioning scheme:

- **Minor** version will increase when a backward-incompatible change is introduced.
- **Patch** version will increase when a bug is fixed or a new feature is added.

Once this package is considered stable, the **Major** version will be bumped to 1.0.0 and will follow [semver](https://semver.org/).