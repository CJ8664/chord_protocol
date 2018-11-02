#!/usr/bin/env bash

for i in `seq 1 19`
do
  printf "************ Running Test $i ************"
  chord -i test_cases/test$i.tst 2 > test_cases/test$i.res
  diff test_cases/test$i.res test_cases/test$i.op
  printf "****************************************\n\n\n"
done
