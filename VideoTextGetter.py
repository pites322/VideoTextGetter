import speech_recognition as sr
import pandas as pd
import pytube
from pytube.exceptions import RegexMatchError


def download_video(video_url):
    # download video with audio codek and lowest resolution to video directory and return path
    try:
        video_information = pytube.YouTube(video_url)
    except RegexMatchError:
        print('You input incorrect url')
        path_to_video = ''
        return path_to_video
    video_variants = video_information.streams.all()
    video_variants_resolution_dict = {}
    video_list_num = 0
    for elem in video_variants:
        if elem.includes_audio_track and elem.resolution:
            if len(elem.resolution) == 4:
                video_variants_resolution_dict.update({elem.resolution[:3]: video_list_num})
            elif len(elem.resolution) == 5:
                video_variants_resolution_dict.update({elem.resolution[:4]: video_list_num})
        video_list_num += 1
    path_to_video = video_variants[video_variants_resolution_dict[min(video_variants_resolution_dict.keys())]]\
        .download(filename='video')
    return path_to_video


def take_text_from_video_and_save_to_csv():
    # get text from wav
    recognizer = sr.Recognizer()

    audio = 'audio.wav'
    # read audio file
    with sr.AudioFile(audio) as source:
        audio = recognizer.record(source)
        print('extracting text from video started')
    # try to get text from google recognize and save to csv
    try:
        # text = recognizer.recognize_sphinx(audio)
        text = recognizer.recognize_google(audio)
        df = pd.DataFrame(text.lower().split(' '), columns=["word"])
        df.to_csv('words.csv', index=False)
        print('extracting text from video ended')
        return True
    # raise exception if it happened
    except Exception as e:
        print(f'unfortunately extracting text from video was ended with exception: {e}. Please try again later or '
              f'change video')
        return False


na_values = ['of', 'with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout',
             'despite', 'towards', 'upon', 'concerning', 'to', 'in', 'for', 'on', 'by', 'about', 'like', 'through',
             'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', 'following',
             'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off', 'above',
             'near', 'the', 'a', 'so', 'at', 'that', 'and', 'ok', 'i', 'am', 'he', 'she', 'it', 'is', 'you', 'we',
             'they', 'are', 'will', 'be', 'was', 'were', 'as', 'or', "it's", 'so', 'been']