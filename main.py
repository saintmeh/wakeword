import argparse
import pyaudio
import speech_recognition as sr

class MicrophoneSwitcher:
    def __init__(self, mic_filter=None):
        self.recognizer = sr.Recognizer()
        self.microphones = self.get_filtered_microphones(mic_filter)
        if not self.microphones:
            print("No microphones match the filter. Exiting.")
            exit(1)
        self.current_mic_index = 0  # Default to the first microphone

    def get_filtered_microphones(self, mic_filter):
        all_microphones = sr.Microphone.list_microphone_names()
        if mic_filter is not None:
            try:
                # Check if mic_filter contains indices
                indices = [int(idx) for idx in mic_filter.split(",") if idx.isdigit()]
                selected_mics = [all_microphones[i] for i in indices if 0 <= i < len(all_microphones)]
                if selected_mics:
                    return selected_mics
                else:
                    print(f"No valid microphones found for indices: {indices}")
                    exit(1)
            except ValueError:
                # If mic_filter is not numeric, treat it as a substring filter
                return [mic for mic in all_microphones if mic_filter.lower() in mic.lower()]
        return all_microphones

    def list_microphones(self):
        print("Available microphones:")
        for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{i}: {mic_name}")

    def switch_microphone(self):
        self.current_mic_index = (self.current_mic_index + 1) % len(self.microphones)
        print(f"Switched to: {self.microphones[self.current_mic_index]}")

    def listen_for_activation(self, activation_word):
        print(f"Listening for activation word: '{activation_word}'")
        with sr.Microphone(device_index=self.current_mic_index) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print(f"Microphone ready: {self.microphones[self.current_mic_index]}")
            while True:
                try:
                    print("Waiting for activation word...")
                    audio = self.recognizer.listen(source)
                    transcript = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {transcript}")
                    if activation_word.lower() in transcript.lower():
                        self.switch_microphone()
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
    parser = argparse.ArgumentParser(
        description="Microphone Switcher with Activation Word",
        epilog=(
            "Examples:\n"
            "  python script_name.py -l\n"
            "    List all available microphones.\n"
            "  python script_name.py -f USB -a hello\n"
            "    Use microphones containing 'USB' and set activation word to 'hello'.\n"
            "  python script_name.py -f 0,2 -a switch\n"
            "    Use microphones at indices 0 and 2 and set activation word to 'switch'.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-l", "--list-mics", action="store_true", help="List all available microphones.")
    parser.add_argument("-f", "--mic-filter", type=str, help="Filter microphones by name substring or specify a comma-separated list of indices.")
    parser.add_argument("-a", "--activation-word", type=str, required=True, help="Set the activation word to switch microphones.")
    args = parser.parse_args()

    if args.list_mics:
        MicrophoneSwitcher().list_microphones()
    else:
        switcher = MicrophoneSwitcher(mic_filter=args.mic_filter)
        switcher.listen_for_activation(activation_word=args.activation_word)
