#! /bin/bash
make clean

make BT CLASS=W
mv ./bin/bt.W.x ./bin/bt.W.x_14
make clean
