# anki-vocab-builder
Build your vocabulary in Anki.

# Start testing the project

1. Run the following command at the root of the project to clone [anki-testing](https://github.com/krassowski/anki_testing)

   ```sh
   git clone https://github.com/krassowski/anki_testing
   ```

2. Then run the following command to install all dependencies.

   ```sh
   pip install -r requirements.txt
   ```

3. Open the Anki addon folder, create a link to the project (you may need to change the source and target directory):

   ```shell
   ln -s ~/PycharmProjects/anki-vocab-builder/vocab_builder ~/Library/Application Support/Anki2/addons21
   ```

4. Run `run_anki.py`:

   ```shell
   python3 run_anki.py
   ```