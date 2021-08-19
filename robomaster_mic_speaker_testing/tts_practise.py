from gtts import gTTS
import os

mytext="four" #set what you want to say

language="en"

myobj = gTTS(text=mytext, lang=language, slow=True) #google text to speech

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("four.mp3")

# Playing the converted file
os.system("four.mp3")
