import requests
import streamlit as st

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Book RAG Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Data Engineering Book Assistant")


# =========================================================
# SESSION STATE
# =========================================================

if "access_token" not in st.session_state:
    st.session_state.access_token = None


# =========================================================
# AUTHENTICATION
# =========================================================

st.sidebar.header("🔐 Authentication")

email = st.sidebar.text_input("Email")

password = st.sidebar.text_input(
    "Password",
    type="password",
)

if st.sidebar.button("Login"):

    response = requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    if response.status_code == 200:

        data = response.json()

        st.session_state.access_token = data["access_token"]

        st.sidebar.success("Login successful!")

    else:

        st.sidebar.error(
            f"Login failed: {response.text}"
        )

# =========================================================
# CHECK AUTH
# =========================================================

if not st.session_state.access_token:

    st.warning("Please login first.")

    st.stop()


# =========================================================
# AUTH HEADER
# =========================================================

headers = {
    "Authorization": (
        f"Bearer {st.session_state.access_token}"
    )
}


# =========================================================
# UPLOAD
# =========================================================

st.header("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
)


if uploaded_file:

    if st.button("Index PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf",
            )
        }

        response = requests.post(
            f"{API_URL}/upload/",
            files=files,
            headers=headers,
        )

        if response.status_code == 200:

            data = response.json()

            st.success(data["message"])

            st.info(
                f"""
                File: {data["filename"]}

                Chunks: {data["chunks"]}
                """
            )

        else:

            st.error(
                f"Upload failed: {response.text}"
            )


# =========================================================
# CHAT
# =========================================================

st.header("💬 Ask Question")

question = st.text_input(
    "Your question"
)


if st.button("Ask"):

    if not question:

        st.warning("Please enter a question.")

    else:

        response = requests.post(
            f"{API_URL}/chat/chat/",
            json={
                "question": question
            },
            headers=headers,
        )

        if response.status_code == 200:

            data = response.json()

            st.subheader("Answer")

            st.write(data["answer"])

            sources = data.get(
                "sources",
                []
            )

            if sources:

                st.subheader(
                    "📚 Page References"
                )

                for source in sources:

                    st.write(
                        f"[{source['reference']}] "
                        f"{source['file_name']} — "
                        f"page {source['page_number']} "
                        f"(chunk {source['chunk_number']}, "
                        f"match {source['score']:.0%})"
                    )

        elif response.status_code == 401:

            st.error(
                "Authentication failed. "
                "Please login again."
            )

            st.session_state.access_token = None

        else:

            st.error(
                f"Chat failed: {response.text}"
            )