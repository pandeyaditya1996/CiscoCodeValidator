import streamlit as st
from validator import CodeValidator
from embeddings import CodeEmbeddings
import os

def load_sample_code():
    samples = {}
    samples_dir = "../data/c_samples"
    for file in os.listdir(samples_dir):
        if file.endswith('.c'):
            with open(os.path.join(samples_dir, file), 'r') as f:
                samples[file] = f.read()
    return samples

def main():
    st.title("C Code Validation Chatbot")
    
    if 'validator' not in st.session_state:
        # Initialize embeddings and validator
        embedder = CodeEmbeddings()
        samples = load_sample_code()
        vector_store = embedder.create_vector_store(samples)
        st.session_state.validator = CodeValidator(vector_store)
    
    st.write("Enter the original and modified code to validate the changes:")
    
    original_code = st.text_area("Original Code:", height=200)
    modified_code = st.text_area("Modified Code:", height=200)
    
    if st.button("Validate Changes"):
        if original_code and modified_code:
            result = st.session_state.validator.validate_change(
                original_code, modified_code
            )
            
            st.write("### Analysis Result:")
            st.write(result)
        else:
            st.error("Please enter both original and modified code.")

if __name__ == "__main__":
    main()
