from src.video import Video
from src.video_playlist import Playlist
from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._videolist = self._video_library.get_all_videos()
        self._currentlyPlayId = ""
        self._currentlyPauseId = ""
        self.createdPlaylists = {}

    def show_results(self,results,term):
        """This method displays all of the videos that correspond to the relavent search term"""
        
        if len(results) != 0:
            print("Here are the results for "+term+":")
         #remember to start the count at 1 to display it
            count = 1
            for result in results:
                title = result.title
                id = result.video_id 
                tags = result.tags
                print(" "+f"{count}) {title} ({id}) [{' '.join(tags)}]")
                count = count+1
            
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            response = input()
            if not response.isnumeric() or int(response)-1>=len(results):
                return
            
            else:
                self.play_video(results[int(response)-1].video_id)
        
        else:
            print("No search results for " + term)


    def message_of_video_title(self,action,video_id):
        """This shows if a video title is playing, paused or has ceased playing"""
        
        print(action + " video:"+ f" {self._video_library._videos[video_id].title}")

    def check_flag(self,video_id):
        """This checks to see if a video in the video library is flagged"""
        if self._video_library.get_video(video_id).flag == True:
            return True
        
        else:
            return False
    
    def print_flagged_message(self,video_id,action):
        """This command prints the flag message of a video"""
        print ("Cannot " + action + ": Video is currently flagged"+ f" (reason: {self._video_library._videos[video_id].reason})")

    def flag_procedure(self,video_id,action):
        """This method calls a flag procedure that deals with flagged videos and their messages"""
        
        if self.check_flag(video_id):
                self.print_flagged_message(video_id,action)
                return True
        else:
            return False

    
    def number_of_videos(self):
        """This command prints how many videos are present in the library"""

        num_videos = len(self._videolist)
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """This command will list all available videos in the format: 
        “title (video_id) [tags]”. The videos should be shown in lexicographical order by title. 
        If there are no tags available, display empty brackets."""

        """Returns all videos."""

        print("Here's a list of all available videos:")

        """Get the attributes from the list of objects as they are not a dictionary"""
        for video in self._videolist: 
            title = video.title
            id = video.video_id 
            tags = video.tags
            flag = video.flag

            if flag == False:
                print(" "+f"{title} ({id}) [{' '.join(tags)}]")

            else:
                flag_reason = video.reason
                print(" "+f"{title} ({id}) [{' '.join(tags)}] - FLAGGED"+f" (reason: {flag_reason})")


    def play_video(self, video_id):
        """Plays the respective video.
        
        Args:
            video_id: The video_id to be played.
        """
        if video_id in self._video_library._videos:

            if self.flag_procedure(video_id,"play video"):
                return

            if self._currentlyPlayId != "":
               self.message_of_video_title("Stopping",self._currentlyPlayId)
            
            self.message_of_video_title("Playing",video_id)
            self._currentlyPlayId =  video_id
            self._currentlyPauseId = ""
        
        else:
            print("Cannot play video: Video does not exist")
        
    def stop_video(self):
        """Stops the current video."""

        if self._currentlyPlayId != "":
             self.message_of_video_title("Stopping",self._currentlyPlayId)
             self._currentlyPlayId = ""
             self._currentlyPauseId = ""
            
        else:
             print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        random_video_list = self._video_library.get_all_random_videos()
        
        if len(random_video_list) == 0:
            print("No videos available")
            return

        if self._currentlyPlayId != "":
            self.message_of_video_title("Stopping",self._currentlyPlayId)

        self._currentlyPlayId = (random.choice(random_video_list)).video_id
        self.message_of_video_title("Playing",self._currentlyPlayId)

    def pause_video(self):
        """Pauses the current video."""
        if self._currentlyPlayId != "" and self._currentlyPauseId == "":
            title = self._video_library._videos[self._currentlyPlayId].title
            print("Pausing video: "+ f"{title}")
            self._currentlyPauseId = self._video_library.get_video(self._currentlyPlayId).video_id
        
        elif self._currentlyPauseId != "":
             print("Video already paused: "+ f"{self._video_library.get_video(self._currentlyPauseId).title}")
        
        else:
            print("Cannot pause video: No video is currently playing")
        
    def continue_video(self):
        """Resumes playing the current video."""
        if self._currentlyPauseId != "":
            self._currentlyPauseId = ""
            self.message_of_video_title("Continuing",self._currentlyPlayId)
        
        elif self._currentlyPauseId == "" and self._currentlyPlayId != "":
            print("Cannot continue video: Video is not paused")

        elif self._currentlyPlayId == "":
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""

        if self._currentlyPlayId == "" :
            print("No video is currently playing")
            return
        
        title = self._video_library.get_video(self._currentlyPlayId).title
        id = self._video_library.get_video(self._currentlyPlayId).video_id
        tags = self._video_library.get_video(self._currentlyPlayId).tags
        
        if self._currentlyPlayId != "" and self._currentlyPauseId == "":
            print("Currently playing: "+f"{title} ({id}) [{' '.join(tags)}]")
        
        elif self._currentlyPauseId != "":
            print("Currently playing: "+f"{title} ({id}) [{' '.join(tags)}]" +" - PAUSED")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() not in self.createdPlaylists:
            self.createdPlaylists[playlist_name.lower()] = Playlist(playlist_name)

            print("Successfully created new playlist: "+ playlist_name)
        
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        if playlist_name.lower() in self.createdPlaylists:
            if video_id not in self._video_library._videos:
                 print("Cannot add video to " +playlist_name+": Video does not exist")
            
            else:
                error_message = "add video to "+playlist_name
                title = self._video_library._videos[video_id].title
                tags = self._video_library._videos[video_id].tags

                selectedPlaylist = self.createdPlaylists[playlist_name.lower()]
                
                if video_id not in selectedPlaylist.videos_in_queue:
                    
                    if self.flag_procedure(video_id,error_message):
                        return
                    
                    selectedPlaylist.addToQueue(title,video_id,tags)
                    print("Added video to " +playlist_name+": "+title)
                
                else:
                    if self.flag_procedure(video_id,error_message):
                        return
                    
                    print("Cannot add video to " + playlist_name+": Video already added")

        else:
            print("Cannot add video to " +playlist_name+": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        isFull = bool(self.createdPlaylists)
        
        if isFull:
            print("Showing all playlists:")

             # sort dictionary by `key` in the natural order
            self.createdPlaylists = {k: v for k, v in sorted(self.createdPlaylists.items(), key=lambda item: item[0])}

            for playlist in self.createdPlaylists:
                print(f" {self.createdPlaylists[playlist].playlist_title}")
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.createdPlaylists:
             print("Showing playlist: "+playlist_name)
             selectedPlaylist = self.createdPlaylists[playlist_name.lower()]
             selectedPlaylist.displayQueue()

        else:
            print("Cannot show playlist " +playlist_name+": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        
        if playlist_name.lower() in self.createdPlaylists:
            if video_id not in self._video_library._videos:
                 print("Cannot remove video from " +playlist_name+": Video does not exist")
            
            else:
                selectedPlaylist = self.createdPlaylists[playlist_name.lower()]
                
                if video_id in selectedPlaylist.videos_in_queue:
                    
                    title = self._video_library._videos[video_id].title
                    selectedPlaylist.remove(video_id)
                    print("Removed video from " +playlist_name+": "+title)
                
                else:
                    print("Cannot remove video from " + playlist_name+": Video is not in playlist")

        else:
            print("Cannot remove video from " +playlist_name+": Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.createdPlaylists:
              selectedPlaylist = self.createdPlaylists[playlist_name.lower()]
              selectedPlaylist.removeAll()
              print("Successfully removed all videos from "+playlist_name)

        else:
            print("Cannot clear playlist " +playlist_name+": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() in self.createdPlaylists:
            self.createdPlaylists.pop(playlist_name.lower())
            print("Deleted playlist: "+ playlist_name)
        
        else:
            print("Cannot delete playlist " + playlist_name +": Playlist does not exist")
       

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        results = []
        for video in self._videolist: 
            title = video.title
            if search_term.lower() in title.lower() and not video.flag:
                results.append(video)
        
        self.show_results(results,search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        
        results = []
        for video in self._videolist:
            tagsAsString = ' '.join(video.tags)
            if video_tag.lower() in tagsAsString.lower() and "#" in video_tag and not video.flag:
                results.append(video)
        
        self.show_results(results,video_tag)

    def flag_video_in_playlist(self,video_id,flag,reason):
        """Flag the respective video in the playlist"""
        
        for playlist in self.createdPlaylists:
            
            if video_id not in self.createdPlaylists[playlist].videos_in_queue:
                continue

            else:
                self.createdPlaylists[playlist].flag_certain_video(video_id,flag,reason)
    
    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        
        if video_id in self._video_library._videos:
            if  self._video_library._videos[video_id].flag == False:
                title = self._video_library._videos[video_id].title

                if video_id == self._currentlyPlayId:
                    self.stop_video()
                
                if flag_reason == "":
                    flag_reason = "Not supplied"
                    print("Successfully flagged video: " +title+ f" (reason: {flag_reason})")
                
                else:
                    print("Successfully flagged video: " +title+ f" (reason: {flag_reason})")

                self._video_library.remove_random_video(video_id)
                self._video_library.get_video(video_id).setFlag(True)
                self._video_library.get_video(video_id).setReason(flag_reason)
                self.flag_video_in_playlist(video_id,True,flag_reason)

                """Call function to loop through all playlists to locate if the video is in the playlist"""
            
            else:
                 print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")
         
    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if video_id in self._video_library._videos:
            if  self._video_library._videos[video_id].flag == True:
                title = self._video_library._videos[video_id].title

                print("Successfully removed flag from video: " +title)

                self._video_library.add_random_video(video_id)
                self._video_library.get_video(video_id).setFlag(False)
                self._video_library.get_video(video_id).setReason("")
                self.flag_video_in_playlist(video_id,False,"")

                """Call function to loop through all playlists to locate if the video is in the playlist"""
            
            else:
                    print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")
