import yfinance as yf
import openai
import json
from dotenv import load_dotenv

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

mensagens = [{'role':'user','content':'Qual a cotação da Magazine Luiza no ultimo ano?'}]


#Realizando a pergunta a OPENAI
response = client.chat.completions.create(
    messages = mensagens,
    model = 'gpt-3.5-turbo-0125',
    tools = tools,
    tool_choice='auto'

)

#Resgatando as informações da ação
tool_calls = response.choices[0].message.tool_calls
# print(tool_calls)

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
        print(second_response.choices[0].message)