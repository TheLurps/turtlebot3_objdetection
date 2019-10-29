import sys
import time
import subprocess
import timeit
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = "/home/lurps/.ros"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "modified" and event.src_path.find("obj_detection_frame") > -1:
            username = getpass.getuser()
            dir = "/home/" + username + "/catkin_ws/src/obj_detection"
            cmd = "md5sum " + event.src_path
            cmd_darknet = "cd " + dir + \
                "/darknet && ./darknet detect custom/yolov3-tiny-obj.cfg custom/OfficeHomeDataset_realworld_small/yolov3-tiny-obj_30000.weights " + event.src_path
            cmd_google = "python cloud_vision.py " + event.src_path
            cmd_bagofwords = "cd " + dir + \
                "/Minimal-Bag-of-Visual-Words-Image-Classifier && python classify.py -c custom_obj_codebook.file -m custom_obj_trainingdata.svm.model " + event.src_path
            cmd_ncs = "cd " + dir + \
                "/yoloNCS/py_examples && python yolo_example.py " + event.src_path
            cmd_tensor = "curl --user psawaffle:TurtleBot3 --form input_photo=@" + \
                event.src_path + "http://104.199.21.87/post"
            if(len(sys.argv) > 1):
                if sys.argv[1] == "darknet":
                    cmd = cmd_darknet
                elif sys.argv[1] == "google":
                    cmd = cmd_google
                elif sys.argv[1] == "bagofwords":
                    cmd = cmd_bagofwords
                elif sys.argv[1] == "ncs":
                    cmd = cmd_ncs
                elif sys.argv[1] == "tensor"
                    cmd = cmd_tensor

            start = timeit.default_timer()
            subprocess.call(cmd, shell=True)
            stop = timeit.default_timer()
            print(cmd + ": " + str((stop - start) * 1000) + " ms")


if __name__ == "__main__":
    w = Watcher()
    w.run()
