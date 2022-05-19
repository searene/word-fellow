# WordFellow

## Introduction

WordFellow is a simple Anki add-on that helps you to build your vocabulary word by word. The idea is very simple:

1. Import a document in your target language.
2. WordFellow splits the document into words and lets you check them one by one. You can add any of the words to anki in the process, or only mark them and study later.
3. When you are done with the document, you will know all the words in it, then you can start reading/listening to the document.

I'll illustrate each step with a GIF:

1. Import the texts in your target language into the addon.

![import](description/img/import.gif)

2. The addon splits your texts into words, which are shown to you one by one. Each word is accompanied by the sentences that contain the word. You can then check the word one by one telling WordFellow how you want to deal with the word. Here are 4 ways in total:

- **Add to anki**: You don't know the word, you want to add the word to anki immediately.
- **Ignore**: You want to ignore the word because it's useless to you. E.g. names, locations, etc.
- **I Know It**: You know the word.
- **Study Later**: You don't know the word, but you are not in the mood for adding it to Anki immediately, you want to add it later.

![review](description/img/review.gif)

3. You can switch between different statuses at any time.

![status](description/img/status.gif)

Note that word status applies to all the documents at the same time, no matter which document you are currently reviewing. For example, suppose you have two documents, both contain the same word `the`. Suppose you mark the word as `Study Later` in one of the documents, the status of the word `the` in the other document will be changed to `Study Later` too. So you don't need to repetitively check the same word in different documents.
Build your vocabulary in Anki.

## Build

1. Run the following command to install all dependencies.

   ```sh
   pip install -r requirements.txt
   ```

2. Open the Anki addon folder, create a link to the project (you may need to change the source and target directory):

   ```shell
   ln -s ~/PycharmProjects/word-fellow/word_fellow ~/Library/Application\ Support/Anki2/addons21
   ```

3. Run `run_anki.py` to start Anki along with this addon.

   ```shell
   python3 run_anki.py
   ```