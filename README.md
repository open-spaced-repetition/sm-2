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