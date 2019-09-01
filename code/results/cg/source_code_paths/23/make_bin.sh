#! /bin/bash
make clean

make BT CLASS=W
mv ./bin/bt.W.x ./bin/bt.W.x_23
make clean
