import gradio as gr
import time

def greet(name):
    time.sleep(3)
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(share=True)   

# OK for the window