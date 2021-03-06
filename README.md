# Chord Protocol
This implementation is based on the paper [https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)

## STEP #1
Clone the repository

``csjain@vm17-81:~$ git clone https://github.ncsu.edu/csjain/csjain_hw2.git``

## STEP #2
Change the active directory to repository folder

``csjain@vm17-81:~$ cd csjain_hw2``

## STEP #3
Run the make command. This will download all the necessary libraries and dependencies required for the program to run. It will also setup the environment.

``csjain@vm17-81:~/csjain_hw2$ make``

## STEP #4

Run your test/evaluation.

### For Batch mode

``csjain@vm17-81:~/csjain_hw2$ chord -i <batch_file> 8``

OR

### For Interactive mode

``csjain@vm17-81:~/csjain_hw2$ chord 8``


## EXTRA:

I have created a small script that runs a few scenarios with varying commands, this is just for convenience and should not be used for grading :P

``csjain@vm17-81:~/csjain_hw2$ ./run_test.sh``

## Assumptions:

To maintain the invariant of having the local information correct and eventually achieve global consistency `stab` and `fix` commands should be run multiple times and in a particular order. These commands ideally run periodically on each node but as it was mentioned by Professor, we are not supposed to fire these commands implicitly.

Thus, given a certain sequence of `add` and `join` the number of topology rings in the system can vary. This is referred to as stale information.

Here local information is a node's current state of predecessor and successor. The assumptions that maintain the invariant are listed below.

- #### Page 6 of paper, Second column, Last Paragraph:
As a simple example, suppose node N joins the system, and its ID lies between nodes Np and Ns. In its call to join(), N acquires Ns as its successor. Node Ns, when notified by N, acquires N as its predecessor. When Np next runs stabilize(), it asks Ns for its predecessor (which is now N); Np then acquires N as its successor. Finally, Np notifies N, and N acquires Np as its predecessor. At this point, all predecessor and successor pointers are correct. At each step in the process, Ns is reachable from Np using successor pointers; this means that lookups concurrent with the join are not disrupted.
- #### Page 8 of paper, Second column, Section 'Voluntary Node Departures':
Since Chord is robust in the face of failures, a node voluntarily leaving the system could be treated as a node failure. However, two enhancements can improve Chord performance when nodes leave voluntarily. First, a node N that is about to leave may transfer its keys to its successor before it departs. Second, N may notify its predecessor P and successor S before leaving. In turn, node P will remove n from its successor list, and add the last node in N’s successor list to its own list. Similarly, node S will replace its predecessor with N’s predecessor. Here we assume that N sends its predecessor to N, and the last node in its successor list to P.
