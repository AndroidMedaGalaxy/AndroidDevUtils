# AndroidDevUtils
This is a Python-based graphical user interface (GUI) application that simplifies and enhances the usage of ADB (Android Debug Bridge) commands for Android development and troubleshooting. The tool allows users to interact with their Android devices using a variety of functions through a user-friendly interface.

## Features

### 1. **ADB Device Manipulation**
   - **Reboot Device**: Reboots the connected Android device.
   - **Clear App Data**: Clears the app data for a specific package.
   - **Uninstall APK**: Uninstalls a specific app from the connected device.

### 2. **ADB Input Commands**
   - **Send Text Input**: Sends custom text to the device via ADB shell input text.
   - **ADB Language Setting**: Opens the language settings of the connected Android device.

### 3. **APK Management**
   - **Install APK**: Install APK files on the connected Android device by selecting the file from your system.

### 4. **Logcat & Device Monitoring**
   - **View Logcat**: Displays real-time device logs.
   - **List Connected Devices**: Lists all the connected Android devices via ADB.
   - **Device Info**: Displays the RAM and CPU usage of the connected device.

### 5. **Screen Capture & Recording**
   - **Take Screenshot**: Captures a screenshot from the Android device and saves it to your computer.
   - **Record Screen**: Records the screen of the Android device and saves the video file to your computer.

### 6. **Custom ADB Commands**
   - **Run Custom Command**: Allows you to run any custom ADB command on the connected device.

### 7. **Interactive History**
   - **Command History**: Stores and allows you to reuse previously run commands with a simple click.

### 8. **Confirmation for Sensitive Actions**
   - **Confirmation Dialogs**: Adds confirmation dialogs before running sensitive actions like uninstalling APKs or clearing app data to avoid accidental executions.

## Requirements

- Python 3.6+ (Tested on Python 3.8 and 3.9)
- `ttkbootstrap` library for the UI styling
- `subprocess` for executing ADB commands
- `tkinter` (comes pre-installed with Python)
- `adb` (Android Debug Bridge) installed and added to your system's PATH

## Installation

1. Install Python 3.6 or higher from [python.org](https://www.python.org/downloads/).
2. Install the required Python libraries by running:
   ```bash
   pip install ttkbootstrap

  


