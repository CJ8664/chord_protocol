#!/usr/bin/env bash

for i in `seq 1 10`
do
  printf "************ Running Test $i ************"
  python chord.py -i test_cases/test$i.tst 2 > test_cases/test$i.res
  diff test_cases/test$i.res test_cases/test$i.op
  printf "****************************************\n\n\n"
done
