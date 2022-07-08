RES_FILENAME="media_size.dat"

echo "------- Merging Result In ./result -------"
echo

rm -rf ${RES_FILENAME}
touch ${RES_FILENAME}

for file in `ls ./result`;
do
    echo "processing file result/${file}"
    cat "./result/${file}" | grep Length | awk '{print $2}' >> ${RES_FILENAME}
done

# result prompt
echo  "------- final result -------"
echo `wc -l ${RES_FILENAME}`