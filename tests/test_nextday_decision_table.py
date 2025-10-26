import arrow
import pytest
from nextdate import next_date, NextDateError, NextDate


RULES = [
    # M1 (30-day months: 4,6,9,11)
    (4, 14, 1991, (4, 15, 1991)),  # D1 ->day
    (4, 28, 1991, (4, 29, 1991)),  # D2 ->day
    (4, 29, 1991, (4, 30, 1991)),  # D3 ->day
    (4, 30, 1991, (5, 1, 1991)),  # D4 -> reset day,month
    (4, 31, 1991, NextDateError),  # D5 -> impossible
    # M2 (31-day months except December: 1,3,5,7,8,10)
    (1, 14, 1991, (1, 15, 1991)),  # D1 ->day
    (1, 30, 1991, (1, 31, 1991)),  # D4 ->day
    (1, 31, 1991, (2, 1, 1991)),  # D5 -> reset day,month
    # M3 (December)
    (12, 14, 1991, (12, 15, 1991)),  # D1 ->day
    (12, 31, 2011, (1, 1, 2012)),  # D5 -> reset day,month,year (valid)
    # (12, 31, 2012) would be out-of-domain next day; covered elsewhere.
    # M4 (February): leap vs common
    # Y1 (leap: 2000)
    (2, 14, 2000, (2, 15, 2000)),  # D1 ->day
    (2, 28, 2000, (2, 29, 2000)),  # D2 ->day (leap)
    (2, 29, 2000, (3, 1, 2000)),  # D3 -> reset day,month
    (2, 30, 2000, NextDateError),  # D4 -> impossible
    # Y2 (common: 1991)
    (2, 14, 1991, (2, 15, 1991)),  # D1 ->day
    (2, 28, 1991, (3, 1, 1991)),  # D2 -> reset day,month
    (2, 29, 1991, NextDateError),  # D3 -> impossible
]


@pytest.mark.parametrize("m,d,y,exp", RULES)
def test_decision_table_rules(m, d, y, exp):
    if isinstance(exp, type) and issubclass(exp, Exception):
        with pytest.raises(exp):
            next_date(m, d, y)
    else:
        assert next_date(m, d, y) == exp


def _ref_last_business_day(y: int, m: int):
    end = arrow.get(y, m, 1).shift(months=+1).shift(days=-1)
    cur = end
    while cur.weekday() >= 5:  # correct
        cur = cur.shift(days=-1)
    return (cur.month, cur.day, cur.year)


# Decision table (limited-entry), condition on weekday(end-of-month):
# Wd  {Mon..Fri} -> A: return end
# Wd == Sat       -> B: back off 1 day
# Wd == Sun       -> C: back off 2 days
#  - Mon..Fri: 2010-12 (Fri)
#  - Sat:      2011-12 (Sat)
#  - Sun:      2011-07 (Sun)

RULES = [
    # (year, month, weekday_class)
    (2010, 12, "weekday"),  # Fri
    (2011, 12, "saturday"),
    (2011, 7, "sunday"),
]


@pytest.mark.parametrize("y,m,wclass", RULES)
def test_last_business_day_decision_table(y, m, wclass):
    got = NextDate.of(m, 10, y).last_business_day_of_month().as_tuple()
    exp = _ref_last_business_day(y, m)
    assert got == exp, f"DTT rule failed ({wclass}): got={got}, expected={exp}"
