import streamlit as st
from agents.graph import FrontendAgent

if st.session_state.get("frontend_agent") is None:
    frontend_agent = FrontendAgent(data_path="data\\shadcn.csv")
    st.session_state.frontend_agent = frontend_agent

st.set_page_config(page_title="Chat to frontend with Shadcn", layout="wide")
# Streamlit UI elements
st.title("Chat to frontend with Shadcn Agent")

# Input from user
input_text = st.text_area("Enter the frontend component or page you want to create:")

if st.button("Run Agent"):
    results = []
    with st.spinner():
        for output in st.session_state.frontend_agent.run(input_text):
            results.append(output)
            if output["node"] == "select":
                st.write("Selected components:")
                st.code(output["output"])
            elif output["node"] == "outline":
                st.write("Frontend Outline:")
                st.write(output["output"])
            elif output["node"] == "code":
                st.write("Frontend Code:")
                st.code(output["output"], language="tsx")
            elif output["node"] == "refine":
                st.write("Refined Frontend Code:")
                st.code(output["output"], language="tsx")
    st.write("Done!")