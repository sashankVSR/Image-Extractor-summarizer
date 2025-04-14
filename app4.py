import streamlit as st
import pytesseract
from PIL import Image

# Streamlit app title
st.title("Image Text Extractor & Summarizer")

# Image upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    try:
        # Load and display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Extract text using Tesseract
        with st.spinner("Extracting text..."):
            extracted_text = pytesseract.image_to_string(image)

        if extracted_text.strip():
            st.write("**Extracted Text:**")
            st.write(extracted_text)

            # Summarize the extracted text
            with st.spinner("Generating summary..."):
                # Simple sentence splitting (split on periods, clean up)
                sentences = [s.strip() for s in extracted_text.split('.') if s.strip()]
                
                # Define stopwords manually (small set for simplicity)
                stop_words = {
                    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
                    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
                    'to', 'was', 'were', 'will', 'with'
                }

                # Calculate word frequency
                word_freq = {}
                for word in extracted_text.lower().split():
                    # Remove basic punctuation for cleaner words
                    word = word.strip('.,!?()[]{}":;').strip()
                    if word and word not in stop_words and word.isalnum():
                        word_freq[word] = word_freq.get(word, 0) + 1

                # Score sentences based on word frequency
                sentence_scores = {}
                for sentence in sentences:
                    score = 0
                    for word in sentence.lower().split():
                        word = word.strip('.,!?()[]{}":;').strip()
                        if word in word_freq:
                            score += word_freq[word]
                    sentence_scores[sentence] = score

                # Select top 2 sentences for summary (adjustable)
                summary_sentences = sorted(
                    sentence_scores, key=sentence_scores.get, reverse=True
                )[:2]
                summary = ". ".join(summary_sentences) + ("." if summary_sentences else "")

                st.write("**Summary:**")
                st.write(summary if summary else "No meaningful summary could be generated.")
        else:
            st.warning("No text detected in the image.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload an image to begin.")