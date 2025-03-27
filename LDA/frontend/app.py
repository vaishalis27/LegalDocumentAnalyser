import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/api/upload-pdf"

st.set_page_config(page_title="Legal Document Analyzer", layout="wide")

st.title("📑 AI-Powered Legal Document Analyzer")
st.markdown("Upload a legal PDF to get a summary and clause insights.")

uploaded_file = st.file_uploader("Upload your legal PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        with st.spinner("Analyzing document..."):
            # Log file information
            st.write(f"File name: {uploaded_file.name}")
            st.write(f"File type: {uploaded_file.type}")
            st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")

            # Send request to backend
            # Create a tuple with the file name and file object
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            
            # Add headers to ensure proper content type
            headers = {
                "Accept": "application/json"
            }
            
            response = requests.post(API_URL, files=files, headers=headers)

            # Log response information
            st.write(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                st.subheader("📌 Summary")
                st.write(result.get("summary", "No summary available"))

                if "entities" in result and result["entities"]:
                    st.subheader("🔍 Detected Entities / Clauses")
                    for ent in result["entities"]:
                        st.markdown(f"- **{ent['entity']}**: _{ent['word']}_ (Score: {ent['score']})")
                else:
                    st.warning("No Legal Entities Detected.")

                with st.expander("📝 Raw Text Preview"):
                    st.text_area("Document Text", result.get("raw_text", ""), height=200)

            else:
                # Handle error response
                try:
                    error_data = response.json()
                    error_message = error_data.get("detail", "Unknown error occurred")
                    st.error(f"Error: {error_message}")
                except json.JSONDecodeError:
                    st.error(f"Error: {response.text}")
                
                # Show debug information
                with st.expander("Debug Information"):
                    st.write("Response Headers:")
                    st.json(dict(response.headers))
                    st.write("Response Content:")
                    st.text(response.text)
                    st.write("Request Headers:")
                    st.json(dict(response.request.headers))
                    st.write("Request Files:")
                    st.json(dict(response.request.files))

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        with st.expander("Debug Information"):
            st.write("Error details:")
            st.exception(e)
