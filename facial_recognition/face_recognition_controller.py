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
        # facial_req.recognise(self.face_queue)
        # while True:
        #     if not self.face_queue.empty():
        #         # Get the data from the queue
        #         persons = self.face_queue.get()
        #     else:
        #         persons = []
        #     return persons
        camera_thread = threading.Thread(target=facial_req.recognise, args =(self.face_queue,))
        camera_thread.daemon = True
        camera_thread.start()
        # facial_req.recognise()
        return "Name of client"
    
    def get_identification(self):
        global stop_flag

        while not stop_flag:
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
    # face_recognition_controller.register("Roy")
    stop_flag = False
    face_recognition_controller.start_camera()
    # face_recognition_controller.get_identification()
    identity_queue = queue.Queue()
    identity_thread = threading.Thread(target=face_recognition_controller.get_identification)
    identity_thread.daemon = True
    identity_thread.start()
    time.sleep(3)
    for i in range(50):
        print(face_recognition_controller.identity_queue_get())
        time.sleep(0.2)
    stop_flag = True
    print("program stopped")
