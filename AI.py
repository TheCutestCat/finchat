import openai

class AI:
    def __init__(self, model="gpt-3.5-turbo-0613"):
        try:
            # get the OPENAI_API_KEY
            openai.Model.retrieve(model)
            self.model = model
        except openai.InvalidRequestError:
            print(
                f"Please set upt the OPENAI_API_KEY in the enverment."
            )        
    
    def get_completion_from_messages(self,messages, 
                                 model="gpt-3.5-turbo-0613", 
                                 temperature=0, 
                                 max_tokens=500):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
            # functions = functions,
            # function_call="auto"
        )
        return response.choices[0].message["content"]    
    
    def get_completion_from_messages_function(messages, 
                                 functions,
                                 model="gpt-3.5-turbo-0613", 
                                 temperature=0, 
                                 max_tokens=500):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
            functions = functions,
            function_call="auto"
        )
        if(response.choices[0].message["content"]!="Nones"):
            return response.choices[0].message["function_call"]
        else: 
            return response.choices[0].message["content"]
    
    def chat_completion_request(messages, functions=None, function_call=None, model="gpt-3.5-turbo-0613"):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }
        json_data = {"model": model, "messages": messages}
        if functions is not None:
            json_data.update({"functions": functions})
        if function_call is not None:
            json_data.update({"function_call": function_call})
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
        
if __name__ == "__main__":
    ai = AI()
    functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
            },
            "required": ["location", "format"],
        },
    },
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
                "num_days": {
                    "type": "integer",
                    "description": "The number of days to forecast",
                }
            },
            "required": ["location", "format", "num_days"]
        },
    },
]
    MA = []
    MA.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    MA.append({"role": "user", "content": "What's the weather like today"})
    chat_response = ai.chat_completion_request(
    messages=MA, functions=functions)
    assistant_message = chat_response.json()["choices"][0]["message"]
    print(assistant_message)