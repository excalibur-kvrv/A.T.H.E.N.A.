import os
import shutil
import webbrowser
from time import sleep

import notify2 as notify
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from requests_html import HTMLSession


def open_youtube(recognizer, microphone):
	SEARCH_QUERY_PATH = os.path.join(os.getcwd(), "voice", "youtube", "search_query.mp3")

	notify.init("A.T.H.E.N.A youtube action")
	notice = notify.Notification("Initializing youtube action", icon="youtube.png")
	notice.set_urgency(notify.URGENCY_NORMAL)
	notice.set_timeout(4000)
	notice.show()
	sleep(6)

	if os.path.isfile(SEARCH_QUERY_PATH):
		playsound(SEARCH_QUERY_PATH)
	else:
		message = "What would you like to search?"
		search_query = gTTS(text=message)
		search_query.save("search_query.mp3")
		shutil.move("search_query.mp3", SEARCH_QUERY_PATH)
		playsound(SEARCH_QUERY_PATH)

	while True:
		try:
			notice.update("Begin speaking")
			notice.show()
			with microphone as source:
				recognizer.energy_threshold = 4000
				audio = recognizer.listen(source)
			query = recognizer.recognize_google(audio)
			break
		except Exception as e:
			sleep(6)
			notice.update("Please try again", f"{e}")
			notice.show()
			continue

	print(f"your query is {query}")
	url = f"https://www.youtube.com/results?search_query={'+'.join(query.split())}"
	print(f"request url is {url}")
	videos_list = find_videos(url)
	videos = []
	for video in videos_list.keys():
		sleep(6)
		notice.update(f"{video}")
		notice.show()
		videos.append(video)

	sleep(6)

	VIDEO_PATH = os.path.join(os.getcwd(), "voice", "youtube", "which_video.mp3")

	if os.path.isfile(VIDEO_PATH):
		playsound(VIDEO_PATH)
	else:
		message = "Which video would you like to play?"
		which_video = gTTS(text=message)
		which_video.save("which_video.mp3")
		shutil.move("which_video.mp3", VIDEO_PATH)
		playsound(VIDEO_PATH)

	while True:
		try:
			notice.update("begin speaking")
			notice.show()
			with microphone as source:
				recognizer.energy_threshold = 4000
				audio = recognizer.listen(source)
			query = recognizer.recognize_google(audio)
			found = get_video_url(query, videos, videos_list)
			if found:
				webbrowser.open(f"https://www.youtube.com{found}")
				break
			else:
				sleep(6)
				notice.update(f"Unable to recognize {query}")
				notice.show()
				continue
		except Exception as e:
			sleep(6)
			notice.update(f"Try again",f"{e}")
			notice.show()
			continue

	notice.close()	

def get_video_url(query, videos, videos_list):
	query = query.lower()
	if "1st" in query or "first" in query:
		return videos_list[videos[0]]
	elif "2nd" in query or "second" in query:
		return videos_list[videos[1]]
	elif "3rd" in query or "third" in query:
		return videos_list[videos[2]]
	elif "4th" in query or "fourth" in query:
		return videos_list[videos[3]]
	elif "5th" in query or "fifth" in query:
		return videos_list[videos[4]]
	elif "6th" in query or "sixth" in query:
		return videos_list[videos[5]]
	elif "7th" in query or "seventh" in query:
		return videos_list[videos[6]]
	elif "8th" in query or "eighth" in query:
		return videos_list[videos[7]]
	elif "9th" in query or "ninth" in query:
		return videos_list[videos[8]]
	elif "10th" in query or "tenth" in query:
		return videos_list[videos[9]]
	return ""

def find_videos(url):
	session = HTMLSession()
	res = session.get(url)
	res.html.render(sleep=2)
	size_count = 0
	videos_list = {}
	for video in res.html.find("#video-title"):
		try:
			size_count += 1
			videos_list[video.attrs["title"]] = video.attrs["href"]
		except:
			continue
		if size_count == 10:
			break
	return videos_list
