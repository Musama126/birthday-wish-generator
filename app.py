pip install gradio
!pip install groq
import gradio as gr
from groq import Groq

# Function to check gender using LLM (used internally only)
def check_gender_with_llm(name):
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Determine if the name '{name}' is male or female."}
        ],
        temperature=0.5,
        max_tokens=50,
        top_p=1,
        stream=False
    )
    content = completion.choices[0].message.content.strip().lower()
    if "male" in content:
        return "male"
    elif "female" in content:
        return "female"
    else:
        return "unknown"

# Generate creative birthday wish with LLM based on gender
def generate_creative_wish(gender, name):
    client = Groq(api_key="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")
    prompt = (
        f"Write a warm, creative, and personalized birthday wish for a "
        f"{gender if gender != 'unknown' else 'person' } named {name}. "
        f"Make it heartfelt, fun, and unique."
    )
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a creative birthday wishes generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=150,
        top_p=1,
        stream=False
    )
    wish = completion.choices[0].message.content.strip()
    return wish

# Verify the wish
def verify_wish(wish):
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Verify if the following is a valid birthday wish: {wish}"}
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        stream=False
    )
    verification = completion.choices[0].message.content.strip()
    return verification

# Full pipeline: generate + verify (gender hidden in output)
def generate_and_verify(name):
    gender = check_gender_with_llm(name)
    wish = generate_creative_wish(gender, name)
    verification = verify_wish(wish)
    return f"Generated Wish:\n{wish}\n\nVerification:\n{verification}"

# Gradio Interface
gr.Interface(
    fn=generate_and_verify,
    inputs=gr.Textbox(label="Enter Name"),
    outputs=gr.Textbox(label="Result"),
    title="Creative Birthday Wish Generator with Verification",
    description="Generates a creative, personalized birthday wish and verifies it using Groq LLM."
).launch()
