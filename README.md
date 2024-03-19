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


## Run project

### Register user

To register a user run:

   ```bash
   python register.py
   ```
Insert your name when asked. A camera on your computer will pop up. Press enter to take photoes 4-6 should be sufficent. Press esc when you are done. The program will prosess and train the model with the photoes. 