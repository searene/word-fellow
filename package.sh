
if [ -z "$1" ]; then
  TARGET_DIR="/tmp/word_fellow"
else
  TARGET_DIR="$1"
fi

rm -rf ${TARGET_DIR}
mkdir ${TARGET_DIR}
cp -r word_fellow/* ${TARGET_DIR}
pushd ${TARGET_DIR} || exit
zip -r ../word_fellow.ankiaddon *
rm -rf ${TARGET_DIR:?}/*
mv ../word_fellow.ankiaddon ${TARGET_DIR}

echo "The addon has been packaged to ${TARGET_DIR}/word_fellow.ankiaddon"
popd || exit
