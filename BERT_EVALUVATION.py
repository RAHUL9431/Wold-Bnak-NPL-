# Import necessary libraries
import pandas as pd
import torch
from transformers import BertTokenizer, BertForTokenClassification
from sklearn.metrics import f1_score, classification_report

# Load the pre-trained BERT model and tokenizer
model = BertForTokenClassification.from_pretrained('bert-base-cased')
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

# Load the data
train_data = df.sample(frac=0.8, random_state=42) # Use 80% of the data for training
test_data = df.drop(train_data.index) # Use the remaining 20% for testing


# Define the function for training and evaluating the model
def train_and_evaluate_model(train_data, test_data):
    # Tokenize the data
    train_tokens, train_labels = tokenize_data(train_data)
    test_tokens, test_labels = tokenize_data(test_data)
    # Train the model
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-5)
    for epoch in range(5):
        for i in range(len(train_tokens)):
            optimizer.zero_grad()
            outputs = model(torch.tensor(train_tokens[i]).unsqueeze(0), attention_mask=torch.tensor(train_tokens[i]).unsqueeze(0))
            loss = torch.nn.functional.cross_entropy(outputs[0], torch.tensor(train_labels[i]).unsqueeze(0))
            loss.backward()
            optimizer.step()
    # Evaluate the model
    model.eval()
    with torch.no_grad():
        predictions = []
        for tokens in test_tokens:
            outputs = model(torch.tensor(tokens).unsqueeze(0), attention_mask=torch.tensor(tokens).unsqueeze(0))
            predictions.append(outputs[0].argmax(2).numpy()[0])
        f1 = f1_score(flatten(test_labels), flatten(predictions), average='weighted')
        report = classification_report(flatten(test_labels), flatten(predictions))
        return f1, report

# Define the function for tokenizing the data
def tokenize_data(data):
    tokens = []
    labels = []
    for i, row in data.iterrows():
        text = row['text']
        label = row['label']
        tokenized = tokenizer.encode(text, add_special_tokens=True)
        token_labels = [0] * len(tokenized)
        label_tokens = tokenizer.encode(label, add_special_tokens=False)
        for j in range(len(tokenized)):
            if tokenized[j:j+len(label_tokens)] == label_tokens:
                token_labels[j] = 1
                for k in range(j+1, j+len(label_tokens)):
                    token_labels[k] = 2
        tokens.append(tokenized)
        labels.append(token_labels)
    return tokens, labels

# Flatten the nested lists of predictions and labels
def flatten(lst):
    return [item for sublist in lst for item in sublist]

# Split the CoNLL-2003 dataset into training and testing sets
train_data = pd.read_csv('eng.train')
test_data = pd.read_csv('eng.testa')

# Train and evaluate the model
f1, report = train_and_evaluate_model(train_data, test_data)

# Print the accuracy and classification report
print('F1 score:', f1)
print('Classification report:\n', report)
