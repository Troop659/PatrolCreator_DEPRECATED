from __future__ import annotations

from enum import Enum
from re import Match


class Rank(Enum):
    UNRANKED = 0
    SCOUT = 1
    TENDERFOOT = 2
    SECOND = 3
    FIRST = 4
    STAR = 5
    LIFE = 6

    @staticmethod
    def from_string(rank_str: str):
        return Rank[rank_str]

    def __str__(self):
        return self.name


class Scout:

    # A set of names of inactive scouts
    INACTIVE: set[str] = {
        "Shady Yowkeem",
        "Pierre Attalla",
        "Emmanuel Samaan",
        "John M Samaan",
        "Alfred Mekhail",
        "Youssef Wasfy",
        "Paul R Boles",
        "Daniel Ghabrial",
        "Michael Mohareb",
        "Jan M Said",
        "Jason Shohdy",
        "Adam Bibawy",
        "Gerges Katkout",
        "Mark Mikhail",
        "Andrew E Hakim"
    }

    def __init__(
                self,
                first_n: str,
                middle_i: str | None,
                last_n: str,
                age: int,
                rank: Rank,
            ):
        """Initializes a Scout based on name, age, and rank"""
        self.first_n = first_n.title()
        self.middle_i = middle_i.title() if middle_i else ''
        self.last_n = last_n.title()
        self.age = age
        self.rank = rank

    @classmethod
    def _from_match(cls, match: Match, rank: str):
        return Scout(
            match.group("first_n"),
            match.group("middle_i"),
            match.group("last_n"),
            int(match.group("age")),
            Rank.from_string(rank) if rank else Rank.UNRANKED
        )

    def __eq__(self, o: Scout):
        return (
            self.first_n == o.first_n and
            self.middle_i == o.middle_i and
            self.last_n == o.last_n and
            self.age == o.age and
            self.rank == o.rank
        )

    def __hash__(self) -> int:
        return hash(str(self))

    def is_related(self, o: Scout):
        return self.last_n == o.last_n

    def __str__(self):
        return self.name + f" ({self.age}) ({self.rank})"

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return (
            self.first_n +
            f"{f' {self.middle_i} ' if self.middle_i else ' '}" +
            self.last_n
        )

    @property
    def is_active(self):
        return self.name not in Scout.INACTIVE
