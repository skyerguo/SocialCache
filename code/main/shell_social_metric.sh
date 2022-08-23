sleep 20
cat code/main/basic_config.json | jq '.caching_policy="Degree"' > code/main/config.json
sudo python3 -m code.main.main

sleep 20
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
sudo python3 -m code.main.main

sleep 20
cat code/main/basic_config.json | jq '.caching_policy="Laplacian Centrality"' > code/main/config.json
sudo python3 -m code.main.main

sleep 20
cat code/main/basic_config.json | jq '.caching_policy="Betweenness Centrality"' > code/main/config.json
sudo python3 -m code.main.main

sleep 20
cat code/main/basic_config.json | jq '.caching_policy="Effective Size"' > code/main/config.json
sudo python3 -m code.main.main