sleep 5
cat code/main/basic_config.json | jq '.caching_policy="Degree"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config_tmp2.json
# cat code/main/config_tmp2.json | jq '.trace_dir="gtc_long_trace"' > code/main/config.json
# sudo python3 -m code.optimize.try_LRU_social  