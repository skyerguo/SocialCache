sleep 5
cat code/main/basic_config.json | jq '.caching_policy="Degree"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[75, 100, 0]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[1, 680, 0]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[1, 230, 0]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[1, 270, 0]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[108, 100, 1]' > code/main/config.json
sudo python3 -m code.main.main