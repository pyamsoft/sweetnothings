#!/usr/bin/env python3

import sys
from typing import Any

from sweetnothings.sweetnothings import SweetNothings


def _log(*args: Any):
    print("[main]: ", *args)


def main():
    # Remove ourself
    args = sys.argv[1:]

    if not args or len(args) <= 0:
        _log("Must provide at least one file path to a video file.")
        return

    model = SweetNothings()
    try:
        _log("Processing possible video files: ", args)
        for file_path in args:
            result = model.generate_subtitles(
                path=file_path,
            )
            if result:
                _log("Generated subtitles for ", file_path)
            else:
                _log("Failed to generate subtitles for ", file_path)
    finally:
        model.destroy()


if __name__ == "__main__":
    main()
