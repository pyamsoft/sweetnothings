#!/usr/bin/env python3
import os
import sys

from pathlib import Path
from traceback import print_exc
from typing import Any, List, Callable

from sweetnothings.sweetnothings import SweetNothings

_XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", f"{Path.home()}")


class Locker:
    _LOCK_FILE_PATH = f"{_XDG_CACHE_HOME}/.cache/sweet-nothings.lock"

    @classmethod
    def _log(cls, *args: Any):
        print("[Locker]: ", *args)

    @classmethod
    def with_lock(
        cls,
        files: List[str],
        on_lock_claimed: Callable[[List[str]], None],
    ) -> bool:
        p = Path(cls._LOCK_FILE_PATH)
        if p.exists():
            cls._log("Lock file is already claimed by a different process")
            return False

        # noinspection PyBroadException
        try:
            cls._log("Claim lock file", cls._LOCK_FILE_PATH)
            p.touch()

            on_lock_claimed(files)
            return True
        except Exception as _:
            print_exc()
            return False
        finally:
            p.unlink()


class Main:
    @classmethod
    def _log(cls, *args: Any):
        print("[Main]: ", *args)

    @classmethod
    def _run_generator(cls, paths: List[str]):
        model = SweetNothings()
        try:
            cls._log("Processing possible video files: ", paths)
            for file_path in paths:
                result = model.generate_subtitles(
                    path=file_path,
                )
                if result:
                    cls._log("Generated subtitles for ", file_path)
                else:
                    cls._log("Failed to generate subtitles for ", file_path)
        finally:
            model.destroy()

    @classmethod
    def main(cls, paths: List[str]) -> bool:
        return Locker.with_lock(paths, cls._run_generator)


if __name__ == "__main__":
    # Remove ourself
    args = sys.argv[1:]

    if not args or len(args) <= 0:
        print("SweetNothings: Must provide at least one file path to a video file.")
    else:
        if Main.main(args):
            sys.exit(0)
        else:
            sys.exit(1)
