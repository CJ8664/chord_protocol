#!/usr/bin/env bash

printf "************ Running Test 1 ************"
python chord.py -i test_cases/test1.tst 3 > test_cases/test1.res
diff test_cases/test1.res test_cases/test1.op
printf "****************************************\n\n\n"
