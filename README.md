# anki-vocab-builder
Build your vocabulary in Anki.

# Start testing the project

1. Run the following command to install all dependencies.

   ```sh
   pip install -r requirements.txt
   ```

2. Open the Anki addon folder, create a link to the project (you may need to change the source and target directory):

   ```shell
   ln -s ~/PycharmProjects/anki-vocab-builder/vocab_builder ~/Library/Application Support/Anki2/addons21
   ```

3. Run `run_anki.py`:

   ```shell
   python3 run_anki.py
   ```