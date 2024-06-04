import os
import pickle
from mlx_lm import load
from mlx_lm import generate

# Define your llama3_model to import
# llama3_model_name = "mlx-community/Meta-Llama-3-70B-Instruct-4bit"
models_dir = './models'
llama3_model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"

# local_llama3_model_dir = "/llama3_models"
local_llama3_model_path = os.path.join(models_dir, llama3_model_name)

def save_object(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def load_object(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

# Check if llama3_model and tokenizer are already downloaded and saved locally
llama3_model_file = os.path.join(local_llama3_model_path, 'llama3_model.pkl')
llama3_tokenizer_file = os.path.join(local_llama3_model_path, 'llama3_tokenizer.pkl')

if os.path.exists(llama3_model_file) and os.path.exists(llama3_tokenizer_file):
    # Load the llama3_model and tokenizer from the local directory
    llama3_model = load_object(llama3_model_file)    
    # llama3_tokenizer = load_object(llama3_tokenizer_file)
    _, llama3_tokenizer = load(llama3_model_name)
    print(f"llama3_model and tokenizer loaded from local directory: {local_llama3_model_path}")
else:
    # Load the llama3_model and llama3_tokenizer from the internet
    llama3_model, llama3_tokenizer = load(llama3_model_name)
    print(f"llama3_model downloaded: {llama3_model_name}")

    # Ensure the directory exists
    os.makedirs(local_llama3_model_path, exist_ok=True)
    
    # Save the llama3_model and tokenizer to the local directory
    save_object(llama3_model, llama3_model_file)
    save_object(llama3_tokenizer, llama3_tokenizer_file)
    print(f"llama3_model and tokenizer saved locally to: {local_llama3_model_path}")

def simple_diolog(model=llama3_model, 
                  tokenizer=llama3_tokenizer, 
                  chatbot_role="You are a test_machine", 
                  user_message='Say something'):
    messages = [
        {"role": "system", "content": chatbot_role}, 
        {"role": "user", "content": user_message}
    ]
    
    # Getting tokenization
    input_ids = llama3_tokenizer.apply_chat_template(messages,  add_generation_prompt=True)
    
    # Decoding input tokenized text
    prompt = tokenizer.decode(input_ids)
    # Generate a response using the llama3_model
    response = generate(model, tokenizer, max_tokens=1024, prompt=prompt)
    # Printing llama3_models response using Markdown cell formatting
    # Markdown(response)
    # print(response)
    return response


def main():
    # Generate a response from the llama3_model
    # Define the role of the chatbot
    chatbot_role = "You are a test_machine"
    # Defining role and message
    question = """
    Say something
    """
    messages = [
        {"role": "system", "content": chatbot_role}, 
        {"role": "user", "content": question}
    ]
    
    # Getting tokenization
    input_ids = llama3_tokenizer.apply_chat_template(messages,  add_generation_prompt=True)
    
    # Decoding input tokenized text
    prompt = llama3_tokenizer.decode(input_ids)
    # Generate a response using the llama3_model
    response = generate(llama3_model, llama3_tokenizer, max_tokens=1024, prompt=prompt)
    # Printing llama3_models response using Markdown cell formatting
    # Markdown(response)
    print(response)

if __name__ == '__main__':
    main()
    # print(simple_diolog())