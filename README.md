# Chord Protocol
This implementation is based on the paper [https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)

## STEP #1
Clone the repository

``csjain@vm17-81:~$ git clone https://github.ncsu.edu/csjain/chord_protocol.git``

## STEP #2
Change the active directory to repository folder

``csjain@vm17-81:~$ cd chord_protocol``

## STEP #3
Run the make command. This will download all the necessary libraries and dependencies required for the program to run. It will also setup the environment.

``csjain@vm17-81:~/chord_protocol$ make``

## STEP #4

Run your test/evaluation.

### For Batch mode

``csjain@vm17-81:~/chord_protocol$ chord -i <batch_file> 8``

OR

### For Interactive mode

``csjain@vm17-81:~/zookeeper_game$ chord -i <batch_file> 8``


## EXTRA:

I have created a small script that runs a few scenarios with varying commands, this is just for convenience and should not be used for grading :P

``csjain@vm17-81:~/chord_protocol$ ./run_test.sh``
