# Import necessary libraries
#!pip install transformers
import pandas as pd
import torch
from transformers import BertTokenizer, BertForTokenClassification

# Load the pre-trained BERT model and tokenizer
model = BertForTokenClassification.from_pretrained('bert-base-cased')
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

# Load the data
data = df

# Define the function for extracting named entities from text
def extract_entities(text):
    # Tokenize the text and add special tokens
    tokens = tokenizer.encode(text, add_special_tokens=True)
    # Get the token labels from the model
    with torch.no_grad():
        outputs = model(torch.tensor(tokens).unsqueeze(0))
        predictions = outputs[0].argmax(2).numpy()[0]
    # Convert the token labels back to named entities
    entities = []
    current_entity = ''
    current_label = ''
    for i, token in enumerate(tokens):
        label = predictions[i]
        if label == 0 or label == 2:  # ignore 'O' labels and 'CLS'/'SEP' tokens
            if current_entity != '':
                entities.append((current_entity.strip(), current_label))
                current_entity = ''
                current_label = ''
        if label == 1:  # 'B' label indicates start of a new entity
            if current_entity != '':
                entities.append((current_entity.strip(), current_label))
            current_entity = tokenizer.convert_ids_to_tokens([token])[0]
            current_label = 'B'
        if label == 3:  # 'I' label indicates continuation of an entity
            current_entity += ' ' + tokenizer.convert_ids_to_tokens([token])[0]
            current_label = 'I'
    if current_entity != '':
        entities.append((current_entity.strip(), current_label))
    return entities

# Apply the function to each column of text data
for column in data.columns:
    data[column+'_entities'] = data[column].apply(extract_entities)
