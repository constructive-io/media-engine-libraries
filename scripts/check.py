#!/usr/bin/env python3
"""Is media-index.json an index? The answer that needs nothing installed.

    python3 scripts/check.py            # this index
    python3 scripts/check.py FOLDER     # another one

It says everything wrong with the file: a library with no name, an address
that is not one, a library listed twice. It needs Python 3.9 and nothing
else, so it runs on every push. It does not fetch the libraries: an index
says where a library is and does not vouch for it. `me library add NAME`,
from Constructive Media, reads and checks the library itself.
"""

import json
import re
import sys
from pathlib import Path

INDEX = "media-index.json"
HOLDS = ("voices", "banks", "faces")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SHORT = re.compile(r"[A-Za-z0-9][\w.-]*/(?!\.{1,2}$)[\w.-]+")
FETCHED = ("https://", "ssh://", "git@", "file://")
KNOWN = {"index", "summary", "homepage", "libraries"}
OF_A_LIBRARY = {"name", "source", "summary", "license", "holds", "tags", "homepage"}


def address(source):
    """Whether `source` is an address an index may name: never a path, an option or a program to run."""
    source = source.strip()
    if not source or source.startswith("-") or "::" in source or any(mark in source for mark in "\n\r\0 "):
        return False
    return bool(SHORT.fullmatch(source)) or source.startswith(FETCHED)


def check(folder):
    """Everything wrong with the index in `folder`: (name, how many libraries, problems, notes)."""
    written = Path(folder).expanduser() / INDEX
    if not written.is_file():
        return None, 0, [f"{folder} is not an index: it has no {INDEX}"], []
    try:
        index = json.loads(written.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return None, 0, [f"{written} cannot be read as JSON: {error}"], []
    if not isinstance(index, dict):
        return None, 0, [f"{written} should hold an object, in braces"], []

    problems, notes = [], []
    name = index.get("index")
    if not isinstance(name, str) or not NAME.fullmatch(name):
        problems.append('"index" is the index\'s name: lower case letters and numbers, joined by hyphens')
        name = None
    for key in sorted(set(index) - KNOWN):
        notes.append(f'"{key}" is not something an index says; it is ignored')
    given = index.get("libraries", [])
    if not isinstance(given, list):
        problems.append('"libraries" should be a list')
        given = []

    seen, count = set(), 0
    for number, one in enumerate(given, start=1):
        if not isinstance(one, dict):
            problems.append(f"library {number} should be an object, in braces")
            continue
        called, which = one.get("name"), f"library {number}"
        if not isinstance(called, str) or not NAME.fullmatch(called):
            problems.append(f'{which}: "name" is what the library calls itself: lower case, with hyphens')
        else:
            which = f"`{called}`"
            if called in seen:
                problems.append(f"{which} is listed twice: a name is one library")
            seen.add(called)
            count += 1
        source = one.get("source")
        if not isinstance(source, str) or not address(source):
            problems.append(f'{which}: "source" is where the library is: owner/name on GitHub, or an address that '
                            "starts https://, ssh:// or git@")
        for key in ("summary", "license", "homepage"):
            if key in one and (not isinstance(one[key], str) or not one[key].strip()):
                problems.append(f'{which}: "{key}" should be a line of words')
        if not one.get("summary"):
            notes.append(f"{which} has no summary, so a search finds it only by its name")
        if not one.get("license"):
            notes.append(f"{which} does not say under what terms it may be used")
        for key in ("holds", "tags"):
            words = one.get(key, [])
            if not isinstance(words, list) or not all(isinstance(word, str) and word.strip() for word in words):
                problems.append(f'{which}: "{key}" should be a list of words')
            elif key == "holds":
                for what in words:
                    if what not in HOLDS:
                        problems.append(f'{which}: "holds" names `{what}`. A library holds any of {", ".join(HOLDS)}')
        for key in sorted(set(one) - OF_A_LIBRARY):
            notes.append(f'{which}: "{key}" is not something an index says of a library; it is ignored')
    if given != sorted(given, key=lambda one: str(one.get("name")) if isinstance(one, dict) else ""):
        notes.append("the libraries are not in the order of their names, which is how a person looks for one")
    return name, count, problems, notes


def main(arguments):
    folder = arguments[0] if arguments else Path(__file__).resolve().parent.parent
    name, count, problems, notes = check(folder)
    for problem in problems:
        print(problem)
    for note in notes:
        print(f"note: {note}")
    if problems:
        print(f"{len(problems)} problem(s): this is not an index yet", file=sys.stderr)
        return 1
    print(f"ok: {name}, {count} librar{'y' if count == 1 else 'ies'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
