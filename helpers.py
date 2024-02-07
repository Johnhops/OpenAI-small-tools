import openai,time,math,soundfile as sf,sounddevice as sd
from scipy.io.wavfile import write

path = r'./'
OPENAI_API_KEY = 'YOUR_API_KEY'

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def record(save_as='./Files/temp.mp3',freq = 44100,duration=5):
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)
    for i in range(math.ceil(duration),0,-1):
            print(f'{i:3g}',end='\r')
            time.sleep(1)
    write(save_as, freq, recording)

def play(open_fname,wait=False):
    sd.play(*sf.read(open_fname, dtype = 'float32'))
    if wait:sd.wait()

def OpenAI_Audio2text(open_fname='',toEN=False,model="whisper-1",duration=5):
    if not open_fname:
        open_fname = './Files/temp.mp3'
        sd.play(*sf.read('./Files/0. Say_something.mp3', dtype = 'float32'))
        sd.wait()
        record(save_as=open_fname,duration=duration)
    with open(open_fname,'rb') as audio_file:
        if toEN:resp = client.audio.translations.create(model = model, file = audio_file,) 
        else:resp = client.audio.transcriptions.create(model = model, file = audio_file,) 
            
    return resp.text 

def OpenAI_Text2audio(text,save_as='',model='tts-1',voice='alloy'):
    response = client.audio.speech.create(model=model,voice=voice,input=text,)
    if save_as:response.stream_to_file(save_as)
    return response

def OpenAI_TextChat(Q,model='gpt-3.5-turbo'):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model = model,
        messages = [
            {'role':'user','content':Q},
                ]
    )
    A = response.choices[0].message.content
    return A

def OpenAI_AudioChat(open_fname='',save_as='./Files/answer_audio.mp3',toEN=False,show_answer=True,read_aloud=True,duration=5,
                     gpt_model='gpt-3.5-turbo',tts_model='tts-1',voice='alloy'):
    if not open_fname:
        play('./Files/1. Please_ask.mp3',wait=True)
        open_fname = "./Files/temp.mp3"
        record(open_fname,duration=duration)
        play('./Files/2. Let_me_think.mp3')
    question_text = OpenAI_Audio2text(open_fname,toEN=toEN)
    print(question_text)
    answer_text = OpenAI_TextChat(question_text,model=gpt_model)
    if show_answer:print(answer_text)
    if read_aloud:play('./Files/3. A_moment.mp3')
    answer_audio = OpenAI_Text2audio(text=answer_text,save_as=save_as,model=tts_model,voice=voice)
    if read_aloud:play(save_as)
    if save_as:answer_audio.stream_to_file(save_as)
    return answer_text