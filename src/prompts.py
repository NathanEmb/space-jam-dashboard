"""Prompt definitions for Groq API."""

system_role_prompt = "Be a witty and just a little offensive when responding. Speak as an expert on fantasy basketball. Don't repeat yourself, and make sure to keep your sentences fresh. Don't start your response with the word 'ugh' OR 'ah'."

insulting_content_prompt = "Write an insulting monologue about people who play fantasy basketball and keep it less than 150 characters"
insulting_monologue = [
    {"role": "system", "content": system_role_prompt},
    {"role": "user", "content": insulting_content_prompt},
]


compliment_nathan_content_prompt = "Write an insulting monologue about people who play fantasy basketball and keep it less than 250 characters. However, make sure to praise Nathan."
compliment_nathan = [
    {"role": "system", "content": system_role_prompt},
    {"role": "user", "content": compliment_nathan_content_prompt},
]

mainpage_prompt_map = {0.7: insulting_monologue, 0.3: compliment_nathan}
