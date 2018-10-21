#!/usr/bin/python

import argparse
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
    def __init__(self, id):
        self.id = id
        self.has_joined = False
        self.predecessor = None
        self.finger_table = []

        # Initialize Finger table
        for i in range(key_size):
            self.finger_table.append(self.id)

    def join(self, to_node):
        '''
        Join a Chord ring containing to_node
        '''
        self.predecessor = None
        self.finger_table[0] = to_node.find_successor(self)
        self.has_joined = True

    def find_successor(self, from_node):
        '''Find the successor starting with to_node'''
        if (from_node.id > self.id and from_node.id <= self.finger_table[0]):
            return from_node.finger_table[0]
        else:
            # forward the query around the circle
            successor = topology[self.finger_table[0]]
            candidate_id = successor.closest_preceding_node(from_node.id)
            candidate = topology[candidate_id]
            if candidate_id == self.id:
                return candidate_id
            return candidate.find_successor(from_node)


    def closest_preceding_node(self, from_id):
        '''Search the local table for the highest predecessor of id'''
        for i in range(key_size - 1, -1, -1):
            if (self.finger_table[i] > self.id and self.finger_table[i] < from_id):
                return self.finger_table[i]
        return self.id


    def stabalize(self):
        '''
        Called periodically. n asks the successor about its predecessor,
        verifies if n's immediate successor is consistent,
        and tells the successor about n
        '''
        successor = topology[self.finger_table[0]]
        if successor.predecessor:
            temp = topology[successor.predecessor]
            if (temp.id > self.id and temp.id < successor.id):
                self.finger_table[0] = temp.id;
                successor = topology[self.finger_table[0]]
        successor.notify(self.id);

    def notify(self, id):
        '''
        it might be our predecessor
        '''
        if (self.predecessor is None or (id > self.predecessor and id < self.id)):
            self.predecessor = id;


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

    parser = argparse.ArgumentParser(description='CHORD protocol simulation')

    parser.add_argument('key_size', type=int, nargs=1,
                    help='Key size for finger table')

    parser.add_argument('-i', dest='file_name', action='store',
                    help='Input file for batch mode')

    args = parser.parse_args()
    file_name = args.file_name
    key_size = args.key_size[0]

    if file_name:
        # Batch mode
        return 0
    else:
        # Interactive mode
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
    try:
        while True:
            execute_command(raw_input('> '))
    except KeyboardInterrupt as ex:
        pass


def execute_command(command):
    '''
    Execute the given command
    '''
    command = command.strip()
    cmd_parts = command.split(' ')
    if cmd_parts[0] == 'end':
        # stop the program without saying anything.
        sys.exit()
    elif cmd_parts[0] == 'list':
        return list_ring()
    elif cmd_parts[0] == 'add':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'add', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return add_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'drop':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'drop', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return drop_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'join':
        if len(cmd_parts) != 3:
            print_error(3, {'cmd': 'fix', 'act': 2, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]) and is_int_node_id(cmd_parts[2]):
            return join_node(int(cmd_parts[1]), int(cmd_parts[2]))
    elif cmd_parts[0] == 'fix':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'fix', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return fix_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'stab':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'stab', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return stabilize_node(int(cmd_parts[1]))
    elif cmd_parts[0] == 'show':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'show', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return show_node(int(cmd_parts[1]))
    else:
        print_error(0)
    return False


def list_ring():
    '''Show the id for each node in the ring.'''
    print('Nodes: {}'.format(', '.join(map(str, sorted(topology.keys())))))


def add_node(id):
    '''Add node to ring with given id.'''
    node = Node(id)
    topology[id] = node
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
    if id in topology:
        node = topology[id]
        print('Node {}: suc {}, pre {}: finger {}'.format(id, node.finger_table[0], node.predecessor, ','.join(map(str, node.finger_table))))
    else:
        print_error(4, {'id': id})

def join_node(from_id, to_id):
    '''Join node from with the node to. Join should be call only once right after a node is added.'''
    global topology

    both_node_exists = True

    if from_id not in topology:
        both_node_exists = False
        print_error(4, {'id': from_id})

    if to_id not in topology:
        both_node_exists = False
        print_error(4, {'id': to_id})

    if both_node_exists:
        from_node = topology[from_id] # current
        to_node = topology[to_id] # current

        if not from_node.has_joined:
            from_node.join(to_node)
            # topology[from_id] = from_node
            # Stabalize
            from_node.stabalize()
            # Notify
            from_node.notify(to_id)
            # Fix fingers
            to_node.fix_finger_table()


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
