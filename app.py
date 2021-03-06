#!pip install streamlit
#!apt-get install python3.7
#!pip install ipykernel
#!pip install -q streamlit
#pip install openai

#!wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
#!unzip ngrok-stable-linux-amd64.zip
#get_ipython().system_raw('./ngrok http 8501 &')

#!curl -s http://localhost:4040/api/tunnels | python3 -c \
#st.session_state



import urllib
from random import randint
#import torch
#from transformers import pipeline, set_seed
#from transformers.pipelines import TextGenerationPipeline
import streamlit as st


from SessionState import _SessionState, _get_session, _get_state

import logging
import openai as openai

API_KEY = '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'


def shabdifyTextGeneratorUsingAda(textstr, noOfWords=5):

    openai.api_key= data['API_KEY']
    response = openai.Completion.create(
      engine="ada",
      prompt=textstr,
      temperature=0.1,
      max_tokens=noOfWords,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    );

    return response.choices[0].text;

#def shabdify_suggest(text: str) -> str:
 #   content  = text
  #  value = shabdifyTextGeneratorUsingAda(content, 5)
   # st.write(value);
    #return value;




#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def main():

    state = _get_state()
    st.set_page_config(page_title="Mail Assistant", page_icon="📧")

    # set_seed(42)  # for reproducibility
   
    load_page(state)

    state.sync()  # Mandatory to avoid rollbacks with widgets, must be called at the end of your app


def load_page(state: _SessionState):
    disclaimer_short = """
    __Disclaimer__: 
    """
    disclaimer_long = """
    __Description__: This part is under development

    """
    st.markdown(disclaimer_short)
    st.sidebar.markdown(disclaimer_long)

    # st.write("---")

    st.title("Shabdify")

    state.input = st.text_area(
        "Content (add more words for better results):",
        state.input,
        height=200,
        max_chars=5000,
    )

    state.slider = st.slider(
        "Output length:",
        5,
        500,
        state.slider,
    )

    if len(state.input) + state.slider > 500:
        st.warning("Your output cannot be longer than 500 words")
        st.stop()

    button_generate = st.button("Generate Content")
   

    if button_generate:
        try:
            output_text = shabdifyTextGeneratorUsingAda(state.input, state.slider)
            
            state.input = st.text_area(
                "Start your story:", output_text or "", height=50
            )
        except:
            pass

    st.markdown(
        '<h2 style="text-align:center;">Your results appear here</h2>',
        unsafe_allow_html=True,
    )

    for i, line in enumerate(state.input.split("\n")):
        if ":" in line:
            speaker, speech = line.split(":")

            st.markdown(
                f'<p style="font-family:Courier;text-align:center;"><b>{speaker}:</b><br>{speech}</br></p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<p style="font-family:Courier;text-align:center;">{line}</p>',
                unsafe_allow_html=True,
            )
    
    st.markdown("---")
   


if __name__ == "__main__":
    main()
