#! /bin/bash
make clean

make BT CLASS=B
mv ./bin/bt.B.x ./bin/8
make clean
