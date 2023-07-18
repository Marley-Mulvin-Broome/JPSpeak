from ttsprovider import TTSProvider
from gtts import gTTS


class GoogleTTS(TTSProvider):
    def speak(self, text):
        response = gTTS(text, lang="ja")

        return response.stream()

    def speakers_get(self):
        return ["Japanese"]

    def __repr__(self):
        return "Google"
