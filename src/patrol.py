from __future__ import annotations

from src.scout import Scout


class Patrol:

    # A dictionary of name: set of names. Associated names will not be placed
    # in the same patrol
    INCOMPATIBLE = {
        "First Last": {"First M Last"}
    }

    # A set of names of scouts that will be in the leaders patrol
    TROOP_LEADERS = {
        "Jacob J Abdou",
        "John Wasily",
        "Justin Ibrahim",
        "Timothy Wasef",
        "Theodore Georgy",
        "Peter B Abader",
        "Jonah W Gaad"
    }

    # A set of names of patrol leaders
    # (meaning only one patrol leader per patrol)
    PATROL_LEADERS = {
        "Matthew Abadeer",
        "Pierre Gerges",
        "Alexander Youakim",
        "Marcus M Morgan",
        "Chris S Kozman"
    }

    def __init__(self, scouts: set[Scout]):
        self.scouts = scouts

    @classmethod
    def get_leaders_patrol(cls, scouts: set[Scout]):
        """Given a list of all available scouts, return the Leaders patrol"""
        scouts = set(sc for sc in scouts if Patrol.is_troop_leader(sc))
        return cls(scouts)

    def add(self, scout: Scout):
        self.scouts.add(scout)

    def __bool__(self):
        return bool(self.scouts)

    def has_related_scout(self, o: Scout):
        """Checks if the patrol already has a Scout with the same last name"""
        return any([o.is_related(i) for i in self.scouts])

    def has_valid_age(self, o: Scout, age: int):
        """Tries to find at least one scout within age range"""
        if not self.scouts:
            return True

        for scout in self.scouts:
            if abs(o.age - scout.age) <= age:
                return True
        return False

    def future_avg_rank(self, o: set[Scout]):
        if not self.scouts:
            return -1
        return Patrol.calculate_avg_rank(self.scouts | o)

    @property
    def average_rank(self):
        if not self.scouts:
            return -1
        return Patrol.calculate_avg_rank(self.scouts)

    @staticmethod
    def calculate_avg_rank(scouts: set[Scout]):
        return sum([i.rank.value for i in scouts])/len(scouts)

    @property
    def incompatible_scouts(self):
        """
        Retrieves a set of all the names of all scouts that can't be added
        to this patrol
        """
        incompatible: set[str] = set()
        for scout in self.scouts:
            incompatible.update(self.get_incompatible_for(scout))

        return incompatible

    def get_incompatible_for(self, scout: Scout) -> set[str]:
        """
        Retrieve the incompatible scouts for this specific scout

        This returns a set of NAMES of scouts
        """
        incompatible: set[str] = set()
        for main, sub in Patrol.INCOMPATIBLE.items():
            if scout.name == main:
                incompatible.update(sub)
            if scout.name in sub:
                incompatible.add(main)

        return incompatible

    def has_patrol_leader(self) -> bool:
        """Returns whether or not a patrol leader was already assigned"""
        return bool(set(i.name for i in self.scouts) & self.PATROL_LEADERS)

    @staticmethod
    def is_troop_leader(scout: Scout) -> bool:
        return scout.name in Patrol.TROOP_LEADERS

    @staticmethod
    def is_patrol_leader(scout: Scout) -> bool:
        return scout.name in Patrol.PATROL_LEADERS

    def __str__(self):
        # Start with patrol leader
        output = ""
        for sc in self.scouts:
            if sc.name in Patrol.PATROL_LEADERS:
                output = str(sc) + " (Patrol Leader)\n"
                break

        # Add the rest of the patrols
        for scout in self.scouts:
            output += (
                str(scout) + "\n"
                if not Patrol.is_patrol_leader(scout)
                else ''
            )

        return output

    def __repr__(self):
        return str(self)

    @staticmethod
    def format_patrol(index: int, patrol: Patrol):
        output = ""
        output += (
            (f"Patrol #{index} " if index else "Leaders Patrol ") +
            f"({len(patrol.scouts)} Scouts) " +
            f"({patrol.average_rank} Avg. Rank)\n" +
            "------------\n" +
            str(patrol)
        )
        return output
