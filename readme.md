# AI Posture Monitor

A real-time posture monitoring desktop application built with Python, OpenCV, MediaPipe, and CustomTkinter. The app analyzes webcam input, detects slouching posture, and provides live visual feedback with sound alerts through a clean modern UI.

## Features

- Real-time webcam-based posture monitoring.
- Pose estimation using MediaPipe landmarks.
- Slouch detection based on posture ratio calculations.
- Audio alert when slouching is detected.
- Modern desktop UI with rounded buttons and subtle color palette.
- Live posture status display with ratio feedback.
- Improved detection logic after multiple iterations and testing.

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Pillow
- CustomTkinter
- Winsound

## How It Works

The application captures frames from the webcam and extracts body landmarks using MediaPipe Pose. It calculates ear and shoulder reference points, then derives a posture ratio to determine whether the user is sitting upright or slouching.

If the posture falls below the chosen threshold, the app updates the UI status and plays a sound alert. This creates a lightweight real-time posture assistant that can be used during study or work sessions.

## Key Improvements

This project was improved through testing and debugging:

- Initial posture logic was too sensitive to head tilt.
- Center-based tracking was introduced to reduce side tilt issues.
- Front-slouch detection was improved using a posture ratio approach.
- Sound alerts were added without freezing the video feed.
- The interface was upgraded from a basic window to a cleaner modern UI.

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-posture-monitor.git
cd ai-posture-monitor
```

Install dependencies:

```bash
pip install opencv-python mediapipe==0.10.21 numpy pillow customtkinter
```

Run the application:

```bash
python posture_detector.py
```

## Usage

- Launch the app.
- Click **Start Camera**.
- Sit naturally in front of the webcam.
- If slouching is detected, the app will show a warning and play a sound.
- Click **Stop Camera** to pause the feed.

## Project Motivation

I built this project to create something practical with computer vision and AI that also solves a real daily problem: poor sitting posture during long work or study sessions. The goal was not just to detect pose, but to iteratively improve accuracy and make the final application feel like a real product.

## Future Improvements

- User-specific calibration mode.
- Posture history tracking and analytics.
- Session timer and productivity dashboard.
- Export posture logs to CSV.
- Packaging as a standalone desktop app.

## Demo

Add screenshots, GIFs, or a short demo video here.

## Author
Manan Patel