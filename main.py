import os
import shutil
import signal
from time import sleep

import notify2 as notify
from gtts import gTTS
from playsound import playsound

import speech_recognition as sr
from functions.youtube.youtube import open_youtube
from functions.google.google import open_google
from snow_boy import snowboydecoder

interrupted = False


class Athena:
	def __init__(self):
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
		self.actions = {
			"google search": open_google,
			"youtube search": open_youtube
		}

	def wake_up(self):
		GENERAL_VOICE_PATH = os.path.join(
			os.getcwd(), "voice", "trigger_voice.mp3")

		if os.path.isfile(GENERAL_VOICE_PATH):
			playsound(GENERAL_VOICE_PATH)
		else:
			message = "Hi Kevin, how can i help you?"
			trigger_voice = gTTS(text=message)
			trigger_voice.save("trigger_voice.mp3")
			shutil.move("trigger_voice.mp3", GENERAL_VOICE_PATH)
			playsound(GENERAL_VOICE_PATH)

	def detect_action(self):
		notify.init("A.T.H.E.N.A")

		ICON_PATH = os.path.join(os.getcwd(), "athena.ico")

		notice = notify.Notification(
			"Initializing A.T.H.E.N.A", icon=ICON_PATH)

		notice.set_urgency(notify.URGENCY_NORMAL)
		notice.set_timeout(4000)
		notice.show()
		self.wake_up()
		sleep(6)

		while True:

			try:
				notice.update("Begin Speaking")
				notice.show()
				with self.microphone as source:
					self.recognizer.energy_threshold = 4000
					audio = self.recognizer.listen(source)
				speech = self.recognizer.recognize_google(audio)
				speech = speech.lower()
				count = 0
				for action in self.actions.keys():
					if speech in action:
						self.call_action(action)
						break
					count += 1

				if count == len(self.actions):
					sleep(6)
					notice.update(f"couldn't find {speech} in valid actions, try again")
					notice.show()
					continue

				break

			except Exception as e:
				sleep(6)
				notice.update("Unable to recognize try again", f"{e}")
				notice.show()
				continue

		notice.close()		

	def call_action(self, action):
		self.actions[action](self.recognizer, self.microphone)

if __name__ == "__main__":
	def detect_callback():
		NOTIFICATIONS_PATH = os.path.join(
			os.getcwd(), "voice", "notifications", "notificationaudio.mp3")
		playsound(NOTIFICATIONS_PATH)

		athena = Athena()
		athena.detect_action()

		del athena


	def signal_handler(signal, frame):
		global interrupted
		interrupted = True


	def interrupt_callback():
		global interrupted
		return interrupted


	signal.signal(signal.SIGINT, signal_handler)
	detector = snowboydecoder.HotwordDetector(
		"snow_boy/Athena.pmdl", sensitivity=0.5)
	detector.start(detected_callback=detect_callback,
				interrupt_check=interrupt_callback,
				sleep_time=0.03)
	detector.terminate()
