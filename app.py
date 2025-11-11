import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from gtts import gTTS
from io import BytesIO
from datetime import datetime
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("Add your OPENAI_API_KEY to a .env file.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="Riverwood AI Voice Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    body { background-color: #f8fafc; font-family: 'Poppins', sans-serif; }
    .title { text-align: center; font-size: 2.2em; font-weight: 700; color: #1e3a8a; margin-bottom: 0.3em; }
    .subtitle { text-align: center; font-size: 1.1em; color: #475569; margin-bottom: 1.5em; }
    .chat-bubble-user {
        background-color: #e2e8f0; color: #1e293b; padding: 10px 15px;
        border-radius: 15px; margin-bottom: 8px; margin-left: auto;
        width: fit-content; max-width: 70%;
    }
    .chat-bubble-ai {
        background-color: #1e3a8a; color: white; padding: 10px 15px;
        border-radius: 15px; margin-bottom: 8px; margin-right: auto;
        width: fit-content; max-width: 70%;
    }
    .footer {
        font-size: 0.8em; color: #64748b; text-align: center; margin-top: 3em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Riverwood AI Voice Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>“Namaste, chai pee li?” — Meet Miss Riverwood, your friendly AI assistant!</div>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://riverwoodindia.com/assets/images/logo.png", use_container_width=True)
    st.markdown("### Construction Updates")
    updates = [
        "Road leveling completed at Sector 7 site.",
        "Clubhouse structure is 80% done.",
        "Landscaping and plantation have begun.",
        "Electrical wiring Phase 2 starts next week.",
        "Drainage inspection successfully completed."
    ]
    for update in updates:
        st.markdown(f"- {update}")
    st.markdown("---")
    st.markdown("**Developed for:** Riverwood AI Voice Agent Challenge")
    st.markdown("**By:** Srinath Reddy Chitteti")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

def get_construction_update():
    updates = [
        "Sector 7 site par road leveling complete ho gaya hai.",
        "Clubhouse structure ka kaam 80% tak complete ho chuka hai.",
        "Landscaping team ne kal se plantation start kar diya hai.",
        "Electrical wiring ka phase 2 next week se start hoga.",
        "Drainage system ka inspection successfully complete ho gaya hai."
    ]
    return updates[datetime.now().day % len(updates)]

def generate_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": (
            "You are Miss Riverwood, an AI voice agent for Riverwood Projects LLP — a real estate developer based in Haryana, India. "
            "You are warm, cheerful, and speak in Hinglish (English + Hindi mix). "
            "You represent Riverwood Estate — a 25-acre township project in Sector 7, Kharkhauda, near the IMT Kharkhauda industrial zone, "
            "home to the Maruti Suzuki and Suzuki Two-Wheeler mega plants. "
            "Founders are Sanyam Chugh and Tarvinder Singh — combining traditional real estate experience with modern AI innovation. "
            "Riverwood builds homes with the philosophy: 'We don’t just build homes. We build stories.' "
            "Your job is to sound friendly, remember past chats, and share updates or insights about Riverwood when asked."
        )}
    ]
    for u, a in st.session_state.conversation:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

def speak_text(text: str) -> BytesIO | None:
    try:
        tts = gTTS(text=text, lang="hi")
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)
        return audio
    except Exception:
        st.warning("Couldn't generate voice output.")
        return None

def listen_to_user() -> str:
    if not VOICE_AVAILABLE:
        st.warning("Voice input not available — install 'speech_recognition' and 'pyaudio'.")
        return ""
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            st.info("Listening... please speak now.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=6)
        text = recognizer.recognize_google(audio, language="en-IN")
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Couldn't understand your voice. Try again.")
        return ""
    except sr.RequestError:
        st.error("Speech recognition service unavailable.")
        return ""

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Type your message:",
        value=st.session_state.pending_input,
        placeholder="Enter your query here",
        key="text_input"
    )

with col2:
    if st.button("Speak"):
        spoken_text = listen_to_user()
        if spoken_text:
            st.session_state.pending_input = spoken_text
            st.session_state["trigger_send"] = True
            if hasattr(st, "rerun"):
                st.rerun()
            else:
                st.experimental_rerun()

if "trigger_send" in st.session_state and st.session_state["trigger_send"]:
    user_input = st.session_state.pending_input
    if user_input:
        if any(word in user_input.lower() for word in ["update", "construction", "progress"]):
            bot_reply = get_construction_update()
        else:
            bot_reply = generate_response(user_input)
        st.session_state.conversation.append((user_input, bot_reply))
        audio_data = speak_text(bot_reply)
        st.session_state.pending_input = ""
        st.session_state["trigger_send"] = False
        st.markdown(f"<div class='chat-bubble-ai'>{bot_reply}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble-user'>{user_input}</div>", unsafe_allow_html=True)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")

elif st.button("Send") and user_input.strip():
    if any(word in user_input.lower() for word in ["update", "construction", "progress"]):
        bot_reply = get_construction_update()
    else:
        bot_reply = generate_response(user_input)
    st.session_state.conversation.append((user_input, bot_reply))
    audio_data = speak_text(bot_reply)
    st.session_state.pending_input = ""
    st.markdown(f"<div class='chat-bubble-ai'>{bot_reply}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-user'>{user_input}</div>", unsafe_allow_html=True)
    if audio_data:
        st.audio(audio_data, format="audio/mp3")

if st.session_state.conversation:
    st.markdown("---")
    st.markdown("### Conversation History")
    for user_msg, ai_msg in reversed(st.session_state.conversation):
        st.markdown(f"<div class='chat-bubble-ai'>{ai_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble-user'>{user_msg}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>© 2025 Riverwood Projects LLP | Built for AI Voice Agent Challenge</div>", unsafe_allow_html=True)
