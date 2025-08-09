import streamlit as st
import random
import pyperclip
import webbrowser
from streamlit.components.v1 import html


if "daziyo" not in st.session_state:
    st.session_state.daziyo = {}

st.title("Dazyio")
st.subheader("Daziyo is a language spoken by a fictonal group that lives under water - merpeople. " \
"Hence, its characteristics allow the maximal intellegibility under water (atleast in theory)")

consonants = ["d", "n", "r", "l", "ð", "ʒ"]
vowels = ["i", "y", "ɘ", "ɵ", "ɤ", "o", "ʌ", "ɔ", "ɑ", "ɒ"]
syllablesInWord = [1, 2, 3]
special_chars = set('!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

def replace_second_consonants(word):
    consonant_counts = {}
    result = ""
    for char in word:
        if char.isalpha() and char not in vowels:
            consonant_counts[char] = consonant_counts.get(char, 0) + 1
            if consonant_counts[char] == 2 and char in ["d", "n", "r", "l"]:
                result += "||"
                continue
            elif consonant_counts[char] == 2 and char == "ʒ":
                result += "!"
                continue
            elif consonant_counts[char] == 2 and char == "ð":
                result += "|"
                continue
        result += char
    return result

def make_CV():
    return random.choice(consonants) + random.choice(vowels)
def make_VCV():
    return random.choice(vowels) + random.choice(consonants) + random.choice(vowels)
def make_VV():
    return random.choice(vowels) + random.choice(vowels)

syllableGenerators = [make_CV, make_VCV, make_VV]

ʒReplace = ("zh", "s", "g")
iReplace = ("ee", "e")
yReplace = ("ü", "u") 
ɵReplace = ("ur", "ir")
oReplace = ("o", "oa", "ow")
ɔReplace = ("aw", "or")   
ɑReplace = ("ah", "a")  

def orthographic_form(IPAtranscription): 
    transcriptionWithSyllableBorders = IPAtranscription.replace("ð", "th").replace("ʒ", random.choice(ʒReplace)).replace("i", random.choice(iReplace)).replace("y", random.choice(yReplace)).replace("ɘ", "uh").replace("ɵ", random.choice(ɵReplace)).replace("ɤ", "uh").replace("o", random.choice(oReplace)).replace("ʌ", "u").replace("ɔ", random.choice(ɔReplace)).replace("ɑ", random.choice(ɑReplace)).replace("ɒ", "o")
    result = transcriptionWithSyllableBorders.replace(".", "").replace("||", "").replace("!", "").replace("|", "").replace("/", "")
    return result


# DAZIYO now RETURNS the message instead of writing directly
def DAZIYO():
    englishWord = st.session_state.englishWord # we save it under englishWord so we do not have to type st.sessions_state.englishWord everytime we use it in the rest of the script
    if not englishWord:
        return "Please enter a word." 
    elif englishWord in special_chars: 
        return "you have just entered a special character - how am I supposed to translate this?"
    elif englishWord.isdigit():
        return "you have just entered a number into a translator, you think you funny?"
    elif englishWord in st.session_state.daziyo:
        return englishWord + " " + "in daziyo means" + " " + st.session_state.daziyo[englishWord][0] + ", its phonemic transcription is" + " " + st.session_state.daziyo[englishWord][1]
    else:
        while True:
            syllablesNumberNewWord = random.choice(syllablesInWord)
            syllablesStructureNewWord = [
                random.choice(syllableGenerators)() for _ in range(syllablesNumberNewWord)
            ]
            daziyoTranslation = '.'.join(syllablesStructureNewWord)
            daziyoTranslation2 = random.choice(consonants) + daziyoTranslation 
            daziyoFinal = "/" + replace_second_consonants(daziyoTranslation2) + "/"
            if daziyoFinal not in st.session_state.daziyo.values():
                break

        st.session_state.daziyo[englishWord] = [orthographic_form(daziyoFinal), daziyoFinal]
        return englishWord + " " + "in daziyo means" + " " + st.session_state.daziyo[englishWord][0] + ", its phonemic transcription is" + " " + st.session_state.daziyo[englishWord][1]

# --- FORM: capture the boolean submitted, not on_click ---
with st.form(key="my_form"):
    st.text_input("Enter an English word", key="englishWord") # this is the streamlit equivalent of englishWord = input("Enter an English Word")
    submitted = st.form_submit_button("translate")

# placeholder below the form 
output_box = st.empty()

# run AFTER the form and display result below the form. Why is it after the output_box placeholder? because we have to initalize output_box before we can use it
if submitted:
    message = DAZIYO()
    output_box.write(message) 



if 'open_count' not in st.session_state:
    st.session_state.open_count = 0

def copyToIPA():
    ipa = st.session_state.daziyo[st.session_state.englishWord][1]
    js_code = f"""
    <script>
    navigator.clipboard.writeText("{ipa}").then(() => {{
        window.open("https://ipa-reader.com", "new_window_{st.session_state.open_count}", "popup").focus();
    }});
    </script>
    """
    st.session_state.open_count += 1
    html(js_code, height=0, width=0)

with st.form(key="my_secondform"):
    st.form_submit_button("copy and go", on_click=copyToIPA)


