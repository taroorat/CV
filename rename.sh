#!/usr/bin/env bash
count=0
for i in `ls $1`
do
  count=`expr $count + 1`
  mv $1/$i $1/`printf "%06d" $count`.png
done
