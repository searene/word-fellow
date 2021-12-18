ANKI_ADDON_FOLDER=$HOME/.local/share/Anki2/addons21/

function kill_anki_if_it_exists() {
  anki_pid=$(ps aux | grep '/bin/anki' | grep -v grep | awk '{print $2}')
  if [ ! -z $anki_pid ]; then
    kill $anki_pid
  fi
}

rm -rf $ANKI_ADDON_FOLDER/vocab_builder
cp vocab_builder $HOME/.local/share/Anki2/addons21/ -r

kill_anki_if_it_exists
anki
