# app/modules/extraction/service.py
import os
from openai import OpenAI
from app.schemas.recipe import RecipeGraphPayload  # The Pydantic model we designed

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def parse_recipe_with_llm(raw_data: dict) -> RecipeGraphPayload:
    system_prompt = """
    You are a culinary operations engineer. Convert raw recipe text, notes, and tips 
    into a Directed Acyclic Graph (DAG) for constraint scheduling.
    
    Rules:
    1. Break compound instructions into discrete, atomic tasks.
    2. Explicitly classify each step as 'active' or 'passive'.
    3. Determine true hard prerequisite dependencies (by task ID).
    4. Account for author notes/tips to tweak durations or warn about burning.
    5. Ensure no cyclic dependencies.
    """

    user_content = f"""
    RECIPE TITLE: {raw_data['title']}
    
    RAW INSTRUCTIONS:
    {raw_data['instructions']}
    
    NOTES & TIPS:
    {raw_data.get('notes', 'None provided')}
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format=RecipeGraphPayload,
        temperature=0.1,
    )

    return completion.choices[0].message.parsed