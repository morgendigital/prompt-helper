import streamlit as st
import openai
import os  # Import os for environment variable management (if needed)

# Function to replace variables in the prompt
def replace_variables(prompt, variables):
    for key, value in variables.items():
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt

# Function to generate a response using OpenAI's API
def generate_response(system_prompt, pre_prompt, prompt, post_prompt):
    full_prompt = f"{system_prompt}\n\n{pre_prompt}\n\n{prompt}\n\n{post_prompt}"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the newer model as specified
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pre_prompt},
            {"role": "user", "content": prompt},
            {"role": "user", "content": post_prompt},
        ]
    )
    return response.choices[0].message.content.strip()

# Initialize OpenAI configurations
def init_openai_config(api_key, base_url=None):
    openai.api_key = api_key
    if base_url:
        openai.base_url = base_url
    # Optional: You can also set default headers here if needed
    # openai.default_headers = {"x-foo": "true"}

# Streamlit app
def main():
    st.title("🤌 Prompt Helper")

    # API Key Input
    api_key = st.text_input("Enter your API Key (OpenAI or OpenAI-compatible)", type="password")
    base_url = st.text_input("OpenAI Base URL (optional)")

    if api_key:
        init_openai_config(api_key, base_url)

    # Inputs for the prompts and variables
    system_prompt = st.text_area("System Prompt")
    pre_prompt = st.text_area("Pre-prompt")
    prompt = st.text_area("Prompt")
    post_prompt = st.text_area("Post-prompt")
    variables = st.text_area("Variables (Enter as key:value pairs on new lines)")

    # Parse variables input into a dictionary
    variables_dict = {}
    if variables:
        for line in variables.split("\n"):
            key, value = line.split(":")
            variables_dict[key.strip()] = value.strip()

    # Replace variables in the prompt
    filled_prompt = replace_variables(prompt, variables_dict)

    if st.button("Generate Response") and api_key:
        response = generate_response(system_prompt, pre_prompt, filled_prompt, post_prompt)
        st.text_area("Response", response, height=300)
    elif not api_key:
        st.error("Please enter your OpenAI API Key.")

if __name__ == "__main__":
    main()
