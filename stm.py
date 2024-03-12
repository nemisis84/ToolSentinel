from transitions import Machine
from facial_recognition import face_recognition_controller as frc
from speech_handler import main as speech_recogniser

class StateMachine:
    states = ["idle", 'waiting', 'FindPurpose', "AskForTool", 'AwaitAction']

    def __init__(self):
        self.machine = Machine(model=self, states=StateMachine.states, initial='idle')
        self.camera = frc.FaceRecognitionController()
        self.speech_recognizer = speech_recogniser
        self.setup_transitions()
        self.setup_state_functions()

        self.tools = {"hammer": True, "scissor": True} # True if available
        self.get_tool = True

        self.recognised_users = ["Simen"]

    def setup_transitions(self):
        self.machine.add_transition('initiate_stm', 'idle', 'waiting')
        self.machine.add_transition('recognise_person', 'waiting', 'FindPurpose', conditions=['is_authenticated'])
        self.machine.add_transition('purpose_decided', 'FindPurpose', 'AskForTool', conditions=['is_valid_input'])
        self.machine.add_transition('tool_decided', 'AskForTool', 'AwaitAction', conditions=['is_valid_input'])
        self.machine.add_transition('invalid_action', 'AskForTool', 'FindPurpose')
        self.machine.add_transition('action_taken', 'AwaitAction', 'waiting')
        self.machine.add_transition('timeout_or_quit', '*', 'waiting')

    def setup_state_functions(self):
        self.machine.on_exit_idle("start_camera")
        self.machine.on_enter_FindPurpose('ask_purpose_question')
        self.machine.on_enter_AskForTool("which_tool_question")
        self.machine.on_enter_AwaitAction("open_safe")
        self.machine.on_exit_AwaitAction("close_safe")

    def is_authenticated(self):
        print("Authenticating")
        return True

    def is_valid_input(self, input_message):
        input_message = input_message.lower()
        if self.state == "AskForTool":
            if input_message in self.tools.keys():
                print("Valid tool")
                if self.tools[input_message] and self.get_tool:
                    print("Tool available")
                    self.tools[input_message] = False
                    return True
                elif not self.tools[input_message] and not self.get_tool:
                    print("Free to return tool")
                    self.tools[input_message] = True
                    return True
                elif not self.tools[input_message] and self.get_tool:
                    print("Tool unavailable")
                    self.invalid_action()
                    return False
                elif self.tools[input_message] and not self.get_tool:
                    print("Tool already in box")
                    self.invalid_action()
                    return False
            else:
                print("Tool does not belong to the safe")
                return False
        if self.state == "FindPurpose":
            if input_message in ["grab", "return"]:
                self.get_tool = True if input_message == "grab" else False
                print("Valid purpose")
                return True
            else:
                print("Invalid purpose")
                return False

    def ask_purpose_question(self):
        print("You are authenticated. Do you want to return or grab a tool?")

    def open_safe(self, input_message):
        action = "grab" if self.get_tool else "return"
        print(f"Open safe and {action} the {input_message}")

    def close_safe(self):
        print("close safe")

    def which_tool_question(self, input_message):
        input_message = input_message.lower()
        print(f"You want to {input_message} a tool. Which tool do you want to {input_message}?")

    def start_camera(self):
        pass

def main():
    # Instantiate the StateMachine
    sm = StateMachine()
    print("State machine initialized. Current state: ", sm.state)
    sm.initiate_stm()

    # Simulate triggering transitions based on user input
    while True:
        print("Current state:", sm.state)

        if sm.state == 'waiting':
            sm.recognise_person()
        elif sm.state == 'FindPurpose':
            input_message = input("Grab or return tool?: ")
            sm.purpose_decided(input_message)
        elif sm.state == 'AskForTool':
            input_message = input("Scissor or Hammer: ")
            sm.tool_decided(input_message)
        elif sm.state == 'AwaitAction':
            sm.action_taken()

if __name__ == "__main__":
    main()
