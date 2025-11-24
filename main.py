import streamlit as st
import easyocr
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
import re

# --- CONFIGURATION ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

# --- HELPER FUNCTIONS ---

def extract_text_easyocr(image):
    image_np = np.array(image)
    result = reader.readtext(image_np, detail=0, paragraph=True)
    return "\n".join(result)

def smart_parse_text(text):
    """
    Parses text and returns a flat dictionary of fields.
    """
    data = {}
    text_lower = text.lower()
    
    # 1. Detect Type
    if "income tax" in text_lower or re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text):
        doc_type = "PAN Card"
    elif "male" in text_lower and re.search(r"\d{4}\s\d{4}\s\d{4}", text):
        doc_type = "Aadhaar Card"
    elif "passport" in text_lower:
        doc_type = "Passport"
    else:
        doc_type = "General ID"
        
    data['Document Type'] = doc_type

    # 2. Extract Fields based on Type
    if doc_type == "PAN Card":
        pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
        data['ID Number'] = pan_match.group(0) if pan_match else None
        
        dob_match = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", text)
        data['DOB'] = dob_match.group(0) if dob_match else None
        
        
        data['Name'] = "Manual Check Needed" 

    elif doc_type == "Aadhaar Card":
        uid_match = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
        data['ID Number'] = uid_match.group(0) if uid_match else None
        
        if "female" in text_lower: data['Gender'] = "Female"
        elif "male" in text_lower: data['Gender'] = "Male"
        
        yob_match = re.search(r"Year of Birth\s*:\s*(\d{4})", text)
        if yob_match: data['DOB'] = yob_match.group(1)

    elif doc_type == "Passport":
        
        pp_match = re.search(r"[A-Z][0-9]{7}", text)
        data['ID Number'] = pp_match.group(0) if pp_match else None
        
        dob_match = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", text)
        data['DOB'] = dob_match.group(0) if dob_match else None

    else:
        
        id_match = re.search(r"\b[A-Z0-9]{6,12}\b", text)
        data['ID Number'] = id_match.group(0) if id_match else "Not Found"

    return data


def main():
    st.set_page_config(page_title="Formatted Extractor", layout="wide")
    st.title("📄 All Document Extractor")
    st.markdown("### Uploaded Data")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    uploaded_file = st.file_uploader("Upload Document (PAN, Aadhaar, etc.)", type=["jpg", "png", "jpeg"])

    if st.button("Process Document"):
        if uploaded_file:
            with st.spinner("Reading & Formatting..."):
              
                image = Image.open(uploaded_file)
                raw_text = extract_text_easyocr(image)
                
              
                extracted_data = smart_parse_text(raw_text)

                record = {
                    "File Name": uploaded_file.name,
                    "Timestamp": datetime.now().strftime("%H:%M:%S")
                }           

                record.update(extracted_data) 
                
                st.session_state['history'].append(record)
                st.success("Added to table!")

    # --- DISPLAY TABLE ---
    if st.session_state['history']:
      
        df = pd.DataFrame(st.session_state['history'])
        
       
        cols = ['File Name', 'Document Type', 'ID Number', 'DOB']
       
        other_cols = [c for c in df.columns if c not in cols and c != "Timestamp"]
        final_order = cols + other_cols + ['Timestamp']
        
     
        final_order = [c for c in final_order if c in df.columns]
        
      
        st.dataframe(df[final_order], use_container_width=True)
    else:
        st.info("No data extracted yet. Upload a file above.")

if __name__ == "__main__":
    main()