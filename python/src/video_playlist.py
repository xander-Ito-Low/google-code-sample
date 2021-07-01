"""A video playlist class."""

from src.video import Video


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self,playlist_title:str):
        """Playlist constructor."""
        self.playlist_title = playlist_title
        self.videos_in_queue = {}

    def addToQueue(self,title,video_id,tags):
        """Add a video to the playlist queue."""
        self.videos_in_queue[video_id] = Video(title,video_id,tags)
    
    def displayQueue(self):
        """Display all of the videos in a playlist."""

        isFull = bool(self.videos_in_queue)
        
        if isFull:
            for video in self.videos_in_queue:
                title = self.videos_in_queue[video].title
                id = self.videos_in_queue[video].video_id
                tags = self.videos_in_queue[video].tags

                print(" "+f"{title} ({id}) [{' '.join(tags)}]")

        else:
            print(" No videos here yet")
    
    def remove(self,video_id):
        """Remove a specific video from the playlist."""
        
        self.videos_in_queue.pop(video_id)
    
    def removeAll(self):
        """Delete all of the videos in a playlist."""
        
        self.videos_in_queue.clear()


        