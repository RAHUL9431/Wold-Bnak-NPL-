import openai
openai.api_key = "XXXXXXXXXXXX"

# Define a function to perform NER using BERT and return the named entities
def perform_ner(text):
    # Tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=True)
    # Predict the labels for each token
    model.eval()
    with torch.no_grad():
        outputs = model(torch.tensor(tokens).unsqueeze(0), attention_mask=torch.tensor(tokens).unsqueeze(0))
        predictions = outputs[0].argmax(2).numpy()[0]
    # Convert the predicted labels to named entities
    entities = []
    current_entity = ''
    current_label = ''
    for i in range(len(tokens)):
        token = tokenizer.decode([tokens[i]])
        label = label_map[predictions[i]]
        if label.startswith('B-'):
            current_entity = token
            current_label = label[2:]
        elif label.startswith('I-'):
            current_entity += ' ' + token
        elif label == 'O':
            if current_entity:
                entities.append({'entity': current_entity, 'label': current_label})
                current_entity = ''
                current_label = ''
    if current_entity:
        entities.append({'entity': current_entity, 'label': current_label})
    return entities

# Define a function to generate a response to a user input using GPT-3
def generate_response(input_text):
    # Perform NER on the input text
    entities = perform_ner(input_text)
    # Generate a response based on the named entities
    if len(entities) == 0:
        response = "I'm sorry, I couldn't find any named entities in your input."
    elif len(entities) == 1:
        response = f"I found one named entity in your input: {entities[0]['entity']} ({entities[0]['label']})."
    else:
        entity_list = ', '.join([f"{entity['entity']} ({entity['label']})" for entity in entities])
        response = f"I found {len(entities)} named entities in your input: {entity_list}."
    return response

# Define the prompt for the chatbot
prompt = "Please enter some text for me to perform Named Entity Recognition on:"

# Start the chatbot
print("Hello! I'm a chatbot that can perform Named Entity Recognition on text data. Type 'exit' to end the conversation.")
while True:
    # Get user input
    user_input = input(prompt + '\n')
    if user_input.lower() == 'exit':
        break
    # Generate a response
    response = generate_response(user_input)
    print(response)
