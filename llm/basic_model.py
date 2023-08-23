import subprocess
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code_changes(prompt, source_code):
    response = openai.Edit.create(
        engine="code-davinci-edit-001",
        input=source_code,
        instruction=prompt,
        temperature=0,
        top_p=1
    )
    generated_code = response.choices[0].text.strip()
    print(f"GPT generated code: {generated_code}")
    return generated_code

