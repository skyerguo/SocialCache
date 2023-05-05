# for cache_size in 15 20 25 50 75 100 ; do
#     # echo "cache_size: "$cache_size
#     cache_size_higher=$(($cache_size * 10))
#     # echo "cache_size_higher: "$cache_size_higher
#     cat code/main/basic_config.json | jq ".cache_size_level_3=$cache_size" > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq ".cache_size_level_2=$cache_size_higher" > code/main/basic_config.json

# ## TwitterEgo
# cat code/main/basic_config.json | jq '.trace_dir="TwitterEgo"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[0.05, 50.5, 90]' > code/main/basic_config.json

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# for i in `seq 0 5`; do
#     python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
# done

# ## TwitterFull
# cat code/main/basic_config.json | jq '.trace_dir="TwitterFull"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[0.05, 50.5, 90]' > code/main/basic_config.json

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# for i in `seq 0 5`; do
#     python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
# done

# ## BrightkiteBigraphCommunity
# cat code/main/basic_config.json | jq '.trace_dir="BrightkiteBigraphCommunity"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[200, 0.0035, 10]' > code/main/basic_config.json

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# for i in `seq 0 5`; do
#     python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
# done

## GowallaBigraphCommunity
cat code/main/basic_config.json | jq '.trace_dir="GowallaBigraphCommunity"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[200, 0.0035, 10]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

for i in `seq 0 5`; do
    python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
done