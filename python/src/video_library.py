"""A video library class."""

import copy
from .video import Video
from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

            # sort list by `name` in the natural order
            self._videos = {k: v for k, v in sorted(self._videos.items(), key=lambda item: item[0])}

            #A deep copy of all of the avaliable videos
            self.randomvideos = copy.deepcopy(self._videos)

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_all_random_videos(self):
        """Returns all playable videos."""
        return list(self.randomvideos.values())
    
    def remove_random_video(self,video_id):
         "removes a random video from the dictionary"
         self.randomvideos.pop(video_id)
    
    def add_random_video(self,video_id):
         "add a random video from the dictionary"
         self.randomvideos[video_id] = self._videos[video_id]

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)
