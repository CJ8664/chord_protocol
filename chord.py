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
        self._has_joined = False
        self.predecessor = None
        self.finger_table = []

        # Initialize Finger table
        for i in range(1, key_size + 1):
            self.finger_table.append(self.id)


# Helper Methods

def print_error(type, args=dict()):
    '''
    Helper Method to print error messages
    '''
    print(error_map[type].format(**args))


def is_int_node_id(id):
    '''
    Check if the given ID is integer
    '''
    try:
        _ = int(id)
        return True
    except Exception as ex:
        print_error(1, {'id': id})
        return False


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
    cmd_parts = command.split(' ')
    if cmd_parts[0] == 'end':
        # stop the program without saying anything.
        sys.exit()
    elif cmd_parts[0] == 'list':
        list_ring()
    elif cmd_parts[0] == 'add':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'add', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]):
            add_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'drop':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'drop', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]):
            drop_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'join':
        if len(cmd_parts) != 3:
            print_error(3, {'cmd': 'fix', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]) and is_int_node_id(cmd_parts[2]):
            join_node(int(cmd_parts[1]), int(cmd_parts[2]))
    elif cmd_parts[0] == 'fix':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'fix', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]):
            fix_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'stab':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'stab', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]):
            stabilize_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'show':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'show', 'act': 2, 'given': len(cmd_parts)})
        if is_int_node_id(cmd_parts[1]):
            show_node(int(cmd_parts[1]))
    else:
        print_error(0)


def list_ring():
    '''Show the id for each node in the ring.'''
    print('Nodes: {}'.format(', '.join(sorted(topology.keys()))))


def add_node(id):
    '''Add node to ring with given id.'''
    print('Added node {}'.format(id))


def drop_node(id):
    '''Remove node with given id from ring.'''
    print('Dropped node {}'.format(id))


def stabilize_node(id):
    '''Stabilize method for given node.'''
    pass


def fix_node(id):
    '''Fix the finger table for given node.'''
    pass


def show_node(id):
    '''Show the successor, predecessor, and finger table for the given node.'''
    print('Node {}: suc {}, pre {}: finger {}'.format(id, id, id, id))


def join_node(from_id, to_id):
    '''Join node from with the node to. Join should be call only once right after a node is added.'''
    pass


def main():
    '''Main function that execute the entire Program'''
    mode = get_operation_mode()
    if mode == 0:
        # Batch mode
        start_batch_mode()
    elif mode == 1:
        # Interactive mode
        start_interactive_mode()


if __name__ == '__main__':
    main()
