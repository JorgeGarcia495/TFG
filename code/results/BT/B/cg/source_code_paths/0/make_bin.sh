#! /bin/bash
make clean

make BT CLASS=B
mv ./bin/bt.B.x ./bin/bt.B.x_0
make clean
