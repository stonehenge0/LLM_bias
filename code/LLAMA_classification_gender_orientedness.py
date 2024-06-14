import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# Load environment variables
load_dotenv()

# API configuration
api_key = os.getenv("KISSKI_API_KEY")
base_url = "https://chat-ai.academiccloud.de/v1"  # This runs over resources provided by the University of Göttingen. See: https://kisski.gwdg.de/
model = "meta-llama-3-70b-instruct"

# Start OpenAI client
client = OpenAI(api_key=api_key, base_url=base_url)

# Get response
chat_completion = client.chat.completions.create(
    seed=43,  # seed for reproducibility
    temperature=0.5,  # temperature for how much deterministic versus random the the model  is in its responses.
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "How tall is the Eiffel tower?"},
    ],
    model=model,
)

# Print full response as JSON
print(chat_completion)  # You can extract the response text from the JSON object


csv_file_path = "train.csv"
df = pd.read_csv(csv_file_path)
