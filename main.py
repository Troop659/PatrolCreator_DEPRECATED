import random

from src.patrol import Patrol
from src.roster import Roster
from src.scout import Scout

# These should be the only variables you need to change!
# ------------------------------------------------------------------------------

# The file path to the roster
ROSTER_PATH = r"C:\Users\jojom\OneDrive\Desktop\roster.pdf"

# How many patrols should be created?
N_PATROLS = 5

# Should we allow brothers in patrols?
RELATION_ALLOWED = False

# A scout must have another scout within age difference
AGE_DIFFERENCE = 2

# The target average rank of all scouts in a patrol
# Unranked = 0, Scout = 1, etc.
# No guarantees of exact target, but should be within a threshold.
TARGET_RANK = 2

# Patrols will be within +- rank threshold of target rank, on average
# If threshold is too low, you risk running into an impossible patrol setup
# If threshold is too high, you might as well not have a target rank
RANK_THRESH = 0.75

# A target of 2 with += 0.75 seems to be fine for now, but feel free to
# change the values

# INSTRUCTIONS
# STEP 1: `pip install -r requirements.txt` to install the library that
# will let you parse the roster PDF file

# STEP 2: Set the variables above ^

# STEP 3: Press run
# Every time you run the program, you will get a new list of patrols, so make
# sure to save the one you end up wanting to use.

# If the program doesn't execute within a few seconds: something went wrong
# with creating the patrols. It ran into a situation where it's impossible
# to create patrols.
# You can either run the program again (to try to randomly get a new set of
# patrols) or you can change the variables above to make it more attainable

# MANUALLY MODIFYING SCOUTS
# To add a Patrol Incompatibility (scouts that cannot be in the same patrol),
# add them to the src/patrol.py "INCOMPATIBLE" dictionary

# To add an Inactive Scout (scouts that cannot be in any patrol), add them to
# the src/scout.py "INACTIVE" set

# Also make sure to add Troop and Patrol leaders in src/patrol.py

# For anything that requires manual name input, make sure to enter the exact
# First, Middle Initial, and Last Name in Title casing

# Glory be to God
# ------------------------------------------------------------------------------


def begin_generating(scouts: list[Scout]):
    global GLOBAL_STRIKES
    global LOCAL_STRIKES
    global SCOUTS_LEFT
    GLOBAL_STRIKES = 20

    n_tries = 0
    patrols = []
    while not patrols:
        SCOUTS_LEFT = 0
        LOCAL_STRIKES = 2 * len(scouts)

        if n_tries == GLOBAL_STRIKES:
            print("Could not generate patrols with current config.")
            return

        print(f"Attempting to generate patrols. Try #{n_tries + 1}")
        patrols = generate_patrols(scouts.copy())
        n_tries += 1

    output_patrols(patrols, set(scouts))


def generate_patrols(scouts: list[Scout]) -> list[Patrol]:
    global LOCAL_STRIKES
    global SCOUTS_LEFT

    # Initialize N_PATROLS empty patrols
    patrols: list[Patrol] = []
    for _ in range(N_PATROLS):
        patrols.append(Patrol(set()))

    curr_patrol = 0
    while scouts:
        # If we have no movement for LOCAL_STRIKES times, we give up
        curr_scouts_left = len(scouts)
        if curr_scouts_left == SCOUTS_LEFT:
            LOCAL_STRIKES -= 1
        SCOUTS_LEFT = curr_scouts_left

        if LOCAL_STRIKES <= 0:
            return []

        scout = random.choice(scouts)
        patrol = patrols[curr_patrol]

        # Check for relation
        if not RELATION_ALLOWED and patrol.has_related_scout(scout):
            continue

        # Check for age
        if not patrol.has_valid_age(scout, AGE_DIFFERENCE):
            continue

        # Check for patrols to have generally similar rank formations
        future_avg_rank = patrol.future_avg_rank(set([scout]))
        if future_avg_rank == -1:
            pass
        elif abs(future_avg_rank - TARGET_RANK) > RANK_THRESH:
            continue

        # Check for incompatible scouts
        if scout.name in patrol.incompatible_scouts:
            continue

        # Don't add scouts from the leaders patrol to any patrol
        if patrol.is_troop_leader(scout):
            scouts.remove(scout)
            continue

        # Patrols can only have one patrol leader each
        if patrol.has_patrol_leader() and patrol.is_patrol_leader(scout):
            continue

        # Add to the patrol and remove from bank of scouts
        patrol.add(scout)
        scouts.remove(scout)

        # Go to the next patrol to add a scout
        curr_patrol += 1
        if curr_patrol >= N_PATROLS:
            curr_patrol = 0

    return patrols


def output_patrols(patrols: list[Patrol], all_scouts: set[Scout]):
    # Format and display the created patrols in terminal.
    # We also write to a file
    output = Patrol.format_patrol(
        0, Patrol.get_leaders_patrol(all_scouts)
    ) + "\n"
    for ind, patrol in enumerate(patrols):
        output += Patrol.format_patrol(ind + 1, patrol) + "\n\n"

    # Output to terminal
    print(output)

    # Output to file
    # CAREFUL. This will *overwrite* the content in patrols.txt
    with open("patrols.txt", "w") as f:
        f.write(output)


if __name__ == "__main__":
    roster = Roster(ROSTER_PATH)
    all_scouts = list(roster.scouts)
    scouts = list(roster.scouts)
    begin_generating(scouts)
