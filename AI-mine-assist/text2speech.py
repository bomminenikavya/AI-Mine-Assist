import os

from deepgram import DeepgramClient, SpeakOptions

filename = "output.wav"

os.environ['DG_API_KEY'] = "87e67f5c0aefd47ed9ecc6153875bee19f6eb7d9"


def text2speech(text):
    try:
        SPEAK_OPTIONS = {"text": text}
        deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        return filename

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    text2speech("This is a test")