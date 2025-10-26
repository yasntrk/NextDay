from __future__ import annotations
import arrow
from dataclasses import dataclass

MIN_YEAR = 1812
MAX_YEAR = 2012


class NextDateError(ValueError):
    """Error handler."""


def _validate_primitive(month: int, day: int, year: int) -> None:
    if not (1 <= month <= 12):
        raise NextDateError("month must be in 1..12")
    if not (1 <= day <= 31):
        raise NextDateError("day must be in 1..31")
    if not (MIN_YEAR <= year <= MAX_YEAR):
        raise NextDateError(f"year must be in{MIN_YEAR}..{MAX_YEAR}")


def _arrow_or_error(year: int, month: int, day: int) -> arrow.Arrow:
    try:
        return arrow.get(year, month, day)
    except Exception as exc:
        raise NextDateError("invalid date combination for given month/year.") from exc


@dataclass(frozen=True)
class NextDate:
    """Immutable date range: 1812..2012."""

    year: int
    month: int
    day: int

    # ---------- Constructors ----------
    @staticmethod
    def of(month: int, day: int, year: int) -> "NextDate":
        _validate_primitive(month, day, year)
        _arrow_or_error(year, month, day)  # check validity
        return NextDate(year=year, month=month, day=day)

    @staticmethod
    def from_arrow(a: arrow.Arrow) -> "NextDate":
        return NextDate.of(a.month, a.day, a.year)

    @staticmethod
    def is_leap(year: int) -> bool:
        if year % 4 != 0:
            return False
        if year % 100 == 0:
            return year % 400 == 0
        return True

    @staticmethod
    def days_in_month(month: int, year: int) -> int:
        if month == 2:
            return 29 if NextDate.is_leap(year) else 28
        return 31 if month in (1, 3, 5, 7, 8, 10, 12) else 30

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.month, self.day, self.year)

    def _as_arrow(self) -> arrow.Arrow:
        return _arrow_or_error(self.year, self.month, self.day)

    def next_day(self) -> "NextDate":
        nxt = self._as_arrow().shift(days=+1)
        if not (MIN_YEAR <= nxt.year <= MAX_YEAR):
            raise NextDateError("next date goes outside allowed year range")
        return NextDate.from_arrow(nxt)

    def prev_day(self) -> "NextDate":
        prv = self._as_arrow().shift(days=-1)
        if not (MIN_YEAR <= prv.year <= MAX_YEAR):
            raise NextDateError("previous date goes outside allowed year range")
        return NextDate.from_arrow(prv)

    def shift_days(self, days: int) -> "NextDate":
        if days == 0:
            return self
        target = self._as_arrow().shift(days=days)
        if not (MIN_YEAR <= target.year <= MAX_YEAR):
            raise NextDateError("shifted date goes outside allowed yearrange")
        return NextDate.from_arrow(target)

    def last_business_day_of_month(self) -> "NextDate":
        """
        Returns the last business day (Mon–Fri) of the month containing this date.
        """
        a = self._as_arrow()
        end = a.shift(months=+1).replace(day=1).shift(days=-1)

        cur = end
        while cur.weekday() > 5:
            cur = cur.shift(days=-1)

        return NextDate.from_arrow(cur)

def next_date(month: int, day: int, year: int) -> tuple[int, int, int]:
    d = NextDate.of(month, day, year).next_day()
    return d.as_tuple()
