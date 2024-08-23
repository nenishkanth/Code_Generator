import os
import requests
import re
import json
import streamlit as st
import base64

# API key for the external service
apiKey = "1480eeed-e842-4a42-9a37-0065d97b523b"

def get_img_as_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("code.jpg")

page_bg_img = f"""

<style>
[data-testid="stAppViewContainer"] > .main {{
background-image :url("data:image/png;base64,{img}");
background-size : cover;
}}
[data-testid="stHeader"]{{
background:rgba(0,0,0,0);
}}
</style>

"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to call the API with the user's input
def apiFunction(usersInputObj):
    inputsArray = [
        {"id": "{input_1}", "label": "Enter problem statement", "type": "text"},
        {"id": "{input_2}", "label": "Enter programming language", "type": "text"}
    ]
    
    # Create the prompt based on user input
    prompt = "Generate code for this problem statement {input_1} in this programming language {input_2}"
    filesData, textData = {}, {}

    # Replace placeholders in the prompt with actual user input
    for inputObj in inputsArray:
        inputId = inputObj['id']
        if inputObj['type'] == 'text':
            prompt = prompt.replace(inputId, usersInputObj[inputId])
        elif inputObj['type'] == 'file':
            path = usersInputObj[inputId]
            file_name = os.path.basename(path)
            with open(path, 'rb') as f:
                filesData[inputId] = f

    # Prepare the data payload for the API request
    textData['details'] = json.dumps({
        'appname': 'generate code',
        'prompt': prompt,
        'documentId': 'no-embd-type',
        'appId': '66c8a7b064d827b744a2a114',
        'memoryId': '',
        'apiKey': apiKey
    })

    # Make the API request
    response = requests.post('https://apiappstore.guvi.ai/api/output', data=textData, files=filesData)
    output = response.json()

    return output['output']

# Streamlit app setup
st.title("Code Generator")

# User inputs through Streamlit text inputs
problem_statement = st.text_input("Enter the problem statement you want to solve:")
programming_language = st.text_input("Enter the desired programming language:")

# Button to trigger the API call
if st.button("Generate Code"):
    usersInputObj = {
        '{input_1}': problem_statement,
        '{input_2}': programming_language,
    }
    
    # Call the API function and get the result
    output = apiFunction(usersInputObj)
    
    # Replace localhost URLs with the correct API endpoint
    url_regex = r'http://localhost:7000/'
    replaced_string = re.sub(url_regex, 'https://apiappstore.guvi.ai/', output)
    
    # Display the output in the Streamlit app
    st.write(replaced_string)
