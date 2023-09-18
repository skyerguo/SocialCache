#!/bin/bash
relation_file="./data/traces/GooglePlus/relations.txt"
c_source_dir="./code/util/c_lang"
result_dir="./data/social_metric_dict/GooglePlus/"

#2. compile
gcc $c_source_dir/effective_size.c -o effective_size -lpthread

#3. exec
./effective_size -r 1 -f $relation_file

#4. copy result
mv ./effective_size.csv $result_dir/EffectiveSize.csv

#5. clean
rm effective_size
