!pip install streamlit
!apt-get install python3.7
!pip install ipykernel
!pip install -q streamlit
!pip install openai
%env OPENAI_API_KEY=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

!wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip ngrok-stable-linux-amd64.zip
get_ipython().system_raw('./ngrok http 8501 &')

!curl -s http://localhost:4040/api/tunnels | python3 -c \
st.session_state

import urllib
from random import randint
#import torch
#from transformers import pipeline, set_seed
#from transformers.pipelines import TextGenerationPipeline
import streamlit as st
from SessionState import _SessionState, _get_session, _get_state
import logging
import openai


API_KEY = os.getenv("OPENAI_API_KEY");

def shabdifyTextGeneratorUsingAda(textstr, noOfWords=1):
    openai.api_key=API_KEY
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

def shabdify_suggest():
    content  = request.args.get('content', None)
    value = shabdifyTextGeneratorUsingAda(content, 10)
    print(content);
    return value;








device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_bad_words() -> list:
    res_list = []

    try:
        file = urllib.request.urlopen(
            "https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/list.txt"
        )
        for line in file:
            dline = line.decode("utf-8")
            res_list.append(dline.split("\n")[0])
    except:
        logging.info("Failed to load bad words list.")

    return res_list


BAD_WORDS = load_bad_words()

STARTERS = {}


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_model() -> TextGenerationPipeline:
    return pipeline("text-generation", model="e-tony/gpt2-rnm")


def filter_bad_words(text: str) -> str:
    explicit = False

    res_text = text.lower()
    for word in BAD_WORDS:
        if word in res_text:
            print(word)
            res_text = res_text.replace(word, word[0] + "*" * len(word[1:]))
            explicit = True

    if explicit:
        output_text = ""
        for oword, rword in zip(text.split(" "), res_text.split(" ")):
            if oword.lower() == rword:
                output_text += oword + " "
            else:
                output_text += rword + " "
        text = output_text

    return text


def main():
    state = _get_state()
    st.set_page_config(page_title="Story Generator", page_icon="🛸")

    model = load_model()
    # set_seed(42)  # for reproducibility

    load_page(state, model)

    state.sync()  # Mandatory to avoid rollbacks with widgets, must be called at the end of your app


def load_page(state: _SessionState, model: TextGenerationPipeline):
    disclaimer_short = """
    __Disclaimer__: 
    """
    disclaimer_long = """
    __Description__:

    """
    st.markdown(disclaimer_short)
    st.sidebar.markdown(disclaimer_long)

    # st.write("---")

    st.title("Shabdify")

    state.input = st.text_area(
        "Content:",
        state.input or STARTERS[randint(0, 6)],
        height=200,
        max_chars=5000,
    )

    state.slider = st.slider(
        "Max story length (add more words for better results):",
        50,
        1000,
        state.slider,
    )

    if len(state.input) + state.slider > 5000:
        st.warning("Your story cannot be longer than 5000 characters!")
        st.stop()

    button_generate = st.button("Generate Content")
   

    if button_generate:
        try:
            outputs = model(
                state.input,
                do_sample=True,
                max_length=len(state.input) + state.slider,
                top_k=50,
                top_p=0.95,
                num_return_sequences=1,
            )
            output_text = filter_bad_words(outputs[0]["generated_text"])
            state.input = st.text_area(
                "Start your story:", output_text or "", height=50
            )
        except:
            pass

    st.markdown(
        '<h2 style="font-family:Courier;text-align:center;">Your Story</h2>',
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
