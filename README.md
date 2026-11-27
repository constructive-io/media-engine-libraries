# media-engine-libraries

<p align="center" width="100%">
  <img height="250" src="https://raw.githubusercontent.com/constructive-io/constructive/refs/heads/main/assets/outline-logo.svg" alt="Constructive" />
</p>

<p align="center" width="100%">
  <a href="https://github.com/constructive-io/media-engine-libraries/actions/workflows/check.yml">
    <img height="20" src="https://github.com/constructive-io/media-engine-libraries/actions/workflows/check.yml/badge.svg" alt="Check status" />
  </a>
  <a href="https://github.com/constructive-io/media-engine-libraries/blob/main/LICENSE"><img height="20" src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license" /></a>
</p>

<p align="center" width="100%">
  Where a library of voices, sounds and faces is found by its name.
</p>

A *library* for [Constructive Media](https://github.com/constructive-io/media-engine)
is a repository of voices to clone, banks of sounds and faces. This is the
*index* the engine reads when no other is named: one file,
[`media-index.json`](./media-index.json), that lists libraries and where each
one is.

```sh
media library search              # every library listed here
media library search weather sounds  # those with every word in them
media library add foley           # add one by its name
```

`media` is the command of Constructive Media.

## What is listed

| Library | Holds | Terms | What it is |
| --- | --- | --- | --- |
| [`foley`](https://github.com/constructive-io/media-engine-library-foley) | banks of sounds | CC0-1.0 | Sound effects, ambience loops and short music beds, every one made by a script |

## What an index is, and is not

An index says where a library is, and nothing more. It does not hold a
library, and it does not vouch for one: the engine reads and checks a library
when it is added, as it would any other, and refuses one that is not called
what the index calls it. A render never needs an index. A project pins its
libraries by commit in `media-libraries.json`, and `media library install` fetches
those from their own addresses.

Anybody can keep an index of their own, in a folder or a repository, and have
their machine read it first:

```sh
export CONSTRUCTIVE_MEDIA_LIBRARY_INDEX=~/indexes/ours,constructive-io/media-engine-libraries
```

## List a library here

Start one with `media init library NAME`, from [media-engine-boilerplates](https://github.com/constructive-io/media-engine-boilerplates),
and open a pull request that adds it to `media-index.json`, in the order of
its name:

```json
{
  "name": "lighthouse",
  "source": "harbour-office/lighthouse-voices",
  "summary": "The keepers of the light, and the weather they keep it in.",
  "license": "CC-BY-4.0",
  "holds": ["voices", "banks"],
  "tags": ["weather", "sea"]
}
```

| Key | Is |
| --- | --- |
| `name` | what the library calls itself in its own `media-library.json` |
| `source` | where it is: `owner/name` on GitHub, or an address that starts `https://`, `ssh://` or `git@` |
| `summary` | one line a search can find it by |
| `license` | the terms it may be used under |
| `holds` | any of `voices`, `banks`, `faces` |
| `tags` | more words to find it by |

To be listed, a library has to be one anybody can fetch, say its terms, and
pass `media library check`. A library with voices says for every one whose voice
it is and by what right it is there; a voice with no consent written down is
not listed, and neither is a voice cloned from a recording somebody found.

```sh
python3 scripts/check.py     # is the file an index; needs nothing installed
```

## License

The index is under the [MIT license](./LICENSE). Each library has terms of its
own, written in its `media-library.json`.
