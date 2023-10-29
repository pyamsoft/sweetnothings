#!/usr/bin/env python3

import sys
from typing import Any

from sweetnothings.sweetnothings import SweetNothings


def _log(*args: Any):
    print("[main]: ", *args)


def main():
    args = sys.argv
    if not args or len(args) <= 1:
        _log("Must provide at least one file path to a video file.")
        return

    model = SweetNothings()
    try:
        for file_path in args:
            model.generate_subtitles(
                path=file_path,
            )
    finally:
        model.destroy()


if __name__ == "__main__":
    main()
