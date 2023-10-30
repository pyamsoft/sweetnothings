#!/usr/bin/env python3
import gc
import os
from traceback import print_exc
from typing import Any

import stable_whisper
from faster_whisper import WhisperModel


class AiModel:
    def __init__(self):
        # Environment
        self._task = os.getenv(
            "TRANSCRIBE_OR_TRANSLATE",
            # We prefer this option, but accept the other for backwards compat
            os.getenv("TASK_TYPE", "translate"),
        )
        self._location = os.getenv("MODEL_PATH", ".")
        self._device = os.getenv(
            "TRANSCRIBE_DEVICE",
            # We prefer this option, but accept the other for backwards compat
            os.getenv("DEVICE", "cpu"),
        )
        self._whisper_model = os.getenv("WHISPER_MODEL", "medium")
        self._namesublang = os.getenv("NAMESUBLANG", "aa")

        self._model = None

    @classmethod
    def _log(cls, *args: Any):
        print("[AiModel]: ", *args)

    def _ensure_load_model(self) -> bool:
        if self._model:
            self._log("Whisper model is already loaded")
            return True

        # noinspection PyBroadException
        try:
            self._log("Load new whisper model")
            ai: WhisperModel = stable_whisper.load_faster_whisper(
                model_size_or_path=self._whisper_model,
                download_root=self._location,
                device=self._device,
            )
            self._model = ai
            return True
        except Exception as _:
            print_exc()
            return False

    def _get_transcribed_file_extension(self) -> str:
        return f".AI-Generated.{self._namesublang}.srt"

    @classmethod
    def _get_file_name_remove_extension(cls, path: str):
        return os.path.splitext(path)[0]

    def destroy(self):
        # noinspection PyBroadException
        try:
            del self._model
        except Exception as _:
            pass

        self._model = None

        # Run garbage collector
        gc.collect()

    def transcribe(self, path: str) -> bool:
        # Make sure we don't already have a generated file
        new_path = (
            self._get_file_name_remove_extension(path)
            + self._get_transcribed_file_extension()
        )
        if os.path.exists(new_path):
            self._log(f"{path} already has generated subtitle. Skip.")
            return False

        # Make sure we have the model
        if not self._ensure_load_model():
            self._log("Failed to load whisper model", self._whisper_model)
            return False

        self._log("Transcribe new subtitles to: ", new_path)

        # noinspection PyBroadException
        try:
            m: WhisperModel = self._model
            result = m.transcribe_stable(
                path,
                task=self._task,
            )
            if not result:
                self._log("Failed to transcribe_stable", path, self._task)
                return False

            # Output the new SRT file
            result.to_srt_vtt(
                new_path,
                word_level=False,
            )
            return True
        except Exception as _:
            print_exc()
            return False
