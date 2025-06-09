import yfinance as yf
import openai
import json
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  

client = openai.Client()

def return_price(ticker, period = "1y"):
    ticker_obj = yf.Ticker(f'{ticker}')
    hist = ticker_obj.history(period=period)["Close"]
    hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)
    # Limit the number of rows to 30

    if len(hist) > 30:
        slice_size  = int(len(hist) / 30)
        hist = hist.iloc[::slice_size][::-1]
    return hist.to_json()

tools = [
    { 
        'type': 'function',
        'function': {
            'name':'return_price',
            'description': 'Returns the historical closing prices of IBOVESPA.',
            'parameters': {
                'type':'object',
                'properties': {
                    'ticker':{
                        'type':'string',
                        'description':"The ticker of shares"
                    },
                    'period':{
                        'type':'string',
                        'description':"Return data of shares in select period",
                        'enum': ['1d','5d','1m','6mo','1y','5y','10y','ytd','max']
                    }
                }
            }
        }
    }
]

function_disponible = {'return_price':return_price}


#Realizando a pergunta a OPENAI
def text_generate(mensagens):
    response = client.chat.completions.create(
    messages = mensagens,
    model = 'gpt-3.5-turbo-0125',
    tools = tools,
    tool_choice='auto'
    
    )
    tool_calls = response.choices[0].message.tool_calls
    
    if tool_calls:
        mensagens.append(response.choices[0].message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = function_disponible[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_return = function_to_call(**function_args)     

            mensagens.append({
                'tool_call_id':tool_call.id,
                'role':'tool',
                'name':function_name,
                'content':function_return
            })
            second_response = client.chat.completions.create(
                messages = mensagens,
                model = 'gpt-3.5-turbo-0125'
            )

            mensagens.append(second_response.choices[0].message)

    return mensagens


st.set_page_config(page_title="ChatBot Finance", page_icon="🤖")

st.title("Chatbot  de cotação de ações 📈")

if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []


#Historico de mensagens
for msg in st.session_state.mensagens:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    if msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])


user_input = st.chat_input("Digite a ação e o periodo que deseja informação:")

if user_input:
    st.session_state.mensagens.append({"role":"user","content":user_input})
    st.chat_message("user").markdown(user_input)

    st.session_state.mensagens = text_generate(st.session_state.mensagens)

    last_msg = st.session_state.mensagens[-1]
    if last_msg.role == "assistant":
        st.chat_message("assistant").markdown(last_msg.content)