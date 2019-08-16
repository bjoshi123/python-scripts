import speech_recognition as sr
import pyaudio
import wave
import requests


def record_audio(chunk, a_format, channels, frame_rate, record_seconds=5, file_name='output.wav'):
    '''
    API to record audio in wav format
    '''
    p = pyaudio.PyAudio()
    stream = p.open(format=a_format,
                    channels=channels,
                    rate=frame_rate,
                    input=True,
                    frames_per_buffer=chunk)  # buffer

    print("***recording started***")
    frames = []

    for i in range(0, int(frame_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("***recording stopped***")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(a_format))
    wf.setframerate(frame_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def google_speech_to_text(file_name):
    '''
    API to convert speech to text using google speech recognition
    '''
    r = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
    try:
        s = r.recognize_google(audio)
        print("Google Text: " + s)
    except Exception as e:
        print("Sorry I don't understand")

def nuance_speech_to_text(file_name):
    '''
    API to convert speech to text using nuance speech to text api
    make a account in nuance.developer.com, create app or from sandbox credential you will get app-id, app key
    id is device id
    '''
    url = 'https://dictation.nuancemobility.net/NMDPAsrCmdServlet/dictation?appId=[app-id]&appKey=[app-key]&id=[device-id]'
    headers = {}
    headers['Content-Type'] = 'audio/x-wav;codec=pcm;bit=16;rate=8000'
    headers['Accept-Language'] = 'eng-IND'
    headers['Accept'] = 'application/xml'
    headers['Accept-Topic'] = 'Dictation'
    data = open(file_name, 'rb')
    print("request started")
    r = requests.post(url, headers=headers, data=data)

    if r.status_code == 200:
        print("Nuance API: ", r.text)
    else:
        print("Sorry I don't understand")
        #print(r.content)


chunk = 1024
a_format = pyaudio.paInt16
channels = 1
frame_rate = 8000
record_seconds = 2
file_name = "output.wav"

record_audio(chunk, a_format, channels, frame_rate, record_seconds, file_name)
google_speech_to_text(file_name)
nuance_speech_to_text(file_name)








