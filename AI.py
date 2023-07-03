import openai

class AI:
    def __init__(self, model="gpt-3.5-turbo-0613", temperature=0):
        self.temperature = temperature

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
        
if __name__ == "__main__":
    ai = AI()
    messages =  [  
    {'role':'system', 
    'content': "None"},    
    {'role':'user', 
    'content': f"hi"},  
    ] 
    ans = ai.get_completion_from_messages(messages = messages)
    print(ans)