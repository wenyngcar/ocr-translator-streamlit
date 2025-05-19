import streamlit as st
from language import languages
from PIL import Image
import time
from translate import translate_text
from imageProcessing import process_image
import asyncio

# Initialize
translated_text = ""

st.markdown("# :violet[Snap & Translate]")
st.markdown("New here? See quick instructions **:violet[below.]**")

container = st.container(border=True)

with st.container(border=True):
    input_image = st.file_uploader(
        "Upload image", type=["png", "jpg", "jpeg"])

    # Display the image if uploaded.
    if input_image is not None:
        image = Image.open(input_image)
        st.image(image, use_container_width=True)

        # Save the input image for cv2 processing.
        image.convert("RGB").save("./images/uploaded_image.jpg")

    with st.form("translate", border=False):

        btn_left, btn_middle, btn_right = st.columns(
            [3, 1, 1], vertical_alignment="bottom")
        with btn_left:
            option_language = st.selectbox(
                "Select language of image",
                ["Afrikaans", "Amharic", "Arabic", "Assamese", "Azerbaijani", "Azerbaijani (Cyrillic)", "Belarusian", "Bengali", "Tibetan", "Bosnian", "Breton", "Bulgarian", "Catalan", "Cebuano", "Czech", "Chinese (Simplified)", "Chinese (Simplified, Vertical)", "Chinese (Traditional)", "Chinese (Traditional, Vertical)", "Cherokee", "Corsican", "Welsh", "Danish", "German", "Dhivehi", "Dzongkha", "Greek", "English", "Middle English", "Esperanto", "Math / Equation", "Estonian", "Basque", "Faroese", "Persian", "Filipino", "Finnish", "French", "Frankish", "Middle French", "Western Frisian", "Scottish Gaelic", "Irish", "Galician", "Ancient Greek", "Gujarati", "Haitian Creole", "Hebrew", "Hindi", "Croatian", "Hungarian", "Armenian", "Inuktitut", "Indonesian", "Icelandic", "Italian", "Old Italian", "Javanese", "Japanese", "Japanese (Vertical)",
                 "Kannada", "Georgian", "Old Georgian", "Kazakh", "Khmer", "Kyrgyz", "Kurmanji (Kurdish)", "Korean", "Korean (Vertical)", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Malayalam", "Marathi", "Macedonian", "Maltese", "Mongolian", "Maori", "Malay", "Burmese", "Nepali", "Dutch", "Norwegian", "Occitan", "Odia (Oriya)", "Orientation and Script Detection", "Punjabi", "Polish", "Portuguese", "Pashto", "Quechua", "Romanian", "Russian", "Sanskrit", "Sinhala", "Slovak", "Slovenian", "Sindhi", "Script and Number Detection", "Spanish", "Old Spanish", "Albanian", "Serbian", "Serbian (Latin)", "Sundanese", "Swahili", "Swedish", "Syriac", "Tamil", "Tatar", "Telugu", "Tajik", "Thai", "Tigrinya", "Tongan", "Turkish", "Uyghur", "Ukrainian", "Urdu", "Uzbek", "Uzbek (Cyrillic)", "Vietnamese", "Yiddish", "Yoruba"],
                index=None,
                placeholder="Select a language",
                accept_new_options=False,
            )
        with btn_middle:
            option_weight = st.selectbox(
                "Select weight",
                ["Heavy", "Thin"],
                index=None,
                placeholder="Select weight",
                accept_new_options=False,
            )

        with btn_right:
            submitted = st.form_submit_button("Translate Image")

    if submitted:
        if input_image is None:
            st.warning("Please upload an image.")
        elif option_language is None:
            st.warning("Please select a language.")
        elif option_weight is None:
            st.warning("Please select a weight.")
        else:
            progress_text = "Please wait while the image is being translated."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)

            # If the image font is heavy, no need to go for preprocessing.
            if option_weight == "Heavy":
                translated_text = asyncio.run(translate_text(
                    input_image, languages[option_language])).text

            # If the image is thin, goes to image processing.
            else:
                preprocess_image = process_image()
                translated_text = asyncio.run(translate_text(
                    "./images/processed_image.jpg", languages[option_language])).text

            my_bar.empty()
            if len(translated_text) > 0:
                st.success("Traslated Successfully")
            else:
                st.error(
                    "Error processing the image. Please make sure you have selected the correct language and weight. Or try another image.")


with st.container(border=True):
    st.markdown("### :violet[Translation]")

    # If translated text is not empty.
    if len(translated_text) > 0:
        st.markdown(f"\"{translated_text}\"")
    else:
        st.markdown("Translated text goes here.")

st.write("")
st.write("")
st.markdown("## :violet[Instructions]")
st.markdown("#### 1. Upload an image of a text of any language.  ")
instruction_image1 = Image.open("./images/instruction1.png")
st.image(instruction_image1, use_container_width=True)

st.markdown("#### 2. Select the correct language.  ")
st.markdown(
    " Some languages are read from \"top\" to \"bottom\". Make sure you select the correct one.")
ins2left, ins2right = st.columns(2, vertical_alignment="center")
instruction_image2 = Image.open("./images/instruction2.png")
instruction_image2_wrong = Image.open("./images/instruction2-wrong.png")
instruction_image2_correct = Image.open("./images/instruction2-correct.png")
with ins2left:
    st.image(instruction_image2)
with ins2right:
    st.markdown(":red-badge[❌ Wrong]")
    st.image(instruction_image2_wrong)
    st.markdown(":green-badge[✅ Correct]")
    st.image(instruction_image2_correct)
st.markdown(
    "#### 3. Select the correct weight. ")
st.markdown("If both does not result to error, try adjusting and compare which weight produces more accurate result.")
st.write("")
st.write("")
st.markdown("""
    <div style="background-color:#f3a362; padding: 10px 20px; border-radius: 10px;">
        <h6 style="color:white;">Notes</h6>
        <p style="color:white;">The translator cannot properly detect image with unclear background, or when too much color and objects is present, or when an image is skewed or rotated.</p>
    </div>
""", unsafe_allow_html=True)
