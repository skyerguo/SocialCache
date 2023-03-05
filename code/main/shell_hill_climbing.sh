cat code/main/basic_config.json | jq '.trace_dir="TwitterSmall"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 0, 0]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="HITS"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="ClusteringCoefficient"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="DegreeCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="ClosenessCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EigenvectorCentrality"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EgoBetweennessCentrality"' > code/main/config.json
sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python -m code.optimize.hill_climbing