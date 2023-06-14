# ## TwitterEgo
# cat code/main/basic_config.json | jq '.trace_dir="TwitterEgo"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[0.05, 50.5, 90]' > code/main/basic_config.json

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="Second-Hit-LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# for i in `seq 0 6`; do
#     python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
# done

# ## TwitterFull
# cat code/main/basic_config.json | jq '.trace_dir="TwitterFull"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.params=[0.05, 50.5, 90]' > code/main/basic_config.json

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="Second-Hit-LRU"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
# sudo python3 -m code.main.main

# sleep 5
# cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
# cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
# sudo python3 -m code.main.main

# for i in `seq 0 6`; do
#     python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
# done

## BrightkiteBigraphCommunity
cat code/main/basic_config.json | jq '.trace_dir="BrightkiteBigraphCommunity"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[200, 0.0035, 10]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

for i in `seq 0 5`; do
    python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
done

## GowallaBigraphCommunity
cat code/main/basic_config.json | jq '.trace_dir="GowallaBigraphCommunity"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[200, 0.0035, 10]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

for i in `seq 0 5`; do
    python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
done

## GooglePlus
cat code/main/basic_config.json | jq '.trace_dir="GooglePlus"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.params=[200, 0.0035, 10]' > code/main/basic_config.json

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="RAND"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="FIFO"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="LRU-Social"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config.json
sudo python3 -m code.main.main

sleep 5
cat code/main/basic_config.json | jq '.caching_policy="EffectiveSize"' > code/main/config_tmp.json
cat code/main/config_tmp.json | jq '.use_priority_queue=false' > code/main/config.json
sudo python3 -m code.main.main

for i in `seq 0 5`; do
    python3 -m code.analyze.main -l -m -e -c -p -d -q -y -z -n $i
done