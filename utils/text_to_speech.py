from gtts import gTTS
from deep_translator import GoogleTranslator
import os

def text_to_speech(text, filename="tts_output.mp3"):
    """
    Converts the given English text into Hindi speech and saves it as an MP3 file.
    
    :param text: English text to be converted into Hindi speech.
    :param filename: File name for the MP3 file (default: "tts_output.mp3").
    :return: Path to the saved MP3 file.
    """
    if not text.strip():
        return None  # Return None for empty input

    try:
        # Create a directory to store audio files
        save_dir = "static"
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
        output_audio_path = os.path.join(save_dir, filename)  # Save inside 'static' folder

        # Translate text to Hindi
        translated_text = GoogleTranslator(source="auto", target="hi").translate(text)

        # Convert translated text to speech
        tts = gTTS(text=translated_text, lang="hi")
        tts.save(output_audio_path)

        return output_audio_path
    except Exception as e:
        print(f"❌ Error in text-to-speech conversion: {str(e)}")
        return None

# 🔥 Test Case
if __name__ == "__main__":
    test_text = "Tesla is leading the electric vehicle industry with innovation."
    result = text_to_speech(test_text)
    if result:
        print(f"✅ Audio saved at: {result}")
    else:
        print("❌ Failed to generate audio.")
