import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# This is SYNCHRONOUS, so it will block until the text is done being spoken
# If you want to say something asynchronously, use sayAsync
def say(text: str):
    engine.say(text)
    engine.runAndWait()

def sayAsync(text: str):
    engine.say(text)
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()
