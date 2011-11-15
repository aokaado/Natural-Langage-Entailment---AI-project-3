#!/bin/bash
ffile="gah"
for ((  i = 0 ;  i <= 100;  i++  ))
do
	ffile="eval_rte.py ../data/RTE2_dev.xml ../data/results.txt$i"
	res=$(python $ffile)
	echo $i$res
done
