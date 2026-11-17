"""
Quiz 4 set-up script.  DO NOT CHANGE.

The set-up cells for Questions (B) and (C) run this script with
    %run quiz_data/FRIDAY_quiz4_setup.py

It defines:
  - Plant        the same Plant class as Question (A), without water
  - all_health   a dictionary of every owner's plant health, read from
                 quiz_data/plant_parents.csv
  - garden       a dictionary of 8 owners picked at random, mapping each
                 owner to their plant's health. It is different every
                 time this script runs.
"""

import random
import pandas as pd

df = pd.read_csv("quiz_data/plant_parents.csv")
owners = list(df["owner"])
healths = list(df["health"])

# every owner's plant health, looked up by owner
all_health = {}
for i in range(len(owners)):
    all_health[owners[i]] = int(healths[i])

# a random garden of 8 plants: this changes every time this script runs
garden_owners = random.sample(owners, k = 8)

garden = {}
for owner in garden_owners:
    garden[owner] = all_health[owner]


class Plant:
    """A plant at the Emory plant swap."""

    def __init__(self, owner, health):
        self.owner = owner
        self.health = health
        self.num_waterings = 0
        self.cutting_from = None

    def __str__(self):
        return f"{self.owner}'s plant (health {round(self.health, 1)})"

    # ---------- getters ----------

    def get_owner(self):
        return self.owner

    def get_health(self):
        return self.health

    def get_num_waterings(self):
        return self.num_waterings

    def get_cutting_from(self):
        return self.cutting_from

    # ---------- setters ----------

    def set_health(self, value):
        assert 0 <= value <= 100, "health must be between 0 and 100"
        self.health = value

    def take_cutting(self, other):
        """Replace self with a cutting from other.
        A cutting starts out as healthy as the plant it came from."""
        self.cutting_from = other
        self.set_health(other.get_health())

    # ---------- scoring ----------

    def care_value(self, score):
        return score
