import openai
from colorama import Fore, Style, init
# Initialize colorama
init(autoreset=True)

client = openai.Client()

def generate_text(mensagens):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages= mensagens,
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    print(f"{Fore.BLUE}Bot: ", end='')
    texto_completo = ""
    for response_stream in response:
        texto = response_stream.choices[0].delta.content
        if texto:
            print(texto, end='')
            texto_completo += texto
    print()
    mensagens.append({"role": "assistant", "content": texto_completo})
    return mensagens
if __name__ == "__main__":
    print(f"{Fore.YELLOW}Chatbot iniciado. Digite 'sair' para encerrar.")
    mensagens = []
    while True:
        in_user = input(f"{Fore.GREEN}user: ")
        mensagens.append({"role": "user", "content": in_user})
        if in_user.lower() == "sair":
            break
        mensagens = generate_text(mensagens)