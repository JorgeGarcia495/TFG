#! /bin/bash
make clean

make SP CLASS=B
mv ./bin/sp.B.x ./bin/sp.B.x_14
make clean