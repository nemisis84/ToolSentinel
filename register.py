from facial_recognition import face_recognition_controller as frc

controller = frc.FaceRecognitionController()

import sys

def register(name):
    controller = frc.FaceRecognitionController()
    path = "facial_recognition/"
    controller.register(name, path)

def main():
    while True:
        name = input("Please provide your name: ")
        if name:
            register(name)
            break
        else:
            print("No name provided. Please try again.")

if __name__ == "__main__":
    main()
