# for cache_size in 15 20 25 50 75 100 ; do
#     # echo "cache_size: "$cache_size
#     cache_size_higher=$(($cache_size * 10))
#     # echo "cache_size_higher: "$cache_size_higher
#     cat code/main/basic_config.json | jq ".cache_size_level_3=$cache_size" > code/main/config_tmp.json
#     cat code/main/config_tmp.json | jq ".cache_size_level_2=$cache_size_higher" > code/main/basic_config.json