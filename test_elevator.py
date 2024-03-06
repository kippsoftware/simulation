"""Run the following to ensure the simulation works as expected.

   % pytest

"""

import pytest
from elevator import Elevator


def test_initialize():
    elevator = Elevator()
    assert elevator.start_floor == 1
    assert len(elevator.floors_visited) == 0
    assert elevator.travel_time == 0
    assert len(elevator.floors_visited) == 0


def test_parse_args():
    elevator = Elevator()
    elevator.parse_args(())
    assert elevator.start_floor == 1
    elevator.parse_args(["start=2"])
    assert elevator.start_floor == 2
    elevator.parse_args(["floor=3,4"])
    assert elevator.floors_to_visit == [3, 4]
    elevator.parse_args("start=5 floor=6,7".split())
    assert elevator.start_floor == 5
    assert elevator.floors_to_visit == [6, 7]
    elevator.parse_args("start=-1 floor=-1,-2".split())
    assert elevator.start_floor == -1
    assert elevator.floors_to_visit == [-1, -2]
    elevator.parse_args("floor=10,9 start=8".split())
    assert elevator.start_floor == 8
    assert elevator.floors_to_visit == [10, 9]


def test_parse_args_bad():
    elevator = Elevator()
    elevator.parse_args(["floor = 11, 12"])
    assert len(elevator.floors_to_visit) == 0
    with pytest.raises(ValueError):
        elevator.parse_args(["start=a"])
    with pytest.raises(ValueError):
        elevator.parse_args(["floor=a,b"])


def test_example():
    elevator = Elevator()
    elevator.parse_args("start=12 floor=2,9,1,32".split())
    elevator.simulate()
    assert str(elevator) == "560 12,2,9,1,32"


def test_memory():
    elevator = Elevator()
    elevator.parse_args("start=12 floor=2,9,1,32".split())
    elevator.simulate()
    elevator.start_floor = 13
    elevator.simulate()
    assert str(elevator) == "570 13,2,9,1,32"
    elevator.start_floor = 1
    elevator.simulate()
    assert str(elevator) == "470 1,2,9,1,32"


def test_underground():
    elevator = Elevator()
    elevator.parse_args("start=1 floor=-100,1".split())
    elevator.simulate()
    assert str(elevator) == "2020 1,-100,1"


def test_bounds():
    elevator = Elevator()
    elevator.parse_args("start=99999999999999999999 floor=0".split())
    elevator.simulate()
    assert str(elevator) == "999999999999999999990 99999999999999999999,0"


def test_pathological_overflow():
    elevator = Elevator()
    maxint = "9" * 4300
    elevator.parse_args(f"start=0 floor={maxint},0".split())
    elevator.simulate()
    with pytest.raises(ValueError):
        str(elevator)
