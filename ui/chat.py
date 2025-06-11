import streamlit as st
import requests
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:80")

def call_chat_api(message: str):
    """Call the backend chat API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/chat",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {str(e)}")
        return None

def check_backend_status():
    """Check if backend is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def main():
    st.set_page_config(
        page_title="Chat with PDF",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Chat with PDF using AI")
    
    # Check backend status
    if check_backend_status():
        st.success("✅ Backend is connected!")
    else:
        st.error("❌ Backend is not available. Please check if the backend service is running.")
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
            help="Upload one or more PDF files to chat with"
        )
        
        if uploaded_files:
            st.write(f"📄 {len(uploaded_files)} file(s) uploaded:")
            for file in uploaded_files:
                st.write(f"- {file.name}")
        
        if st.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source}")
    
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
                response_data = call_chat_api(prompt)
                
                if response_data:
                    ai_response = response_data.get("response", "Sorry, I couldn't process your request.")
                    sources = response_data.get("sources", [])
                    
                    st.markdown(ai_response)
                    
                    if sources:
                        with st.expander("📚 Sources"):
                            for source in sources:
                                st.write(f"- {source}")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_response,
                        "sources": sources
                    })
                else:
                    error_msg = "Sorry, there was an error processing your request. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()