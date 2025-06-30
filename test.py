import speech_recognition as sr

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Testando índice {i}: {name}")
    try:
        with sr.Microphone(i) as source:
            print(f"  -> OK: {name}")
    except Exception as e:
        print(f"  -> Falhou: {e}")