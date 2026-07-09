import os

import gradio
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def initialize_messages():
    return [{"role": "system",
             "content": '''You are an agriculture expert with a masters degree in Agriculture with specialization in Agronomy.
              Your role is to assist people by providing guidance on farming, home gardens, rooftop farming tips and nutrition information.
              Do not provide any response for questions unrelated to farming or agriculture, specify you are only meant to provide farming assistance.
              For short answer questions, give responses only of the required length.
              Refer accurate environmental stats and provide scenarios to help understand complex farming situations.
              The climate of Kerala, India should be the only climate to be referred for all questions.
              Do not encourage abusive or disrespectful language from the user.'''}]

messages_prmt = initialize_messages()

def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )
    print(response)
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply

env_theme = gradio.Theme.from_hub("kbray/NeoSand")

iface = gradio.ChatInterface(customLLMBot,
                     chatbot=gradio.Chatbot(height=300),
                     textbox=gradio.Textbox(placeholder="Ask me a question related to gardening! <3"),
                     title="SeedStory",
                     description="Your Home Gardening Assistant",
                     
                     examples=["Can I grow dragonfruit in rainy weather?","What is the right humidity for growing tomatoes?", "How do I grow passion fruit at home?"]
                     )
iface.launch(
    theme=env_theme,
    share=True
)
