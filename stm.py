from transitions import Machine
from facial_recognition import face_recognition_controller as frc
from speech_handler import main as speech_recogniser
import queue
import threading
import time
import serial

# CHECK THIS WHEN SETTING UP THE BOARD
SERIALPORT = 'COM3'
BAUDRATE = 9600

class StateMachine:
    states = ["idle", 'waiting', 'FindPurpose', "AskForTool", 'AwaitAction']

    def __init__(self):
        self.machine = Machine(model=self, states=StateMachine.states, initial='idle')
        self.camera = frc.FaceRecognitionController()
        self.speech_recognizer = speech_recogniser.recognize_voice # Wait for voice
        self.speaker = speech_recogniser.speak # Input text
        self.setup_transitions()
        self.setup_state_functions()

        self.ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=1)

        self.tools = {"hammer": True, "scissor": True} # True if available
        self.get_tool = True
        self.tool_in_focus = None

        self.recognised_users = ["Simen"]

    def setup_transitions(self):
        self.machine.add_transition('initiate_stm', 'idle', 'waiting')
        self.machine.add_transition('recognise_person', 'waiting', 'FindPurpose', conditions=['is_authenticated'])
        self.machine.add_transition('purpose_decided', 'FindPurpose', 'AskForTool', conditions=['is_valid_input'])
        self.machine.add_transition('tool_decided', 'AskForTool', 'AwaitAction', conditions=['is_valid_input'])
        self.machine.add_transition('invalid_action', 'AskForTool', 'FindPurpose')
        self.machine.add_transition('action_taken', 'AwaitAction', 'waiting')
        self.machine.add_transition('quit', '*', 'waiting')

    def setup_state_functions(self):
        self.machine.on_exit_idle("start_camera")
        self.machine.on_enter_FindPurpose('ask_purpose_question')
        self.machine.on_enter_AskForTool("which_tool_question")
        self.machine.on_enter_AwaitAction("open_safe")
        self.machine.on_exit_AwaitAction("close_safe")

    def is_authenticated(self):
        print("Authenticating ...")
        time.sleep(1)
        users = self.camera.identity_queue_get()

        
        if not users: 
            return False
        
        # Only allow one user in the camera at the time
        if len(users)>1:
            return False

        if users[0] in self.recognised_users:
            return True
        
        return False

    def is_valid_input(self, input_message):
        input_message = input_message.lower()
        if self.state == "AskForTool":

            if input_message in ["one", "two"]:
                input_message = "scissor" if input_message == "one" else "hammer"

                if self.tools[input_message] and self.get_tool:
                    # print("Tool available")
                    self.speaker(f"{input_message} available")
                    self.tools[input_message] = False
                    self.tool_in_focus = input_message
                    return True
                elif not self.tools[input_message] and not self.get_tool:
                    # print("Free to return tool")
                    self.speaker(f"Free to return {input_message}")
                    self.tools[input_message] = True
                    self.tool_in_focus = input_message
                    return True
                elif not self.tools[input_message] and self.get_tool:
                    # print(f"{input_message} unavailable")
                    self.speaker(f"{input_message} unavailable")
                    self.invalid_action()
                    return False
                elif self.tools[input_message] and not self.get_tool:
                    # print("Tool already in box")
                    self.speaker(f"{input_message} already in box")
                    self.invalid_action()
                    return False
            else:
                # print("Tool does not belong to the safe")
                self.speaker("Tool does not belong to the safe")
                return False
        if self.state == "FindPurpose":
            if input_message in ["one", "two"]:
                if input_message == "one" and not any(self.tools.values()):
                    self.speaker("Safe empty, all tools are used")
                    self.speaker("Do you want to return a tool or quit?")
                    return False
                elif input_message == "two" and all(value for value in self.tools.values()):
                    self.speaker("Safe full, no tool to return")
                    self.speaker("Do you want to get a tool or quit?")
                    return False
                self.get_tool = True if input_message == "one" else False
                # print("Valid purpose")
                self.speaker("Valid purpose")
                return True
            else:
                # print("Invalid purpose")
                self.speaker("Invalid purpose")
                return False

    def ask_purpose_question(self):
        # print("You are authenticated. Say one to get a tool, two for returning a tool")
        self.speaker("You are authenticated. Say one to get a tool, two for returning a tool")

    def open_safe(self, input_message):
        action = "get" if self.get_tool else "return"
        # print(f"Open safe and {action} the {input_message}")

        angle = -90
        self.ser.write(str(angle).encode())
        
        self.speaker(f"Open safe and {action} the {input_message}")

    def close_safe(self):
        # print("Close safe")
        self.speaker("Safe closing")

        angle = 90
        self.ser.write(str(angle).encode())
        
        time.sleep(5)

    def which_tool_question(self, input_message):
        input_message = input_message.lower()
        input_message = "grab" if input_message == "one" else "return"
        print(f"You want to {input_message} a tool. Which tool do you want to {input_message}?:")
        items = list(self.tools.keys())
        self.speaker(f"You want to {input_message} a tool. Which tool do you want to {input_message}?\none: {items[0]}, two: {items[1]}")

    def start_camera(self):
        self.camera.start_camera()

        # Start tracking whos in the camera

        identity_thread = threading.Thread(target=self.camera.get_identification)
        identity_thread.start()


def main():
    # Instantiate the StateMachine
    sm = StateMachine()
    print("State machine initialized. Current state: ", sm.state)
    sm.initiate_stm()

    # Simulate triggering transitions based on user input
    try:
        while True:
            print("Current state:", sm.state)

            if sm.state == 'waiting':
                sm.recognise_person()
            elif sm.state == 'FindPurpose':
                # input_message = input("get or return tool?: ")
                input_message = sm.speech_recognizer()
                if input_message == "quit":
                    sm.quit()
                else:
                    sm.purpose_decided(input_message)
            elif sm.state == 'AskForTool':
                # input_message = input("Scissor or Hammer?: ")
                input_message = sm.speech_recognizer()
                if input_message == "quit":
                    sm.quit()
                else:
                    sm.tool_decided(input_message)
            elif sm.state == 'AwaitAction':
                action = "gotten" if sm.get_tool else "returned"
                # input_message = input(f"Have you {action} the {sm.tool_in_focus}?: ")
                sm.speaker(f"Have you {action} the {sm.tool_in_focus}?: ")
                input_message = sm.speech_recognizer()
                if input_message.lower() == "yes":
                    sm.action_taken()
    except KeyboardInterrupt:
        sm.camera.stop_camera()
        print("All processes stopped")

if __name__ == "__main__":
    main()
