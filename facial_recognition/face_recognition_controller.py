import headshots
import facial_req
import train_model
import os
import threading
import time
import queue

class FaceRecognitionController:

    def __init__(self):
        self.face_queue = queue.Queue()
        self.identity_queue = queue.Queue()
        self.stop_flag = stop_flag = threading.Event()  # Create stop_flag as an Event
    def register(self, name):
        
        # Take pictures
        image_path = "dataset/"+ name +"/"
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        headshots.take_headshots(name, image_path)

        # Train
        image_data_path = "dataset"
        train_model.train(image_data_path)
        
    def start_camera(self):
        self.camera_thread = threading.Thread(target=facial_req.recognise, args=(self.face_queue, self.stop_flag))
        self.camera_thread.start()

    def stop_camera(self):

        self.stop_flag.set()  # Set the stop_flag to True
        if self.camera_thread:
            self.camera_thread.join()  # Wait for the thread to finish
        self.stop_flag = None  # Reset stop_flag to None after stopping the camera thread

    
    def get_identification(self):

        while not self.stop_flag.is_set():
            if not self.face_queue.empty():
                # Get the data from the queue
                persons = self.face_queue.get()
            # else:
            #     persons = ["None"]
                self.identity_queue.put(persons)

    def identity_queue_get(self):
        if not self.identity_queue.empty():
            return self.identity_queue.get()
        else:
            return None


if __name__ == "__main__":
    face_recognition_controller = FaceRecognitionController()
    # face_recognition_controller.register("Simen")
    # time.sleep(5)
    face_recognition_controller.start_camera()

    identity_queue = queue.Queue()
    identity_thread = threading.Thread(target=face_recognition_controller.get_identification)
    identity_thread.start()
    time.sleep(3)
    print("Here")
    for i in range(10):
        print(face_recognition_controller.identity_queue_get())
        time.sleep(1)

    print("Stop")
    face_recognition_controller.stop_camera()  # Stop the camera thread

    print("program stopped")
