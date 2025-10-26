import pytest
from nextdate import NextDate, NextDateError, next_date

# ------------------------------------------------------------
# Weak Equivalence Classes
# ------------------------------------------------------------
# - M31: months with 31 days (Jan, Mar, May, Jul, Aug, Oct, Dec)
# - M30: months with 30 days (Apr, Jun, Sep, Nov)
# - MFEB: February
# - D1_28, D29, D30, D31: day classes
# - YLEAP, YNON: leap vs non-leap years


@pytest.mark.parametrize(
    "m,d,y,expected",
    [
        (1, 15, 1991, (1, 16, 1991)),  # M31, D1_28, YNON -> within month
        (1, 31, 1991, (2, 1, 1991)),  # M31, D31, YNON -> month roll
        (4, 30, 1991, (5, 1, 1991)),  # M30, D30, YNON -> month roll
        (2, 21, 1991, (2, 22, 1991)),  # MFEB, D1_28, YNON -> within month
        (2, 28, 1992, (2, 29, 1992)),  # MFEB, D28, YLEAP -> leap day exists
        (2, 28, 1991, (3, 1, 1991)),  # MFEB, D28, YNON -> leap day missing
        (2, 29, 2000, (3, 1, 2000)),  # MFEB, D29, YLEAP (century leap year)
        (12, 31, 2011, (1, 1, 2012)),  # year roll
    ],
)
def test_equivalence_weak_valid(m, d, y, expected):
    assert next_date(m, d, y) == expected


# ------------------------------------------------------------
# Traditional Invalid Classes
# ------------------------------------------------------------
# Each invalid input is tested individually, while the other
# parameters remain within valid ranges.


@pytest.mark.parametrize(
    "m,d,y",
    [
        (0, 10, 1991),  # month < 1
        (13, 10, 1991),  # month > 12
        (5, 0, 1991),  # day < 1
        (5, 32, 1991),  # day > 31
        (6, 15, 1811),  # year < 1812
        (6, 15, 2013),  # year > 2012
    ],
)
def test_equivalence_traditional_invalid_range(m, d, y):
    """Inputs outside the allowed numeric range must raise NextDateError."""
    with pytest.raises(NextDateError):
        next_date(m, d, y)


@pytest.mark.parametrize(
    "m,d,y",
    [
        (6, 31, 1991),  # June has only 30 days
        (4, 31, 1991),  # April has only 30 days
        (2, 30, 1992),  # February never has 30 days
        (2, 29, 1900),  # 1900 is NOT leap (century rule)
        (2, 29, 1991),  # 1991 is not leap
    ],
)
def test_equivalence_traditional_invalid_combinations(m, d, y):
    """Invalid month–day combinations must raise NextDateError."""
    with pytest.raises(NextDateError):
        next_date(m, d, y)


# ------------------------------------------------------------
# Strong Equivalence Classes (Sampled Cross-Class Combinations)
# ------------------------------------------------------------
# Instead of testing every combination, we sample a meaningful subset
# to expose interactions between month-length and leap-year logic.

strong_vectors = [
    # 31-day months with various day classes
    (1, 31, 1993, (2, 1, 1993)),  # M31, D31
    (3, 30, 1993, (3, 31, 1993)),  # M31, D30
    (7, 15, 2001, (7, 16, 2001)),  # M31, midrange
    (9, 30, 1999, (10, 1, 1999)),  # M30, D30
    (11, 29, 2000, (11, 30, 2000)),  # M30, D29
    (4, 15, 2010, (4, 16, 2010)),  # M30, midrange
    (2, 28, 1996, (2, 29, 1996)),  # YLEAP
    (2, 28, 1997, (3, 1, 1997)),
    (2, 29, 2000, (3, 1, 2000)),  # YLEAP (century leap)
]


@pytest.mark.parametrize("m,d,y,expected", strong_vectors)
def test_equivalence_strong_sample(m, d, y, expected):
    """Sampled cross-class tests validating month-length × leap-year interactions."""
    assert next_date(m, d, y) == expected


# ------------------------------------------------------------
# Output-Domain Classes (Behavioral Equivalence)
# ------------------------------------------------------------


@pytest.mark.parametrize(
    "m,d,y,expected_class",
    [
        (12, 31, 2011, "year-roll"),
        (4, 30, 2007, "month-roll"),
        (1, 15, 2007, "same-month"),
    ],
)
def test_equivalence_output_domain(m, d, y, expected_class):
    """Verify that outputs belong to the expected behavioral class."""
    nm, nd, ny = next_date(m, d, y)
    if expected_class == "same-month":
        assert ny == y and nm == m and nd == d + 1
    elif expected_class == "month-roll":
        assert ny == y and nm == (m % 12) + 1 and nd == 1
    elif expected_class == "year-roll":
        assert ny == y + 1 and nm == 1 and nd == 1
