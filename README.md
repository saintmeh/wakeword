quick little late night project I whipped up to give Chat GPT a wake word on a conference mic in my hackerspace.

This will be good for, let's say adding a wake word to chat gpt's browser based interface.

the idea is that everything will be using a dummy software-only dead mic.

When the wake word is said, the default microphone is set and the dummy mic is disabled.  

After a bit, the dummy mic is re-enabled, the dummy mic is set as the default, and the former default is disabled to force a state change.
