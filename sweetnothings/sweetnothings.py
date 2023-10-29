#!/usr/bin/env python3
import os
import time
from typing import Any

from sweetnothings.ai import AiModel
from sweetnothings.video import VideoFile


class SweetNothings:
    def __init__(self):
        self._ai = AiModel()

    @classmethod
    def _log(cls, *args: Any):
        print("[SweetNothings]: ", *args)

    def _process_subtitle(self, path: str) -> bool:
        """
        Generate subtitles using AI Whisper Model
        :param path:
        :return:
        """
        self._log(f"Processing file {os.path.basename(path)}")
        start_time = time.time()

        result = self._ai.transcribe(path)

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)

        minute_suffix = "" if minutes == 1 else "s"
        second_suffix = "" if seconds == 1 else "s"
        succeeded = "SUCCESS" if result else "FAILURE"
        self._log(
            f"Processing {os.path.basename(path)} completed. "
            + f"Took {minutes} minute{minute_suffix} "
            + f"and {seconds} second{second_suffix}. "
            + f"RESULT: {succeeded}"
        )
        return result

    def destroy(self):
        self._ai.destroy()

    def generate_subtitles(self, path: str) -> bool:
        """
        Accepts a file path. Generate subtitles if file is a video file
        :param path:
        :return:
        """
        if not VideoFile.is_video_file(path):
            self._log(f"File is not video file: {path}")
            return False

        if VideoFile.has_internal_subtitles(
            path,
            target_language="eng",
        ):
            self._log(f"File already has ENG subtitles: {path}")
            return False

        return self._process_subtitle(path)
