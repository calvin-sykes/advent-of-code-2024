#!/bin/zsh

for i in `seq 1 1 25`; do
    NUM=$(printf %02d $i)
    [[ -f input/day$NUM.txt ]] || break
    msg="Day $i"
    len=${#msg}
    dashes=$(printf -- '-%.0s' {1..$len})
    echo $dashes"\n"$msg"\n"$dashes
    python day_$NUM.py
done
