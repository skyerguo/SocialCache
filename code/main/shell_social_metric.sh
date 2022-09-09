sleep 5
cat code/main/basic_config.json | jq '.caching_policy="Degree"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 56.0, 13]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 64.5, 310000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 57.5, 54000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 54.0, 52000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 60.0, 103]' > code/main/config.json
sudo python3 -m code.main.main