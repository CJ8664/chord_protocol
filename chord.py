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
    2: "ERROR: node id must be in [0,{limit})",
    3: "SYNTAX ERROR: {cmd} expects {act} parameters not {given}",
    4: "ERROR: Node {id} does not exist",
    5: "ERROR: Node {id} exists",
    6: "ERROR: {key_size} is not valid hash table size, will exit...",
    7: "ERROR: Input file not found, will exit..."
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

# Helper Methods

def print_error(type, args=dict()):
    '''
    Helper Method to print error messages
    '''
    print("< " + error_map[type].format(**args))


def is_int_node_id(id):
    '''
    Check if the given ID is integer
    '''
    try:
        id = int(id)
        if not ( 0 <= id < 2**key_size):
            print_error(2, {'limit': 2**key_size})
            return False
        else:
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

    if key_size < 1:
        print_error(6, {'key_size': key_size})
        sys.exit(-1)

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
        print_error(7)
        sys.exit(-1)

    with open(file_name, 'r') as input_handle:
        for command in input_handle:
            execute_command(command)

    # Remove last 'end' in test file and uncomment this line for mixed mode
    start_interactive_mode()


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
        if len(cmd_parts) != 1:
            print_error(3, {'cmd': 'end', 'act': 0, 'given': len(cmd_parts) - 1})
        else:
            # stop the program without saying anything.
            sys.exit()
    elif cmd_parts[0] == 'list':
        if len(cmd_parts) != 1:
            print_error(3, {'cmd': 'list', 'act': 0, 'given': len(cmd_parts) - 1})
        else:
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
            print_error(3, {'cmd': 'join', 'act': 2, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]) and is_int_node_id(cmd_parts[2]):
            return join_node(int(cmd_parts[1]), int(cmd_parts[2]))
    elif cmd_parts[0] == 'fix':
        if len(cmd_parts) != 2:
            print_error(3, {'cmd': 'fix', 'act': 1, 'given': len(cmd_parts) - 1})
        elif is_int_node_id(cmd_parts[1]):
            return fix_finger_table(int(cmd_parts[1]))
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
    elif cmd_parts[0] == '#' or command == '':
        # Handle comments in the test file
        pass
    else:
        print_error(0)
    return False


def list_ring():
    '''Show the id for each node in the ring.'''
    print('< Nodes: {}'.format(', '.join(map(str, sorted(topology.keys())))))


def add_node(id):
    '''Add node to ring with given id.'''
    if id in topology:
        print_error(5, {'id': id})
        return False
    node = Node(id)
    topology[id] = node
    print('< Added node {}'.format(id))


def drop_node(id):
    '''Remove node with given id from ring.'''
    if id not in topology:
        print_error(4, {'id': id})
        return False

    successor_id = topology[id].finger_table[0]
    predecessor_id = topology[id].predecessor
    del topology[id]

    # Point deleting node's predecessor's successor to deleting node's successor
    # A-B-C become A-C after deleting B
    if predecessor_id in topology: # Stabilize might not have been called
        topology[predecessor_id].finger_table[0] = successor_id

    # Tell id's successor that its predecessor no longer exist
    check_predecessor(successor_id)

    # Point deleting node's successor's predecessor to to deleting node's predecessor
    # A-B-C become A-C after deleting B
    if successor_id in topology: # Stabilize might not have been called
        topology[successor_id].predecessor = predecessor_id

    print('< Dropped node {}'.format(id))


def show_node(id):
    '''Show the successor, predecessor, and finger table for the given node.'''
    if id in topology:
        node = topology[id]
        print('< Node {}: suc {}, pre {}: finger {}'.format(id, node.finger_table[0], node.predecessor, ','.join(map(str, node.finger_table))))
    else:
        print_error(4, {'id': id})


def join_node(from_id, to_id):
    '''Join node from with the node to. Join should be call only once right after a node is added.'''
    both_node_exists = True

    if from_id not in topology:
        both_node_exists = False
        print_error(4, {'id': from_id})

    if to_id not in topology:
        both_node_exists = False
        print_error(4, {'id': to_id})

    if both_node_exists:
        if not topology[from_id].has_joined:
            # Join
            topology[from_id].has_joined = True

            topology[from_id].predecessor = None
            # Find successor for from_id start search with to_id
            predecessor_id, successor_id = find_successor(to_id, from_id)
            # print("For join {} {} we got predecessor: {} successor: {}".format(from_id, to_id, predecessor_id, successor_id))
            topology[from_id].finger_table[0] = successor_id

            # Notify successor_id that from_id might be its new predecessor
            # notify(successor_id, from_id)
            # print("After notif {} {} pred for {} is {}".format(successor_id, from_id, successor_id, topology[successor_id].predecessor))
            # Stabilize predecessor
            # stabilize_node(predecessor_id)
            # Fix fingers for predecessor
            # fix_finger_table(predecessor_id)
            # print("After fix finger for {} finger {}".format(predecessor_id, topology[predecessor_id].finger_table[0]))


