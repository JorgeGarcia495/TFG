#! /bin/bash
make clean

make BT CLASS=W
mv ./bin/bt.W.x ./bin/bt.W.x_7
make clean
