import streamlit as st
import time


def get_chat_response(user_input):
    """
    Dummy function to simulate chat response.

    Parameters:
    user_input (str): The user's input.

    Returns:
    str: The chat response.
    """
    # Replace this with your own function
    return f"You said: {user_input}"


# Set page configuration
st.set_page_config(
    page_title="iSAPedia",
    page_icon=":open_book:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "### This is a header." "\nThis is an *extremely* cool app!",
    },
)

# Add sidebar
st.sidebar.markdown(
    """<h1 style='font-size: 36px;'><span style="color: #ff0000;">i</span>SAP<span style="color: #ff0000;">edia</span></h1><p>&nbsp;</p>""",
    unsafe_allow_html=True,
)

# Add option to select LLM model
st.sidebar.markdown("## Model Type")
selected_model = st.sidebar.selectbox(
    "Select LLM model",
    ["GPT 3.5", "GPT 4", "Llama 3", "Anthropic"],
    index=None,
    placeholder="Choose your desired Model",
)

# Add info box
infobox_placeholder = st.sidebar.empty()

if selected_model:
    infobox_placeholder.info("Option selected: " + selected_model)
    time.sleep(2)

infobox_placeholder.empty()

# Add option to upload PDF files
st.sidebar.markdown("---")
st.sidebar.markdown("## Use your own file")
uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type="pdf",
    help="Upload your PDF file here and inquire freely",
)
uploaded_placeholder = st.sidebar.empty()

# Add a progress bar to simulate file upload
if uploaded_file:
    uploaded_placeholder.progress(0, text="Uploading... Please wait.")
    for percent_complete in range(100):
        time.sleep(0.01)
        uploaded_placeholder.progress(
            percent_complete + 1, text="Uploading... Please wait."
        )
    time.sleep(1)
    uploaded_placeholder.success("File uploaded successfully!")
    time.sleep(2)
uploaded_placeholder.empty()

# Add Title
st.markdown(
    """<h1 style='font-size: 36px;'><span style="color: #ff0000;">SAP </span>Knowledge Base <span style="color: #ff0000;">Query App</span></h1><p>&nbsp;</p>""",
    unsafe_allow_html=True,
)

# Add a chat input
chat_prompt = st.chat_input(placeholder="Enter your question...", key="chat_input")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := chat_prompt:
    # Display user message in chat message container
    st.chat_message(name="human").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "human", "content": prompt})

    response = get_chat_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message(name="ai"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "ai", "content": response})
