# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="Degree"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config.json
# sudo python -m code.optimize.hill_climbing

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python -m code.optimize.hill_climbing