#!/usr/bin/python

import sys
import os

## Globals

# Store the key length for Topology table
key_size = -1

# Store the path in input file
file_name = ''

# Store the topological information about the id -> Node
topology = dict()

# Error mapping
error_map = {
    0: "ERROR: invalid command",
    1: "ERROR: invalid integer {id}",
    2: "ERROR: node id must be in [0,{id})",
    3: "SYNTAX ERROR: {cmd} expects {act} parameters not {given}",
    4: "ERROR: Node {id} does not exist",
    5: "ERROR: Node {id} exists"
}


class Node:
    '''
    Class to store information about a Node in the network
    '''
    def __init__(self, id, key_size):
        self.id = id
        self.predecessor = None
        self.finger_table = dict()

        # Initialize Finger table
        for i in range(1, key_size + 1):
            self.finger_table[i] = self.id



def print_error(type, args=dict()):
    '''
    Helper Method to print error messages
    '''
    print(error_map[type].format(**args))


def get_operation_mode():
    '''Parse the argument and return the operation mode'''
    global key_size, file_name

    if len(sys.argv) > 2:
        # Batch mode
        file_name = sys.argv[2]
        key_size = int(sys.argv[3])
        return 0
    else:
        # Interactive mode
        key_size = int(sys.argv[1])
        return 1


def start_batch_mode():
    '''
    Process the input file and interpret the commands
    '''
    if not os.path.exists(file_name):
        print("Input file not found, will exit...")
        sys.exit(-1)

    with open(file_name, 'r') as input_handle:
        for command in input_handle:
            execute_command(command)


def start_interactive_mode():
    '''
    Start the program in Interactive mode
    '''
    print_error(1, {'id': 100})


def execute_command(command):
    '''
    Execute the given command
    '''
    if command == 'end':
        sys.exit()
    elif command == 'list':
        list_ring()
    else:
        print_error(0)


def list_ring():
    '''
    Show the id for each node in the ring.
    '''
    pass

def main():
    '''
    Main function that execute the entire Program
    '''
    mode = get_operation_mode()
    if mode == 0:
        # Batch mode
        start_batch_mode()
    elif mode == 1:
        # Interactive mode
        start_interactive_mode()


if __name__ == '__main__':
    main()
