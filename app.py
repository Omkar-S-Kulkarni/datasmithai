import streamlit as st
from agent_chatbot_openrouter import run_agent
from audio_chatbot_openrouter import get_audio
from image_openrouter import readPdf

#i have added css as ui lyer we can add more but kept simple 
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}

h1, h2, h3 {
    color: #00ffd5;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(135deg, #00ffd5, #00c2a8);
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}

.stTextInput>div>div>input {
    background-color: #2a2d36;
    color: white;
}

.stTextArea textarea {
    background-color: #2a2d36;
    color: white;
}

.success-box {
    padding: 10px;
    border-radius: 8px;
    background-color: #0f5132;
    color: #d1e7dd;
}

.error-box {
    padding: 10px;
    border-radius: 8px;
    background-color: #842029;
    color: #f8d7da;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1>AI Multi Tool</h1>", unsafe_allow_html=True)

mode = st.radio(
    "Choose Mode",
    ["chat", "pdf", "audio"],
    horizontal=True
)


if mode == "chat":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2>Chat Mode</h2>", unsafe_allow_html=True)

    q = st.text_input("Ask anything")

    if st.button("Send"):
        if q:
            res = run_agent(q)

            if "followup" in res:
                st.warning(res["followup"])
            else:
                st.write(res["result"])

            st.subheader("Logs")
            st.write(res["logs"])

    st.markdown('</div>', unsafe_allow_html=True)



elif mode == "pdf":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2>PDF Mode</h2>", unsafe_allow_html=True)

    file = st.file_uploader("Upload PDF")

    if file:
        with open("temp.pdf", "wb") as f:
            f.write(file.read())

        txt, conf = readPdf("temp.pdf")

        if not txt.strip():
            st.markdown('<div class="error-box">Could not extract text</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">PDF processed</div>', unsafe_allow_html=True)

            st.write(f"OCR Confidence: {conf}%")
            st.text_area("Extracted text", txt[:2000], height=200)

            st.subheader("Ask about this PDF")

            user_q = st.text_input("Your question")

            if st.button("Ask PDF"):
                if user_q:
                    combined_input = txt + "\n\n" + user_q

                    res = run_agent(combined_input)

                    if "followup" in res:
                        st.warning(res["followup"])
                    else:
                        st.write(res["result"])

                    st.subheader("Logs")
                    st.write(res["logs"])

    st.markdown('</div>', unsafe_allow_html=True)



elif mode == "audio":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2>Audio Mode</h2>", unsafe_allow_html=True)

    file = st.file_uploader("Upload Audio")

    if file:
        with open("temp.wav", "wb") as f:
            f.write(file.read())

        txt = get_audio("temp.wav")

        if not txt:
            st.markdown('<div class="error-box">Could not transcribe audio</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">Audio converted to text</div>', unsafe_allow_html=True)

            st.text_area("Transcript", txt, height=200)

            st.subheader("Ask about this Audio")

            user_q = st.text_input("Your question")

            if st.button("Ask Audio"):
                if user_q:
                    combined_input = txt + "\n\n" + user_q

                    res = run_agent(combined_input)

                    if "followup" in res:
                        st.warning(res["followup"])
                    else:
                        st.write(res["result"])

                    st.subheader("Logs")
                    st.write(res["logs"])

    st.markdown('</div>', unsafe_allow_html=True)
