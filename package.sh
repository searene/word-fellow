TARGET_DIR=/tmp/word_fellow
rm -rf ${TARGET_DIR}
mkdir ${TARGET_DIR}
cp -r word_fellow/* ${TARGET_DIR}
echo "\n\n\ninit_addon()\n" >> ${TARGET_DIR}/__init__.py
pushd ${TARGET_DIR} || exit
zip -r ../word_fellow.ankiaddon *
rm -rf ${TARGET_DIR:?}/*
mv ../word_fellow.ankiaddon ${TARGET_DIR}

echo "The addon has been packaged to ${TARGET_DIR}/word_fellow.ankiaddon"
popd || exit
