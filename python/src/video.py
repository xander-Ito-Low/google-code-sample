"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        self._video_flag = False
        self._video_reason = ""

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        #add a boolean to determine if the video is being played (remember to set to false )

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flag(self) -> bool:
        """Returns the flag of a video."""
        return self._video_flag

    @property
    def reason(self) -> str:
        """Returns the reason that a video was flagged."""
        return self._video_reason

    def setFlag(self,flag):
        "This sets the flag for a video"
        self._video_flag = flag

    def setReason(self,reason):
        "This sets the reason as to why a video was flagged"
        self._video_reason = reason



    

        
