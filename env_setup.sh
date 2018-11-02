#!/usr/bin/env bash

echo "****** Setting up Environment *******"
echo "###### Copying binaries #############"
sudo cp -pf chord.py /usr/bin/chord
echo "###### Done #########################"
echo "****** Run POST build test suite ****"
./run_test.sh
echo "###### Done #########################"
echo "************ ALL DONE ! *************"
