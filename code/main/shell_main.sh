cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
sudo python3 -m code.main.main