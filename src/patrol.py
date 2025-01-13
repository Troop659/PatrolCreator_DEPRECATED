from src.scout import Scout


class Patrol:

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

    def __str__(self):
        return str(self.scouts)

    def __repr__(self):
        return str(self)
