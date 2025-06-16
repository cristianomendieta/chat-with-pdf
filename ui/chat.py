import os

import requests
import streamlit as st

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")


def upload_documents(files):
    """Upload PDF documents to the backend"""
    try:
        files_data = []
        for file in files:
            # Reset file pointer to beginning
            file.seek(0)
            files_data.append(
                ("files", (file.name, file.getvalue(), "application/pdf"))
            )

        response = requests.post(f"{API_BASE_URL}/api/v1/documents", files=files_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error uploading documents: {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            st.error(f"Response status: {e.response.status_code}")
            st.error(f"Response content: {e.response.text}")
        return None


def ask_question(question: str):
    """Ask a question to the backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/question", json={"question": question}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error asking question: {str(e)}")
        return None


def check_backend_status():
    """Check if backend is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def main():
    st.set_page_config(page_title="Chat with PDF", page_icon="📄", layout="wide")

    st.title("📄 Chat with PDF using AI")

    # Check backend status
    if check_backend_status():
        st.success("✅ Backend is connected!")
    else:
        st.error(
            "❌ Backend is not available. Please check if the backend service is running."
        )
        st.stop()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type="pdf",
            accept_multiple_files=True,
            help="Upload one or more PDF files to chat with",
        )

        if uploaded_files:
            st.write(f"📄 {len(uploaded_files)} file(s) uploaded:")
            for file in uploaded_files:
                st.write(f"- {file.name} ({file.size} bytes)")

            if st.button("📤 Upload Documents"):
                with st.spinner("Uploading documents..."):
                    result = upload_documents(uploaded_files)
                    if result:
                        st.success(f"✅ {result['message']}")
                    else:
                        st.error(
                            "❌ Failed to upload documents. Check the logs above for details."
                        )

        if st.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.header("💬 Chat Interface")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "references" in message and message["references"]:
                with st.expander("📚 Sources"):
                    for reference in message["references"]:
                        st.write(f"- {reference}")

    # Chat input
    if prompt := st.chat_input("Ask a question about your PDFs..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = ask_question(prompt)

                if response_data:
                    ai_response = response_data.get(
                        "answer", "Sorry, I couldn't process your request."
                    )
                    references = response_data.get("references", [])

                    st.markdown(ai_response)

                    if references:
                        with st.expander("📚 Sources"):
                            for reference in references:
                                st.write(f"- {reference}")

                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": ai_response,
                            "references": references,
                        }
                    )
                else:
                    error_msg = "Sorry, there was an error processing your request. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )


if __name__ == "__main__":
    main()
