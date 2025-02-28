from utils.validations import validate_url
import constants.embeddings as embd_const
import constants.llms as llm_const
import constants.models as models_const
from ui.train import train_model, query_model
import streamlit as st


st.title("DuploCLoud AI Assistant")

with st.sidebar:
    llm_chosen = st.radio("Choose LLM", options=llm_const.LLMS, horizontal=True)
    embedding_chosen = st.selectbox("Choose Embedding Model", options=embd_const.EMBEDDING_MODELS[llm_chosen])
    model_chosen = st.selectbox("Choose Text Model", options=models_const.LLM_MODELS[llm_chosen])

    # github url input
    st.markdown("## Github Details")
    url = st.text_input("Github repo",
                        value="https://github.com/duplocloud/docs/tree/main/getting-started-1", 
                        placeholder="https://github.com/duplocloud/docs/tree/main/getting-started-1",
                        )
                
    if st.button("Train", type="primary"):
        if not validate_url(url):
            st.error("Invalid URL")
        else:
            with st.spinner(text="Training the model",show_time=True):
                train_model(url, model_chosen, embedding_chosen)


question = st.text_input("Your Question")
if st.button("Send"):
    try:
        response = query_model(question, embedding_chosen)
        st.write(response)
    except FileNotFoundError as e:
        st.error("Please train the model, before querying")
