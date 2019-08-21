#A PYTHON THAT MONITORS A SPECIFIED DIRECTORY
#AND ALERTS WHEN AN EVENT HAPPENED IN YOUR FILES IN THE DIRECTORY
#ALSO ARRANGES YOUR FILES ACCORDING TO THEIR FILE TYPE BY PUTTING THEM IN THEIR RESPECTIVE FOLDERS UPON CREATION

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os

# FOLDER NAMES IN YOUR DIRECTORY

root = "./new"
audio = "/Audio/"
img = '/Images/'
video = '/Videos/'
doc = '/Document/'
dev = '/Dev/'

# POSSIBLE FILE TYPES

audio_types = ['mp3', 'aau', 'm4a', 'wav', 'flac']
picture_types = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
video_types = ['mp4', '3gp', 'wmv', 'flv', 'avi']
document_types = ['pdf', 'docx', 'xlsx', 'txt']
dev_types = ['html', 'java', 'css', 'js']

# FUNCTION TO GET FOLDER TO USE ACCORDING TO FILE TYPE


def get_respective_folder(file):
    file_type = file.split('.')[1]
    if(file_type in audio_types):
        return audio
    if(file_type in picture_types):
        return img
    if(file_type in video_types):
        return video
    if(file_type in document_types):
        return doc
    if(file_type in dev_types):
        return dev

# DOES THE MOVING TO RESPECTIVE FOLDER JOB


def arrange(event):
    file_name = str(event.src_path)
    os.rename(event.src_path, root + '/' +
              get_respective_folder(file_name[2:]) + file_name[2:])


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)

# EVENT LISTENERS


def on_created(event):
    file_name = str(event.src_path)
    print(f"hey, {event.src_path} has been created!")
    arrange(event)


def on_deleted(event):
    print(f"what the!!! Someone deleted {event.src_path}!")


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = "."
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
