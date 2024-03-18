# Automated Audio Censoring
This project is audio cleansing utility designed remove profanity content in audio. Utilizing the capabilities of OpenAI's Whisper model, this tool  analyzes audio files to identify and flag profanity. Upon detection, the program utilizes the FFmpeg framework to discretely mute or excise the undesirable segments, ensuring your content remains appropriate for all audiences.

Crafted with podcasters, video creators, and content producers in mind, this application streamlines the process of maintaining high-quality, audience-friendly audio. It's the perfect blend of AI-driven precision and user-friendly functionality, offering a seamless solution for upholding the integrity of your audio projects.

## Getting Started

These instructions will guide you through setting up and running the project on your local machine.

## Prerequisites

Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/). This project was developed with Python 3.x, so it is recommended to use Python 3.x.

### FFmpeg Installation

This tool relies on FFmpeg, a comprehensive multimedia framework that enables audio processing. It's crucial to have FFmpeg installed and correctly set up on your system to utilize this project's audio censoring features.

### Checking FFmpeg Installation

To verify if FFmpeg is installed, open a terminal or command prompt and execute:

```bash
ffmpeg -version
```

### Installing FFmpeg

Windows:
1. Download the latest FFmpeg build from the FFmpeg Official Website.
2. Extract the downloaded ZIP file to a location on your system, e.g., C:\FFmpeg.
3. Add the FFmpeg bin folder (e.g., C:\FFmpeg\bin) to your system's PATH environment variable:
    - Search for "Environment Variables" in your Start menu and select "Edit the system environment variables."
    - In the System Properties window, click on "Environment Variables."
    - Under "System variables," find the "Path" variable, select it, and click "Edit."
    - Click "New" and add the path to your FFmpeg bin folder.
    - Click "OK" on all open dialogs to apply the changes.

MacOS:
You can install FFmpeg using Homebrew, a package manager for macOS:
```
brew install ffmpeg
```

Linux:
Most Linux distributions include FFmpeg by default. If not, you can install it using your package manager. For example, on Ubuntu:
```
sudo apt update
sudo apt install ffmpeg
```

### Verifying the Installation
After installation, reopen your terminal or command prompt and run ffmpeg -version again to confirm that FFmpeg is correctly installed and accessible from your command line.

### Running the Project
With FFmpeg installed, you're all set to run the project.

## Setting Up a Virtual Environment

To avoid conflicts with other projects or system-wide Python packages, it's recommended to use a virtual environment. Here's how to set it up:

1. **Create the Virtual Environment**:

    For Windows:
    ```cmd
    python -m venv myenv
    ```
    
    For Unix or MacOS:
    ```bash
    python3 -m venv myenv
    ```

2. **Activate the Virtual Environment**:

    For Windows:
    ```cmd
    myenv\Scripts\activate
    ```
    
    For Unix or MacOS:
    ```bash
    source myenv/bin/activate
    ```

## Installing Dependencies

With the virtual environment activated, install the project dependencies by running:

```bash
pip install -r requirements.txt
```

This command will install all the packages listed in the requirements.txt file, ensuring you have all the necessary dependencies.

## Running the Program

To run the program, navigate to the src folder and execute main.py:

```
cd src
python main.py  # or python3 main.py on some systems
```

Follow any on-screen instructions to interact with the program.

## Authors
tuvshno

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
>>>>>>> Stashed changes
