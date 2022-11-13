# for cache_size in 15 20 25 50 75 100 ; do
#     # echo "cache_size: "$cache_size
#     cache_size_higher=$(($cache_size * 10))
#     # echo "cache_size_higher: "$cache_size_higher
#     cat code/main/basic_config.json | jq ".cache_size_level_3=$cache_size" > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq ".cache_size_level_2=$cache_size_higher" > code/main/basic_config.json

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="LRU-label"' > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="LRU-social"' > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq '.params=[0, 64.5, 310000]' > code/main/config.json
#     sudo python3 -m code.main.main

#     sleep 5
#     cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq '.params=[0, 60.0, 103]' > code/main/config.json
#     sudo python3 -m code.main.main
# done

# for i in `seq 0 20`; do
#     echo $i
#     # break
#     python3 -m code.analyze.main -l -m -e -c -p -d -z -n $i
# done

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-label"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 60.0, 103]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[0, 64.5, 310000]' > code/main/config.json
# sudo python3 -m code.main.main