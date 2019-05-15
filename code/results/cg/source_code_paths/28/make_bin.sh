#! /bin/bash
make clean

make BT CLASS=B
mv ./bin/bt.B.x ./bin/28
make clean
