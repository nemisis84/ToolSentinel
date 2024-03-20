# ToolSentinel
Project for ambient Intelligence

## Setup
Setup of project using `setup.py`, manage dependencies with `environment.yaml`, and build the project using Conda.

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone git@github.com:nemisis84/ToolSentinel.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ToolSentinel
   ```

3. Create a Conda environment (optional but recommended):
  
   ```bash
   conda env create -f environment.yaml
   ```

   This will create a new Conda environment with the required dependencies specified in `environment.yaml`.

4. Activate the Conda environment:

   ```bash
   conda activate ToolSentinelEnv
   ```

5. Install the project:

   ```bash
   pip install .
   ```

   This will install the project along with its dependencies.

### Arduino Setup

1. Firstly, you need to download Arduino IDE from the official website, according to your computer operating system. Accept all the packages instalations and run the software.

2. Grab the Arduino Uno board and servo, follow the steps:
   ```
   - With the use of cables, connect the red entry of the servo to the 5V entry of the board.

   - Connect the black cable of the motor to the ground entry of the board.

   - Connect the white cable of the motor to the pin number 9 of the board.
   
   - Connect the board to the computer, to the USB entry.
   ```
3. Go to the Arduino IDE and check the board that is currently selected, if there is none, then select the arduino uno and check the port that it is connected to. Ex: COM3. This value will be used in step 5 so keep it in mind.

4. When the lights turn on the board, copy the code on the file arduino.c and paste it into the Arduino IDE. After that, compile and send it to the board.

5. Finally, check the stm.py file and change the SERIALPORT variable to match the port that you checked on step 3. With this, arduino is set up and ready to go.


## Run project

### Register user

To register a user run:

   ```bash
   python register.py
   ```
Insert your name when asked. A camera on your computer will pop up. Press enter to take photoes 4-6 should be sufficent. Press esc when you are done. The program will prosess and train the model with the photoes. 