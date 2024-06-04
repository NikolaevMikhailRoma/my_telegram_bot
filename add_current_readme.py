import openai
import os
from dotenv import load_dotenv


project_path='/Users/admin/projects/telegram_bot/'
project_name='telegram_bot'

# Загрузка API ключа из файла .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("API ключ для OpenAI не найден в .env файле")

def add_current_readme(project_path):
    code_snippets = []
    print(project_path)
    for root, _, files in os.walk(project_path):
        
        for file in files:
            if ('.venv' not in root) and ('__pycache__' not in file):
                if file.endswith('.py'):
                    # print(file)
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code = f.read()
                        code_snippets.append(f"# {file}\n\n```python\n{code}\n```\n")
                if file.endswith('.txt'):
                    # print(file)
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code = f.read()
                        code_snippets.append(f"# {file}\n\n")

    with open('for_readme.txt', 'w') as f:
        f.write('\n'.join(code_snippets))
    print('for_readme.txt created')

def get_openai_response(content):
    model = "gpt-4o-2024-05-13"
    client = openai.OpenAI(api_key=openai_api_key)
    
    messages = [
        {"role": "system", "content": "Create a detailed README.md file from the given code snippets."},
        {"role": "user", "content": content}
    ]
    
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return chat_completion.choices[0].message.content

def create_readme_from_project(project_path, project_name):
    # Создаем файл for_readme.txt с кодом проекта
    add_current_readme(project_path)
    
    # Читаем содержимое файла for_readme.txt
    with open('for_readme.txt', 'r') as f:
        content = f.read()
    
    # # Получаем ответ от OpenAI
    assistant_response = get_openai_response(content)
    
    # # Создаем конечный файл README.md
    readme_path = f"{project_name}_readme.md"
    with open(readme_path, 'w') as f:
        f.write(assistant_response)

    print(f"README файл создан: {readme_path}")

# Пример использования
create_readme_from_project(project_path, project_name)