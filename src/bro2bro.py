#!/usr/bin/env python3

import csv
import argparse
from enum import Enum
from dataclasses import dataclass

class ConnectionType(Enum):
    SELF = -1
    PARENT = 0
    CHILD = 1
    SPOUSE = 2

@dataclass
class Path:
    def __init__(self, init_names: list[str], init_conns: list[ConnectionType]):
        self.path = init_names
        self.conns = init_conns

    def append(self, bro: str, conn: ConnectionType):
        return Path(self.path + [bro], self.conns + [conn])

    def contains(self, bro: str) -> bool:
        return bro in self.path

    def __repr__(self):
        if len(self.path) == 0:
            return ""
        string = self.path[0]
        for i in range(1, len(self.path)):
            string += " --" + self.conns[i].name + "-> " + self.path[i]
        return string
        # return " --> ".join(self.path)

    def __len__(self):
        return len(self.path)

@dataclass
class Connection:
    def __init__(self, bro: str, type: ConnectionType):
        self.bro = bro
        self.type = type
    
    def __repr__(self):
        return f"Connection(bro='{self.bro}', type='{self.type.name}')"
    
def parse_families_csv(filepath: str) -> dict[str, list[Connection]]:
    connections = dict()
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            headers = False
            reader = csv.DictReader(file)
            for row in file:
                if not headers:
                    headers = True
                    continue
                names = [ name.strip() for name in row.split(',') if name.strip()]
                if len(names) != 3:
                    print(f"invalid format for row: {row}")
                    continue
                for i in range(3):
                    names[i] = names[i].strip()
                    if names[i] not in connections:
                        connections[names[i]] = []
                connections[names[0]].append(Connection(names[1], ConnectionType.SPOUSE))
                connections[names[0]].append(Connection(names[2], ConnectionType.CHILD))
                connections[names[2]].append(Connection(names[0], ConnectionType.PARENT))
                connections[names[1]].append(Connection(names[0], ConnectionType.SPOUSE))
                connections[names[1]].append(Connection(names[2], ConnectionType.CHILD))
                connections[names[2]].append(Connection(names[1], ConnectionType.PARENT))
    except FileNotFoundError:
        print(f"Error: The file at {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return connections

# returns all possible paths from bro1 to bro2 (not including cycles), where each path is represented by a list of Connections
def find_relations(connections, bro1, bro2) -> list[Path]:
    paths = []
    stack = [(bro1, Path([bro1], [ConnectionType.SELF]))] # each element: (current_node, current_path)
    while stack:
        current_node, path = stack.pop()
        if current_node == bro2:
            paths.append(path)
            continue
        if current_node in connections:
            for connection in connections[current_node]:
                neighbor = connection.bro
                if not path.contains(neighbor):
                    new_path = path.append(neighbor, connection.type)
                    stack.append((neighbor, new_path))
    return paths

def print_relations(relations: list[Path], bro1: str, bro2: str) -> None:
    if len(relations) == 0:
        print(f"\nYou have NO relationship with {bro2}. You are not Bro2Bros :((\n")

    longest = max(relations, key=len)
    shortest = min(relations, key=len)
    print(f"\n---\nYour closest connection has {len(shortest) - 1} degrees of separation!\n{shortest}")
    print(f"\nYour most distant connection has {len(longest) - 1} degrees of separation!\n{longest}\n---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A program to find family relationships between Kappa Bros."
    )
    parser.add_argument(
        "families_csv",
        help="The file path to the CSV containing family information."
    )
    args = parser.parse_args()

    connections = parse_families_csv(args.families_csv)

    while True:
        print("\nLet's find a Bro2Bro relationship!")
        bro1 = input("What is your name? ")
        while bro1 not in connections:
            print(f"Could not find {bro1} in the family database. Please make sure the spelling (first and last name) is correct.")
            bro1 = input("What is your name? ")
        bro2 = input("Which brotherly relation would you like to explore? ")
        while bro2 not in connections:
            print(f"Could not find {bro2} in the family database. Please make sure the spelling (first and last name) is correct.")
            bro2 = input("Which brotherly relation would you like to explore? ")
        relations = find_relations(connections, bro1, bro2)
        print_relations(relations, bro1, bro2)
