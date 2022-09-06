python3 -m code.trace.make_trace3

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="PageRank"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

python3 -m code.analyze.main -l -m -c -n 2
python3 -m code.analyze.main -l -m -c -n 1
python3 -m code.analyze.main -l -m -c -n 0