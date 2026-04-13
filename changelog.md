# Changelog

All notable changes to this project are documented here.

## [v1.0.0] - Initial Version
### Added
- Basic real-time webcam posture detection using OpenCV.
- MediaPipe Pose landmark extraction.
- Angle-based slouch detection using ear, shoulder, and hip points.
- On-screen posture label and landmark visualization.

## [v1.1.0] - Sound Alerts
### Added
- Audio alert when slouching is detected.
- Cooldown logic to avoid constant sound repetition.
- Non-blocking sound playback for smoother user experience.

### Improved
- Better usability by giving instant feedback beyond visual labels.

## [v1.2.0] - Head Tilt Fix
### Changed
- Replaced single-side landmark logic with center-based tracking.
- Used midpoint calculations for ears, shoulders, and hips.

### Fixed
- Reduced false slouch detection when the head tilted left or right.

## [v1.3.0] - Front Slouch Detection Upgrade
### Changed
- Reworked posture detection logic from simple angle tracking to posture ratio analysis.
- Calculated neck height relative to shoulder width for more reliable front-facing webcam detection.

### Fixed
- Improved slouch detection when leaning forward.
- Reduced incorrect behavior caused by front camera perspective limitations.

## [v1.4.0] - UI Version
### Added
- Desktop GUI using Tkinter/CustomTkinter.
- Start and Stop camera controls.
- Live posture status in the interface.
- More polished and user-friendly layout.

### Improved
- Rounded buttons and better visual design.
- Better color hierarchy and cleaner presentation.

## [v1.5.0] - Visual Polish
### Changed
- Refined UI colors for a more subtle modern appearance.
- Improved overall layout for presentation and usability.

### Improved
- Better project readiness for GitHub portfolio and LinkedIn showcase.