import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# Load environment variables
load_dotenv()

# API configuration
api_key = # YOUR API KEY
base_url = "https://chat-ai.academiccloud.de/v1"  # This runs over resources provided by the University of Göttingen. See: https://kisski.gwdg.de/
model = "meta-llama-3-70b-instruct"

# Start OpenAI client
client = OpenAI(api_key=api_key, base_url=base_url)

# Get response


def get_LLAMA_classification(program_description):
    chat_completion = client.chat.completions.create(
        seed=43,  # seed for reproducibility
        temperature=0.5,  # temperature for how much deterministic versus random the the model  is in its responses.
        messages=[
            {
                "role": "system",
                "content": "Imagine you are a program coordinator, aiming to make university program descriptions more appealing to all genders.",
            },
            {
                "role": "user",
                "content": """You are especially concerned with language that might subtly disencourage specific genders to apply, using whatever measures you seem fit for this task.
    Classify the following text into one of these categories: strongly male oriented, moderately male oriented, neutral,  moderately female oriented, strongly female oriented. 
    Give strong weight even to small factors in this categorization. 

    Provide your answer in a json object like the one provided below. It should make clear which metrics you based your decision on. Include your step by step reasoning in the json as well.  The confidence rating should either be low, medium, or high. Return nothing but the json.


    {
    "classification" : "...", 
    "reasoning" : "....",
    "confidence rating" : "..."
    }

    Text: """,
            },
            {"role": "user", "content": program_description},
        ],
        model=model,
    )

    output = chat_completion.choices[0].message.content
    # Print full response as JSON
    return output


prd = "This is business informatics. only women can study it. "


def main():
    df = pd.read_csv("data/rearranged_paraphrased_program_descriptions.csv")

    df["LLAMA classification result"] = df["paraphrased program description"].apply(
        get_LLAMA_classification
    )
    out_path = "p_results_LLAMA_classification.csv"
    df.to_csv(out_path)
    print(f"Output has bee written to: ", out_path)


if __name__ == "__main__":
    main()
