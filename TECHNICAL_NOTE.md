# Riverwood AI Voice Agent – Technical Note

**Submitted by:** Srinath Reddy Chitteti  
**Challenge:** Riverwood AI Voice Agent Internship Challenge  

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend Interface | Streamlit |
| Large Language Model | OpenAI GPT-4o-mini |
| Text-to-Speech | Google Text-to-Speech (gTTS) |
| Speech-to-Text | SpeechRecognition + PyAudio |
| Environment Management | python-dotenv |
| Runtime | Python 3.10+ |

---

## System Overview

1. **Streamlit UI** provides a user-friendly web interface.
2. **Voice Input** allows users to talk directly through the microphone.
3. **GPT-4o-mini** generates contextual and warm replies in Hinglish.
4. **Text-to-Speech (gTTS)** converts the AI reply into natural spoken voice.
5. **Session Memory** preserves conversation history.
6. **Construction Update Simulation** gives random project progress messages.
7. **Environment Variables** protect API keys via `.env`.

---

## Features

- Hinglish conversational tone.
- Text and voice input.
- Human-like speech output.
- Context memory during session.
- Automatic voice trigger after speaking.
- Simulated construction progress updates.
- Riverwood-branded UI with sidebar and history.

---

## Infrastructure Cost Estimate

| Service | Cost (Approx) |
|----------|---------------|
| OpenAI API (GPT-4o-mini) | ~$5/month (light usage) |
| gTTS | Free |
| Streamlit Cloud Hosting | Free Tier |
| SpeechRecognition | Local Processing (Free) |

---

## Possible Improvements

- Replace gTTS with ElevenLabs or Play.ht for higher-quality speech.
- Deploy on Streamlit Cloud or Replit for public access.
- Integrate Twilio for real phone-call support.
- Add persistent memory storage using a database.




