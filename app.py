import streamlit as st
import os
from openai import OpenAI
from utils import build_repo_context

# --- UI Configuration ---
st.set_page_config(page_title="Sovereign Code Auditor", page_icon="🛡️", layout="wide")

st.title("🛡️ Nemotron 3 Super: Sovereign Code Auditor")
st.markdown("""
Deep reasoning security agent powered by **NVIDIA Nemotron 3 Super (120B)**. 
Analyzes entire repositories for vulnerabilities and architectural flaws.
""")

# --- API Key Management (Local vs Cloud) ---
# Try to get key from HF Secrets or Environment variables
api_key_env = os.environ.get("NVIDIA_API_KEY")

with st.sidebar:
    st.header("Settings")
    if api_key_env:
        st.success("API Key detected from Secrets")
        api_key = api_key_env
    else:
        api_key = st.text_input("Enter NVIDIA API Key", type="password")
        st.info("Get your key at build.nvidia.com")

    project_path = st.text_input("Local Repository Path", placeholder="/home/user/my-project")
    
    st.divider()
    st.caption("Model: nvidia/nemotron-3-super-120b")
    st.caption("Context Window: 1,000,000 Tokens")

# --- Execution Logic ---
if st.button("🚀 Start Deep Audit"):
    if not api_key:
        st.error("Please provide an API Key.")
    elif not project_path:
        st.error("Please provide a project path.")
    else:
        try:
            # 1. Build Context
            with st.spinner("Processing repository..."):
                full_context = build_repo_context(project_path)
            
            # 2. Connect to NVIDIA NIM API
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )

            # 3. AI Reasoning Request
            with st.spinner("Nemotron is reasoning over your codebase..."):
                response = client.chat.completions.create(
                    model="nvidia/nemotron-3-super-120b",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a Senior Cybersecurity Auditor. Provide a detailed security report in Markdown. Identify vulnerabilities, logic errors, and suggest architectural improvements."
                        },
                        {"role": "user", "content": f"Analyze this codebase:\n\n{full_context}"}
                    ],
                    temperature=0.1
                )
                
                report = response.choices[0].message.content

            # 4. Results
            st.success("Audit Complete!")
            st.markdown("### 📊 Security & Architecture Report")
            st.markdown(report)
            
            st.download_button(
                label="Download Report as Markdown",
                data=report,
                file_name="security_audit_report.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# --- Footer ---
st.divider()
st.center = st.caption("Sovereign AI Portafolio Project - 2026")
