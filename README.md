# Project Name: OpenCV2026

## Project Info
- Date: October 2025
- Created by: Lavrenty "Larry" Orlov

## Overview
- Description: This program opens a new window that displays visual information captured by the built-in camera on the user's device or a connected camera. Then, once the user selects an object shown in the camera's frame, the program tracks the frame-by-frame position and rotation of that object until the user stops the program.
- Context: This is the first version of an object detection system I created for a robotic submarine developed at Washington State University's (WSU's) RoboSub Club, which competes at an annual international competition called RoboSub.

## Features
- Provides valuable visual feedback to the user: A rectangle remains positioned around the tracked object; text at the top of the window indicates whether the program is able to find the object in the current frame, and also shows the currently tracked rotation.
- Responds to user input: determines which object to track based on the region of the camera's frame selected by the user; waits for the user to press "Enter" before tracking the object, then waits for the user to press "Q" to end the program once object tracking started.
- Easy to run in Visual Studio.

## Tech Stack
- Language: Python
- IDE: Visual Studio Code

## How to Run
1. Clone the repository on your device's command-line interface:
- ```git clone https://github.com/LavrentyOrlov/OpenCV2026.git```
2. Open the project in Visual Studio.
3. Build the solution.
4. Run the program.
