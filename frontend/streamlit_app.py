import requests
import streamlit as st

# API_URL = os.getenv(
#     "API_URL",
#     "http://api:8000",
# )

# Use this for local testing; change it to "http://api:8000" when using Docker.
API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Book RAG Assistant",
    page_icon="📚",
    layout="wide",
)


st.title("📚 Data Engineering Book Assistant")


st.write("Ask questions from your uploaded books")


# -------------------------
# Upload Section
# -------------------------

st.header("Upload Document")


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
)


if uploaded_file:
    if st.button("Index PDF"):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

        response = requests.post(
            f"{API_URL}/upload/",
            files=files,
        )

        if response.status_code == 200:
            data = response.json()

            st.success(data["message"])

            st.info(
                f"""
                File: {data["filename"]}

                Chunks:
                {data["chunks"]}
                """
            )

        else:
            st.error("Upload failed")


# -------------------------
# Chat Section
# -------------------------

st.header("Ask Question")


question = st.text_input("Your question")


if st.button("Ask"):
    if question:
        response = requests.post(f"{API_URL}/chat/chat/", json={"question": question})

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]

            st.subheader("Answer")

            st.write(answer)

            sources = data.get("sources", [])

            if sources:
                st.subheader("Page References")

                for source in sources:
                    st.write(
                        f"[{source['reference']}] {source['file_name']} — page "
                        f"{source['page_number']} "
                        f"(chunk {source['chunk_number']}, "
                        f"match {source['score']:.0%})"
                    )

        else:
            st.error(response.text)
