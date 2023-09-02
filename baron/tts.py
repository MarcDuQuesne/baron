import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('rate', 120) # Speed percent (can go over 100
engine.setProperty('volume', 0.9) # Volume 0-1
engine.setProperty('voice', voices[0].id) # Voice ID
engine.setProperty('pitch', (0.5, 1)) # Pitch 0-1
# Convert text to speech
engine.say('<pitch middle="0">Emma Emma emma</pitch>')
# engine.say(text)

# Play the speech
engine.runAndWait()
