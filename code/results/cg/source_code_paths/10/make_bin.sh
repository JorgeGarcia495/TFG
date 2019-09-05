#! /bin/bash
make clean

make BT CLASS=D
mv ./bin/bt.D.x ./bin/bt.D.x_10
make clean