def find_successor(to_id, from_id):
    '''Find the successor starting with to_node'''
    successor_id = topology[to_id].finger_table[0]

    # print("Find successor for {} starting with {}".format(from_id, to_id)),
    if (successor_id <= to_id): # Cyclic check
        if (to_id < from_id <= 2**key_size-1) or (0 <= from_id <= successor_id):
            # print("{} in cyclic check if".format(successor_id))
            return (to_id, successor_id)
        else:
            # forward the query around the circle to find the closest predecessor for from_id
            predecessor_id = closest_preceding_node(to_id, from_id)
            return find_successor(predecessor_id, from_id)
    else:
        if (to_id < from_id <= successor_id):
            return (to_id, successor_id)
        else:
            # forward the query around the circle to find the closest predecessor for from_id
            predecessor_id = closest_preceding_node(to_id, from_id)
            return find_successor(predecessor_id, from_id)


def closest_preceding_node(to_id, from_id):
    '''Search the local table for the highest predecessor of from_id'''
    for i in range(key_size - 1, -1, -1):
        finger_id = topology[to_id].finger_table[i]
        if (from_id <= to_id): # Cyclic check
            if (to_id < finger_id <= 2**key_size-1) or (0 <= finger_id < from_id):
                return finger_id
        else:
            if (to_id < finger_id < from_id):
                return finger_id
    return to_id


def stabilize_node(id):
    '''
    Called periodically. 'id' asks its successor about its predecessor,
    verifies if that predecessor is 'id' else tells the successor about 'id'
    '''
    if id not in topology:
        print_error(4, {'id': id})
        return False

    successor_id = topology[id].finger_table[0]
    # print("IN stab for {} successor is {}".format(id, successor_id))
    if successor_id not in topology:
        print("blah")
        pass
    else:
        successor = topology[successor_id]
        # print("sp {}".format(successor.predecessor))
        if successor.predecessor is not None:
            succ_pred_id = topology[successor.predecessor].id
            # print("successor {}'s predecessor is {}".format(successor_id, succ_pred_id))
            if(successor_id <= id):
                # print("in if stab for {} --> {},{},{} ".format(id, id, succ_pred_id, successor_id))
                if (id < succ_pred_id <= 2**key_size-1) or (0 <= succ_pred_id < successor_id):
                    topology[id].finger_table[0] = succ_pred_id
                    # print("finger: {}".format(topology[id].finger_table[0]))
            else:
                # print("in else stab for {} --> {},{},{}".format(id, id, succ_pred_id, successor_id))
                if (id < succ_pred_id < successor_id):
                    topology[id].finger_table[0] = succ_pred_id
        notify(topology[id].finger_table[0], id)
        # print("After stab for {} finger {}".format(id, topology[id].finger_table[0]))


def notify(to_id, from_id):
    '''
    Notify to_id that from_id might be its new predecessor
    '''
    if (to_id <= from_id): # Cyclic Check
        if (topology[to_id].predecessor is None or ((topology[to_id].predecessor < from_id <= 2**key_size-1) or (0 <= from_id < to_id))):
            topology[to_id].predecessor = from_id
    else:
        if (topology[to_id].predecessor is None or ((topology[to_id].predecessor < from_id < to_id))):
            topology[to_id].predecessor = from_id


def fix_finger_table(id):
    if id not in topology:
        print_error(4, {'id': id})
        return False
    for i in range(key_size):
        _, successor_id = find_successor(id, (id + 2**i)%(2**key_size))
        # print("Finger for {} entry {} val {}".format(id, i, successor_id))
        topology[id].finger_table[i] = successor_id


def check_predecessor(id):
    '''Check if id's predecessor doesn't exist'''
    if id in topology:
        predecessor_id = topology[id].predecessor
        if predecessor_id not in topology:
            topology[id].predecessor = None


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
