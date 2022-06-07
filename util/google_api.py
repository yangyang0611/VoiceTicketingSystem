import speech_recognition as sr
import subprocess

r = sr.Recognizer()


def google_asr(file_name):
    WAV = sr.AudioFile(file_name)
    with WAV as source:
        audio = r.record(source)
    
    print("zh: ",r.recognize_google(audio, language="zh"))
    print("zh-TW: ",r.recognize_google(audio, language="zh-TW"))
    print("zh-HK: ",r.recognize_google(audio, language="zh-HK"))
    return r.recognize_google(audio, language="zh")



if __name__ == "__main__":
    # src = "audio.mp3"
    # dst = "audio.wav"                                                       
    # subprocess.call(['C:\\ffmpeg\\bin\\ffmpeg', '-i', src, dst])

    dst = "audiotest3.wav" 
    result =  google_asr(dst)
    
    print(dst)
    print(result)
    


