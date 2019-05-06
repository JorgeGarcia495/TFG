#!/bin/bash

rm -r nas_bt_upper_bound
rm upperbound_bt
mkdir nas_bt_upper_bound
cp -r ../../nas_bt/* ./nas_bt_upper_bound/

python3.6 source_code_parser.py

make -C ./nas_bt_upper_bound/ clean
make -C ./nas_bt_upper_bound/ BT CLASS=B
make -C ./nas_bt_upper_bound/ clean
./nas_bt_upper_bound/bin/bt.B.x > upperbound_sc
