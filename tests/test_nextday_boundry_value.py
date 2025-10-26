import arrow
import pytest
from nextdate import NextDate, NextDateError, next_date


@pytest.mark.parametrize(
    "m,d,y,expected",
    [
        (1, 1, 1812, (1, 2, 1812)),
        (1, 31, 1991, (2, 1, 1991)),
        (4, 30, 2005, (5, 1, 2005)),
        (2, 28, 1991, (3, 1, 1991)),
        (2, 28, 1992, (2, 29, 1992)),
        (2, 29, 1992, (3, 1, 1992)),
        (12, 31, 2011, (1, 1, 2012)),
        (2, 28, 1900, (3, 1, 1900)),
        (2, 28, 2000, (2, 29, 2000)),
        (2, 29, 2000, (3, 1, 2000)),
    ],
)
def test_valid_boundaries_function_api(m, d, y, expected):
    assert next_date(m, d, y) == expected


@pytest.mark.parametrize(
    "m,d,y",
    [
        (0, 10, 1991),
        (13, 10, 1991),
        (5, 0, 1991),
        (5, 32, 1991),
        (6, 15, 1811),
        (6, 15, 2013),
    ],
)
def test_simple_out_of_range(m, d, y):
    with pytest.raises(NextDateError):
        next_date(m, d, y)


@pytest.mark.parametrize(
    "m,d,y",
    [
        (6, 31, 1991),
        (4, 31, 1991),
        (2, 30, 1992),
        (2, 29, 1991),
        (2, 29, 1900),
    ],
)
def test_invalid_combinations(m, d, y):
    with pytest.raises(NextDateError):
        next_date(m, d, y)


def test_dec_31_2012_next_is_out_of_domain():
    with pytest.raises(NextDateError):
        next_date(12, 31, 2012)


def test_prev_day_simple_within_month():
    d = NextDate.of(3, 15, 1999)
    assert d.prev_day().as_tuple() == (3, 14, 1999)


def test_prev_day_month_roll_back_1st_to_30th():
    d = NextDate.of(5, 1, 1999)  # May 1 -> Apr 30
    assert d.prev_day().as_tuple() == (4, 30, 1999)


def test_prev_day_month_roll_back_1st_to_31st():
    d = NextDate.of(8, 1, 1999)  # Aug 1 -> Jul 31
    assert d.prev_day().as_tuple() == (7, 31, 1999)


def test_prev_day_march_1_non_leap_to_feb_28():
    d = NextDate.of(3, 1, 1991)
    assert d.prev_day().as_tuple() == (2, 28, 1991)


def test_prev_day_march_1_leap_to_feb_29():
    d = NextDate.of(3, 1, 1992)
    assert d.prev_day().as_tuple() == (2, 29, 1992)


def test_prev_day_jan_1_rolls_year_back():
    d = NextDate.of(1, 1, 1995)
    assert d.prev_day().as_tuple() == (12, 31, 1994)


def test_prev_day_min_boundary_raises():
    with pytest.raises(NextDateError):
        NextDate.of(1, 1, 1812).prev_day()


def test_shift_days_forward_and_backward():
    d = NextDate.of(12, 30, 2011)
    assert d.shift_days(+2).as_tuple() == (1, 1, 2012)
    assert d.shift_days(-2).as_tuple() == (12, 28, 2011)


def test_shift_days_outside_domain_raises():
    with pytest.raises(NextDateError):
        NextDate.of(12, 31, 2012).shift_days(+1)
    with pytest.raises(NextDateError):
        NextDate.of(1, 1, 1812).shift_days(-1)


def test_days_in_month_and_leap_logic():
    assert NextDate.days_in_month(2, 2000) == 29
    assert NextDate.days_in_month(2, 1900) == 28
    assert NextDate.is_leap(1996) is True
    assert NextDate.is_leap(1900) is False
