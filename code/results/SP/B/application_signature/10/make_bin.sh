#! /bin/bash
make clean

make SP CLASS=B
mv ./bin/sp.B.x ./bin/sp.B.x_10
make clean
