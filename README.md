# Automated Audio Censoring
This project automatically removes censors profanity inside of an audio file using OpenAI Whisper model, HuggingFace Transformers, and FFMPEG.

### How does it work?
It first transcribes the audio data using OpenAI Whisper Model and HuggingFace Transformers. The output of the model provides timestamps on the word level. After recieving the timestamped data, we match any words to a large library of profanity words. We then pipeline those timestamps to FFMPEG where we silence the audio and finally export the new file.

To run the program, navigate to the src folder and execute main.py:

```
cd src
python main.py  # or python3 main.py on some systems
```

Follow any on-screen instructions to interact with the program.

![Example Image](example.png)

## Authors
tuvshno

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
