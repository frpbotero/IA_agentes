import openai
import speech_recognition as sr
from playsound import playsound
from pathlib import Path
from io import BytesIO

client = openai.Client()

audio_file = "hello.mp3"

recognizer = sr.Recognizer()

def record_audio():
    MIC_INDEX = 6  # Ou índice correto do Lenovo
    with sr.Microphone(MIC_INDEX) as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    return audio
         



def audio_transcription(audio_file_path):
    try:
        with open(audio_file_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return transcription.text
    except Exception as e:
        print(f"Erro na transcrição {e}")
        return ""
    

def text_completion(messages):
    try:
        response = client.chat.completions.create(
            messages=messages,
            model = "gpt-3.5-turbo-0125",
            max_tokens=1000,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na geração de reposta {e}")
        return "Desculpe não consegui entender"
    
def audio_generate(text):
    if Path(audio_file).exists():
        Path(audio_file).unlink()
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            instructions="Speech with positive tone and slowly"
        )
        return response.write_to_file(audio_file)
    except Exception as e:
        print(f"Erro na criação do audio {e}")
        return "Desculpe não foi possivel criar o audio!"
    

def play_sound():
    if Path(audio_file).exists():
        playsound(audio_file)
    else:
        print("Erro: O arquivo não foi encontrado!")

def main():
    mensagens = []
    
    while True:
        audio_file_path = "/home/fbotero/Documents/Courses/openapi-app/teste.mp3"
        transcription = audio_transcription(audio_file_path)

        if not transcription:
            print("Não foi possivel transcrever o audio, tente novamente")
            break  # ou continue, se quiser laço infinito

        print("Usuário (transcrição):", transcription)
        mensagens.append({"role":"user","content":transcription})

        text_response = text_completion(mensagens)
        print("Assistente:", text_response)
        mensagens.append({"role":"assistant","content":text_response})

        audio_generate(text_response)
        play_sound()



if __name__ == "__main__":
    main()
