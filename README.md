# Environment Setup

1. Install Anaconda or Miniconda.
2. Create a conda environment from the environment.yml:
    - Use the command: `conda env create -f enviroment.yml`
    - This should create an environment named `muc`. 
3. Activate the conda environment:
    - Windows command: `activate muc` 
    - MacOS / Linux command: `conda activate muc`
4. In VS Code, follow these steps:
    - cmd + p + shift and click on "Python: Select Interpreter"
    - Select the muc environment

# Run Code

1. In the plot-live-data.py file, change serial_port to the correct plot ("COM3" for windows and "\dev\tty..." on Mac)
1. Copy .cpp file into Arduino IDE and click "upload"
2. Once you see "Done Uploading", close the serial monitor then run Python script in VSCode
