#!/usr/bin/env python3
from dataclasses import dataclass
from traceback import print_exc
from typing import Callable, List, Dict

import av


@dataclass
class VideoStream:
    type: str
    metadata: Dict[str, str]


@dataclass
class VideoContainer:
    streams: List[VideoStream]


class VideoFile:
    @classmethod
    def _check_video_streams(cls, path: str, on_stream: Callable[[VideoStream], bool]):
        av.logging.set_level(av.logging.PANIC)

        try:
            container = av.open(path)
            for stream in container.streams:
                if on_stream(stream):
                    return True
        except av.AVError:
            print_exc()

        return False

    @classmethod
    def is_video_file(cls, path: str) -> bool:
        """
        Check if the path provided is to a video file by attempting to open it and
        check for Video streams
        """

        def _on_stream(stream: VideoStream) -> bool:
            return stream.type == "video"

        return cls._check_video_streams(path, _on_stream)

    @classmethod
    def has_internal_subtitles(cls, path: str, target_language: str) -> bool:
        def _on_stream(stream: VideoStream) -> bool:
            if stream.type != "subtitle":
                return False

            lang = stream.metadata.get("language", None)
            return lang and lang == target_language

        return cls._check_video_streams(path, _on_stream)
