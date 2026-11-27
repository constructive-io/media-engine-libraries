# media-libraries — agent guide

The index [Constructive Media](https://github.com/constructive-io/constructive-media)
reads when no other is named. One file, [`media-index.json`](./media-index.json), lists
libraries and where each is. [README.md](./README.md) says what every key means.

## Rules

- **Only libraries anybody can fetch.** A private library is not listed here: a person
  who searched for it could not add it.
- **Never list a voice without consent.** Before adding a library that holds voices,
  read its `media-library.json`: every voice has a `consent` that says whose it is and
  by what right. A library of voices cloned from recordings somebody found is refused.
- **`name` is what the library calls itself.** The engine refuses a library whose own
  `media-library.json` says another name.
- **`source` is an address, never a path.** `owner/name`, or one that starts `https://`,
  `ssh://` or `git@`.
- **Keep the libraries in the order of their names**, and keep the table in the README
  the same as the file.
- **Nothing but the index lives here.** No sounds, no clips, no pictures.

## Before you say it is done

```sh
python3 scripts/check.py                       # must print ok
media library check <a clone of the library>   # for every library you added
```
