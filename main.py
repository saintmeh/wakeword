import pyaudio
import speech_recognition as sr

class MicrophoneSwitcher:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphones = sr.Microphone.list_microphone_names()
        self.current_mic_index = 0  # Default to the first microphone

    def switch_microphone(self):
        self.current_mic_index = (self.current_mic_index + 1) % len(self.microphones)
        print(f"Switched to: {self.microphones[self.current_mic_index]}")

    def listen_for_activation(self, activation_word="switch"):
        print(f"Listening for activation word: '{activation_word}'")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Microphone ready.")
            while True:
                try:
                    print("Waiting for activation word...")
                    audio = self.recognizer.listen(source)
                    transcript = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {transcript}")
                    if activation_word.lower() in transcript.lower():
                        self.switch_microphone()
                        # Switch to the new microphone and listen
                        self.listen_with_current_mic()
                except sr.UnknownValueError:
                    print("Could not understand audio. Try again.")
                except sr.RequestError as e:
                    print(f"Error with speech recognition service: {e}")

    def listen_with_current_mic(self):
        with sr.Microphone(device_index=self.current_mic_index) as source:
            print(f"Listening on {self.microphones[self.current_mic_index]}")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source)
                transcript = self.recognizer.recognize_google(audio)
                print(f"You said: {transcript}")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")

if __name__ == "__main__":
    switcher = MicrophoneSwitcher()
    if len(switcher.microphones) < 2:
        print("Need at least two microphones for switching.")
    else:
        print("Available microphones:")
        for i, mic_name in enumerate(switcher.microphones):
            print(f"{i}: {mic_name}")
        switcher.listen_for_activation("switch")
