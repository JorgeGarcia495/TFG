#! /bin/bash
make clean

make BT CLASS=B
mv ./bin/bt.B.x ./bin/25
make clean
