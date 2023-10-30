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
        on_lock_claimed: Callable[[Path, List[str]], None],
    ) -> bool:
        p = Path(cls._LOCK_FILE_PATH)
        if p.exists():
            cls._log("Lock file is already claimed by a different process")
            current_status = p.read_text()
            cls._log("Current Status === ")
            print(current_status)
            return False

        # noinspection PyBroadException
        try:
            cls._log("Claim lock file", cls._LOCK_FILE_PATH)
            p.touch()

            on_lock_claimed(p, files)
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
    def _run_generator(
        cls,
        lockfile: Path,
        paths: List[str],
    ):
        model = SweetNothings()
        with lockfile.open(mode="a") as status:
            try:
                cls._log("Processing possible video files: ", paths)
                for file_path in paths:
                    status.write(f"Processing file: {file_path}\n")
                    result = model.generate_subtitles(
                        path=file_path,
                    )
                    if result:
                        cls._log("Generated subtitles for ", file_path)
                        status.write(f"Subtitles generated: {file_path}\n")
                    else:
                        cls._log("Failed to generate subtitles for ", file_path)
                        status.write(f"Subtitles failed: {file_path}\n")
                    status.write("\n")
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
