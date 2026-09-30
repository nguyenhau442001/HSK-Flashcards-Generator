# HSK 3.0 vocabulary data

The HSK 3.0 decks follow the 2025 Chinese Proficiency Test syllabus dataset
exported from the official HSK vocabulary endpoint. The source CSV is saved
beside this file as `source_hsk_2025.csv` so the level assignments can be
recreated with `python3 tools/build_hsk30_vocab.py --build`.

Source and license: [profesorm/hsk30](https://github.com/profesorm/hsk30),
licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The repository describes its vocabulary data as an extraction of the official
Chinese Testing International syllabus and gives the source site as
[chinesetest.cn](https://www.chinesetest.cn/).

The syllabus assigns 300, 200, 500, 1,000, 1,600, and 1,800 new entries to
levels 1–6. It has one shared 5,600-entry advanced list for levels 7–9. The app
stores a copy for each of levels 7, 8, and 9 so their study progress remains
separate.

Vietnamese meanings are retained from the app's existing HSK decks when the
same word is present. Meanings for other entries are draft machine translations
prepared with Google Translate, using the syllabus part of speech as context;
they have not had a complete human review. Examples are reused from the
project's existing HSK decks and sentence bank where an exact word match is
available. Entries without a suitable existing example leave the example
fields blank, and the flashcard hides the example panel for those entries.
