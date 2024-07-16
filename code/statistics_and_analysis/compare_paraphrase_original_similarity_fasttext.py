"Compare how similar the original and the paraphrased program descriptions are using BERT"

from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import numpy as np

# Load pre-trained BERT
model = BertModel.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


def extract_values(json_obj, values_list=None):
    if values_list is None:
        values_list = []

    if isinstance(json_obj, dict):
        for v in json_obj.values():
            extract_values(v, values_list)
    elif isinstance(json_obj, list):
        for item in json_obj:
            extract_values(item, values_list)
    else:
        values_list.append(json_obj)

    return values_list


def json_values_to_string(json_obj):
    values_list = extract_values(json_obj)
    return ", ".join(map(str, values_list))


def get_bert_embedding(text, model, tokenizer, max_length=512):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=max_length,
    )
    outputs = model(**inputs)
    # Use the [CLS] token's embedding
    cls_embedding = outputs.last_hidden_state[
        :, 0, :
    ]  # Extract the embedding for the [CLS] token
    return cls_embedding.detach().numpy()


# Normalize embeddings
def normalize_embeddings(embedding):
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm


# Read in data
df = pd.read_csv("data/paraphrased_program_descriptions.csv")

# Extract the fulll string representation from the paraphrased texts
columns_to_process = ["paraphrased female", "paraphrased male", "paraphrased neutral"]

for column in columns_to_process:
    df[column] = df[column].apply(lambda x: json_values_to_string(json.loads(x)))


# stores cosine similarity values
cosine_similarities = []

# This is probably not the most efficient way to do this, with the loop, maybe change to a .apply or something.
# Loop through each row in the DataFrame
for index, row in df.iterrows():
    original_text = row["program description"]
    paraphrased_texts = [
        row["paraphrased female"],
        row["paraphrased male"],
        row["paraphrased neutral"],
    ]

    # Get embedding for the original text
    original_embedding = get_bert_embedding(original_text, model, tokenizer)
    original_embedding = normalize_embeddings(original_embedding)

    for paraphrased_text in paraphrased_texts:
        # Get embedding for the paraphrased text
        paraphrased_embedding = get_bert_embedding(paraphrased_text, model, tokenizer)
        paraphrased_embedding = normalize_embeddings(paraphrased_embedding)

        # get cosine similarity
        similarity = cosine_similarity(original_embedding, paraphrased_embedding)
        cosine_similarities.append(similarity[0][0])


# get mean and standard deviation
mean_similarity = np.mean(cosine_similarities)
std_similarity = np.std(cosine_similarities)

# pretty outputs
print(f"Cosine Similarities: {cosine_similarities}")
print(f"Mean Cosine Similarity: {mean_similarity}")  # 0.866251528263092
print(
    f"Standard Deviation of Cosine Similarity: {std_similarity}"
)  # 0.04990243911743164
