#! /bin/bash
make clean

make SP CLASS=D
mv ./bin/sp.D.x ./bin/sp.D.x_1
make clean