import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

from flask import (
    Blueprint, jsonify, request
)

bp = Blueprint('open_ai', __name__, url_prefix='/ai')

@bp.route('/prompt', methods=('GET', 'POST'))
def generate_recipe():
    prompt = request.json['prompt']
    # prompt = f"Generate a recipe suitable for a {age}-year-old"
    # if selected_fitness_goal:
    #     prompt += f" with a goal of {selected_fitness_goal.lower()}"
    # if height and weight:
    #     prompt += f", {height} cm tall, and {weight} kg in weight"
    # if selected_protein_preference:
    #     prompt += f" that is {selected_protein_preference.lower()}"
    # if cuisine_type:
    #     prompt += f" and has a {cuisine_type.lower()} influence"
    # if dietary_restrictions:
    #     prompt += f" while being {dietary_restrictions.lower()}"
    # prompt += ". Also, provide the nutritional information."
    
    print(prompt)
    # Make a request to the OpenAI API
    response = openai.completions.create(
        # engine="davinci-002",
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0,
        max_tokens=400  # Adjust the maximum number of tokens based on the desired response length
    )
    
    # Get the generated recipe from the API response
    # print('=== === === === === === === ===')
    # print('response: ', response)
    # print('=== === === === === === === ===')
    
    recipe = response.choices[0].text.strip()

    return jsonify(recipe)
