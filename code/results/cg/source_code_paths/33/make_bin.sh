#! /bin/bash
make clean

make BT CLASS=W
mv ./bin/bt.W.x ./bin/bt.W.x_33
make clean
