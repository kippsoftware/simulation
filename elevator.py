#!python3

"""# Elevator Discrete Event Simulator

## Challenge

- Provide code that simulates an elevator. You are free to use any language.
- Upload the completed project to GitHub for discussion during interview.
- Document all assumptions and any features that weren't implemented.
- The result should be an executable, or script, that can be run with
  the following inputs and generate the following outputs.

    Inputs: [list of floors to visit] (e.g. elevator start=12 floor=2,9,1,32)
    Outputs: [total travel time, floors visited in order] (e.g. 560 12,2,9,1,32)
    Program Constants: Single floor travel time: 10

## Assumptions (Contractual Preconditions and Postconditions)

- Floor numbers are integers such that f_i in Z
- Python syntax allows 4300 digits per integer, thus -10^4300 < f_i < 10^4300
- In Python, integers are implemented with arbitrary precision ensuring that
  travel time will not overflow until memory is exhausted;
  however caller must ensure travel time < 10^4300 so that string conversion 
  will not raise a ValueError
- Buildings with negative floors (basements) will have floor 0
- Simulated building has sufficient floors to satisfy the requested traversal
- Inter-floor distance is the positive distance between floor numbers d(i,j) = |f_i - f_j|
- Start floor 1 unless set as start=int on the command line
- Floors to visit is [] unless set as floors=int[,int]+ on the command line
- Raise ValueError on failed argument parse
- Unrecognized arguments are ignored

## Interesting Features not Implemented

- Compute the optimal path of floors to minimize total elevator travel
  time; minimum spanning tree, O(n log n) 
- Simulate realistic elevator acceleration and deceleration

"""
import sys

USAGE = """Usage: ./elevator.py start=int floor=int(,int)*
Simluate elevator visiting the floors of a building then
output the total travel time and list of the floors visited.
"""


# Simulation assumes constant travel time between adjacent floors
SINGLE_FLOOR_TRAVEL_TIME = 10

# Capture the names of the relevant command line parameters
START_ARG = "start"
FLOOR_ARG = "floor"


class Elevator:
    """Encapulate the state of an elevator simulation."""

    def __init__(self):
        """Instantiate with reasonable values"""
        self.start_floor = 1
        self.floors_to_visit = []
        self.travel_time = 0
        self.floors_visited = []

    def parse_args(self, argv):
        """Parse arguments and extract the values of START_ARG and
        FLOOR_ARG. Last write wins. Raise ValueError when values are
        not integers.

        argv - list of strings of the form key=value or key=value(,value)*

        """
        for arg in argv:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if key == START_ARG:
                    self.start_floor = int(value)
                elif key == FLOOR_ARG:
                    self.floors_to_visit = list(map(int, value.split(",")))

    def simulate(self):
        """Given initial values for start_floor and floors_to_visit,
        run the simulation and calculate the total travel time,
        retaining the travel time and floors visited as member variables."""

        self.travel_time = 0
        self.floors_visited = [self.start_floor]
        current_floor = self.start_floor
        for floor in self.floors_to_visit:
            self.travel_time += abs(current_floor - floor) * SINGLE_FLOOR_TRAVEL_TIME
            self.floors_visited.append(floor)
            current_floor = floor

    def __str__(self):
        """Report the most recent simulation as a string"""
        return f"{self.travel_time} {','.join(list(map(str, self.floors_visited)))}"


if __name__ == "__main__":

    # Instantiate the elevator for the simulation
    elevator = Elevator()

    if len(sys.argv) > 1:
        # Set values of start and floor args
        elevator.parse_args(sys.argv[1:])
        # Run the simlation
        elevator.simulate()
        # Report the results
        print(elevator)
    else:
        print(USAGE)
