SRC_DAT_FILENAME=~/total_url.txt
PICK_LINES_FILENAME=sampled_urls.dat

echo "------- processing data file -------"
echo
# get file total number of lines
total_line_num=`wc -l ${SRC_DAT_FILENAME} | awk '{print $1}'`
echo ">> get file lines number : "$total_line_num

# random pick one of ten lines from source file
pick_lines=`expr ${total_line_num} / 10`
echo ">> going to random pick "${pick_lines}" lines"
shuf ${SRC_DAT_FILENAME} -n ${pick_lines} -o ${PICK_LINES_FILENAME}
sed -i 's/[",]//g' ${PICK_LINES_FILENAME}
echo ">> random picked lines saved to : ["${PICK_LINES_FILENAME}"]"

# split to files
echo ">> going to split lines to "${split_lines}"items"
split_lines=`expr ${pick_lines} / $1`
rm -rf data
mkdir -p data
split -l ${split_lines} ${PICK_LINES_FILENAME} -d -a 4 ./data/url_list_

# start wget
echo ">> start wget process"
rm -rf result
mkdir -p result
for file in `ls data`;
do
    wc -l data/${file}
    wget -i data/${file} -o result/${file}.res --spider &
    echo launch ${file}
done
