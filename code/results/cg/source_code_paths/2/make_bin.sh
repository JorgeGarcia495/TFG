#! /bin/bash
make clean

make BT CLASS=B
mv ./bin/bt.B.x ./bin/2
make clean
