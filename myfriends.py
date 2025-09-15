"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""

import py_friends.friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this projectpairs[:5], please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""
from typing import List, Tuple, Dict, Set, Iterator
from pathlib import Path
from itertools import islice

# 1) Read pairs from a file (two strings per non-empty line, whitespace-separated)
def load_pairs(filename: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    with open(filename, "r", encoding="utf-8") as infile:
        for lineno, raw in enumerate(infile, start=1):
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(
                    f"Line {lineno}: expected 2 items, got {len(parts)} in {raw!r}"
                )
            a, b = parts
            pairs.append((a, b))
    return pairs

# 2) Build directory
def make_friends_directory(pairs: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    d: Dict[str, Set[str]] = {}
    for a, b in pairs:
        if a == b:
            continue
        d.setdefault(a, set()).add(b)
        d.setdefault(b, set()).add(a)
    return d

# 3) List (person, numberoffriends) sorted by descending count and name
def find_all_number_of_friends(my_dir: Dict[str, Set[str]]) -> List[Tuple[str, int]]:
    counts = [(person, len(friends)) for person, friends in my_dir.items()]
    counts.sort(key=lambda t: (-t[1], t[0]))
    return counts

# 4) Team roster: leader and (friends and friends-of-friends), ASCII
def make_team_roster(person: str, my_dir: Dict[str, Set[str]]) -> str:
    assert person in my_dir
    first_deg = set(my_dir.get(person, set()))
    second_deg: Set[str] = set()
    for f in first_deg:
        second_deg.update(my_dir.get(f, set()))
    team = (first_deg | second_deg) - {person}
    return "_".join([person] + sorted(team))

# 5) Smallest team label
def find_smallest_team(my_dir: Dict[str, Set[str]]) -> str:
    if not my_dir:
        raise ValueError("my_dir is empty; build it first.")
    size_label = []
    for person in my_dir:
        label = make_team_roster(person, my_dir)
        size = len(label.split("_"))  # leader + tail
        size_label.append((size, label))
    _, best_label = min(size_label, key=lambda t: (t[0], t[1]))
    return best_label

# 6) Iterator over unique friendships
def myfriends(my_dir: Dict[str, Set[str]]) -> Iterator[Tuple[str, str]]:
    for a in sorted(my_dir):
        for b in sorted(my_dir[a]):
            if a < b:
                yield (a, b)

# 7) Runner that prints each part
def main() -> None:
    here = Path(__file__).resolve().parent
    for name in ("myfriends.txt", "Friends", "Friends.txt"):
        data = here / name
        if data.exists():
            break
    else:
        print("❌ Could not find 'myfriends.txt' / 'Friends' / 'Friends.txt' next to", here)
        print("   Files here:", [p.name for p in here.iterdir()])
        return

    print("\n1. run load_pairs")
    pairs = load_pairs(str(data))
    print(pairs)

    print("\n2. run make_friends_directory")
    my_dir = make_friends_directory(pairs)
    print(my_dir)

    print("\n3. run find_all_number_of_friends")
    print(find_all_number_of_friends(my_dir))

    print("\n4. run make_team_roster")
    leader = "DARTHVADER" if "DARTHVADER" in my_dir else next(iter(my_dir))
    print(make_team_roster(leader, my_dir))

    print("\n5. run find_smallest_team")
    print(find_smallest_team(my_dir))

    print("\n6. run myfriends iterator (first 20)")
    for num, pair in enumerate(islice(myfriends(my_dir), 20)):
        print(num, pair)
    total = sum(1 for _ in myfriends(my_dir))
    print("total unique friendships:", total)

if __name__ == "__main__":
    main()

