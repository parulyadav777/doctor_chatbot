# app.py
import streamlit as st
from backend import chat_with_model
from ai_booking import handle_user_message
import backend
print("BACKEND FILE USED:", backend.__file__)
from backend import (
    authenticate_user, create_user,
    load_user_chat_sessions, load_chat_messages,
    save_chat_session_with_messages, update_chat_session_messages
)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🩺 AI Health Assistant")

    # ---------- AUTH ----------
    if not st.session_state.user:
        choice = st.selectbox("Choose Action", ["Login", "Sign Up"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Submit", use_container_width=True):
            if choice == "Login":
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state.user = {
                        "username": username,
                        "id": user_data["id"],
                        "is_admin": user_data["is_admin"]
                    }
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                if create_user(username, password):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Username already exists.")
        st.stop()

    # ---------- USER INFO ----------
    st.success(f"Welcome, {st.session_state.user['username']}")
    st.divider()

    # ---------- NAVIGATION ----------
    def nav_button(label, page):
        active = st.session_state.page == page
        if st.button(
            label,
            use_container_width=True,
            type="primary" if active else "secondary"
        ):
            st.session_state.page = page
            st.rerun()

    nav_button("🏠 Home", "Home")
    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "Home"
        st.rerun()

# =========================
# MAIN CONTENT
# =========================

# ---------- HOME PAGE ----------
if st.session_state.page == "Home":
    st.markdown("""
    <h1 style="text-align:center;">🩺 AI Health Assistant</h1>
    <p style="text-align:center; color:#9CA3AF;">
    Your personal AI-powered medical guidance system
    </p>
    <hr>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("💬 **Medical Chat**\n\nUse the **Chat page** from the sidebar.")
    with col2:
        st.success("👨‍⚕️ **Doctor Guidance**\n\nGet specialization suggestions based on symptoms.")
    with col3:
        st.warning("📜 **Chat History**\n\nAvailable inside the Chat section.")

    st.markdown("""
    ### ⚠️ Disclaimer
    This assistant provides **guidance only** and is **not a replacement for a licensed doctor**.
    """)

    # Initialize chat state
    if "home_chat" not in st.session_state:
        st.session_state.home_chat = []

    # Input box
    user_input = st.text_input(
        "Type your question or appointment request:",
        placeholder="e.g. Book an appointment with cardiologist",
        key="home_input"
    )

    # Send button
    if st.button("Send"):
        if user_input.strip():
            # Save user message
            st.session_state.home_chat.append({
                "role": "user",
                "content": user_input
            })

            # AI response using handle_user_message (books appointments too)
            with st.spinner("Doctor is thinking..."):
                reply = handle_user_message(user_input, st.session_state.user["id"])

            st.session_state.home_chat.append({
                "role": "assistant",
                "content": reply
            })

            # Clear input safely
            st.session_state.pop("home_input", None)
            st.rerun()

    # Display chat messages
    for msg in st.session_state.home_chat:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# ---------- AI CHAT PAGE ----------
elif st.session_state.page == "AI Chat":
    st.title("💬 AI Health Assistant Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a medical question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Doctor is thinking..."):
                reply = chat_with_model(prompt)
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
