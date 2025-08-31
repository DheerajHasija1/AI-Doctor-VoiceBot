import os
Groq_Api = os.environ.get("GROQ_API_KEY")

# Convert image to required format
import base64


# Step 2: Encode the image
# image_path = "acne.jpg"
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image


# Step 3: Use image + query with LLM 
from groq import Groq
# Initialize Groq client - no model parameter here
llm = Groq(api_key=Groq_Api)
query = "Is there something wrong with my face?"


def analyze_image_with_query(query, encoded_image,model):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]

    chat_completion = llm.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content