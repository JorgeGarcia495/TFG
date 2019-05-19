#!/bin/bash

make -C ../../results/upper_bound/nas_bt_upper_bound/ clean
make -C ../../results/upper_bound/nas_bt_upper_bound/ BT CLASS=B
make -C ../../results/upper_bound/nas_bt_upper_bound/ clean
../../results/upper_bound/nas_bt_upper_bound/bin/bt.B.x > ../../results/upper_bound/upperbound_sc
