import argparse
import pyaudio
import speech_recognition as sr
import time

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage()
        print(f"Error: {message}\n")
        print(self.format_help())
        self.exit(2)

class MicrophoneSwitcher:
    def __init__(self, mic_filter=None, sleep_word="sleep", sleep_time=30):
        self.recognizer = sr.Recognizer()
        self.microphones = self.get_filtered_microphones(mic_filter)
        if not self.microphones:
            print("No microphones match the filter. Exiting.")
            exit(1)
        self.current_mic_index = 0  # Default to the first microphone
        self.starting_mic_index = 0  # Remember the starting microphone
        self.sleep_word = sleep_word
        self.sleep_time = sleep_time

    def get_filtered_microphones(self, mic_filter):
        all_microphones = sr.Microphone.list_microphone_names()
        if mic_filter is not None:
            try:
                indices = [int(idx) for idx in mic_filter.split(",") if idx.isdigit()]
                selected_mics = [all_microphones[i] for i in indices if 0 <= i < len(all_microphones)]
                if selected_mics:
                    return selected_mics
                else:
                    print(f"No valid microphones found for indices: {indices}")
                    exit(1)
            except ValueError:
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
        last_activity_time = time.time()
        with sr.Microphone(device_index=self.current_mic_index) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print(f"Microphone ready: {self.microphones[self.current_mic_index]}")
            while True:
                try:
                    print("Waiting for activation word or sleep word...")
                    # Listen for speech
                    audio = self.recognizer.listen(source, timeout=self.sleep_time)
                    transcript = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {transcript}")

                    # Check if the activation word is the first word
                    words = transcript.strip().split()
                    if words and words[0].lower() == activation_word.lower():
                        self.switch_microphone()
                        last_activity_time = time.time()
                    elif words and words[0].lower() == self.sleep_word.lower():
                        print(f"Detected sleep word: '{self.sleep_word}'")
                        self.return_to_starting_mic()
                        break

                except sr.WaitTimeoutError:
                    if time.time() - last_activity_time >= self.sleep_time:
                        print("No activity detected for sleep time. Returning to starting microphone.")
                        self.return_to_starting_mic()
                        break
                except sr.UnknownValueError:
                    print("Could not understand audio. Try again.")
                except sr.RequestError as e:
                    print(f"Error with speech recognition service: {e}")

    def return_to_starting_mic(self):
        self.current_mic_index = self.starting_mic_index
        print(f"Switched back to starting microphone: {self.microphones[self.starting_mic_index]}")

if __name__ == "__main__":
    parser = CustomArgumentParser(
        description="Microphone Switcher with Activation and Sleep Word",
        epilog=(
            "Examples:\n"
            "  python main.py -l\n"
            "    List all available microphones.\n"
            "  python main.py -f USB -a hello -s sleep -t 30\n"
            "    Use microphones containing 'USB', set activation word to 'hello',\n"
            "    sleep word to 'sleep', and timeout to 30 seconds."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-l", "--list-mics", action="store_true", help="List all available microphones.")
    parser.add_argument("-f", "--mic-filter", type=str, help="Filter microphones by name substring or specify a comma-separated list of indices.")
    parser.add_argument("-a", "--activation-word", type=str, help="Set the activation word to switch microphones.")
    parser.add_argument("-s", "--sleep-word", type=str, default="sleep", help="Set the sleep word to return to the starting microphone (default: 'sleep').")
    parser.add_argument("-t", "--sleep-time", type=int, default=30, help="Set the sleep timeout in seconds (default: 30).")
    args = parser.parse_args()

    if not args.list_mics and not args.activation_word:
        parser.error("The -a/--activation-word argument is required unless -l/--list-mics is specified.")

    if args.list_mics:
        MicrophoneSwitcher().list_microphones()
    else:
        switcher = MicrophoneSwitcher(mic_filter=args.mic_filter, sleep_word=args.sleep_word, sleep_time=args.sleep_time)
        switcher.listen_for_activation(activation_word=args.activation_word)
