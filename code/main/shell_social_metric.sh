cat code/main/basic_config.json | jq '.trace_dir="TwitterFull"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0, 0, 0]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[12000, 64.9, 510000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="HITS"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[15000, 64.8, 510000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="ClusteringCoefficient"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 66.0, 320]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="DegreeCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 66.0, 310]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="BetweennessCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 60.0, 54000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="ClosenessCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 56.0, 52000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EigenvectorCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 54.0, 53000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LaplacianCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[21000, 55.1, 62000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EgoBetweennessCentrality"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[18000, 57.5, 54000]' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[0.0, 65.0, 10.0]' > code/main/config.json
sudo python3 -m code.main.main

for i in `seq 0 9`; do
    python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
done