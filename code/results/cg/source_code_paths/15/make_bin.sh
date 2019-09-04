#! /bin/bash
make clean

make BT CLASS=W
mv ./bin/bt.D.x ./bin/bt.D.x_15
make clean
