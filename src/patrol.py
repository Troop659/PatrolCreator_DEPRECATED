from src.scout import Scout


class Patrol:

    # A dictionary of name: set of names. Associated names will not be placed
    # in the same patrol
    INCOMPATIBLE = {
        "First Last": {"First Last", "First M Last"}
    }

    def __init__(self, scouts: set[Scout]):
        self.scouts = scouts

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

    def __str__(self):
        return str(self.scouts)

    def __repr__(self):
        return str(self)
