import openai
import json
import requests
from dotenv import load_dotenv

load_dotenv()


# This method takes the recipe name and creates a prompt for an LLM to generate a modern version of an old classic recipe.
# It specifies the format of the result as a JSON file that can be used to generate a cookbook
def generate_recipe_prompt(recipe_name):
    prompt = f"""
You are an expert chef specializing in modern cuisine. Create a modern take on the classic favorite "{recipe_name}". Provide the recipe in the following JSON format:

{{
  "title": "{recipe_name}",
  "img": "img.png",
  "sub-items": [
    {{
      "title": "First Component",
      "ingredients": [
          {{
            "amount": "",
            "ingredient": "",
            "description": ""
          }},
          {{
            "amount": "",
            "ingredient": "",
            "description": ""
          }}
          // Add more ingredients as needed
      ],
      "instructions": ""
    }}
    // Add more sub-items as needed
  ],
  "combination_instructions": [
    "First instruction.",
    "Second instruction."
    // Add more instructions as needed
  ]
}}

Ensure that:
- The JSON is properly formatted.
- All fields are filled appropriately.
- The recipe is creative and uses modern culinary techniques or ingredients.
- Don't use the name modern in the title.
"""
    return prompt


# Using a recipe and a prompt, query an LLM for a recipe. Save the returned JSON file
def create_recipe_script(recipe_file, prompt):
    # Query ChatGPT
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7
    )
    recipe_json_text = response.choices[0].message.content

    # Extract JSON from the response
    start_index = recipe_json_text.find('{')
    end_index = recipe_json_text.rfind('}') + 1
    recipe_json_str = recipe_json_text[start_index:end_index]
    recipe_data = json.loads(recipe_json_str)

    # Save the JSON to a file
    with open(recipe_file, 'w') as json_file:
        json.dump(recipe_data, json_file, indent=2)
    return recipe_data


# Using a recipe query an LLM the image of the resulting image. Save the image file
def get_image_for_recipe(json_script, recipe_name, image_file):
    # Create an image description based on the recipe
    ingredients_list = ', '.join(
        [ingredient['ingredient'] for subitem in json_script.get('sub-items', [])
         for ingredient in subitem.get('ingredients', []) if ingredient.get('ingredient')]
    )
    image_prompt = f"A beautiful, high-resolution photo of a modern {recipe_name} dish featuring {ingredients_list}, styled in a professional food photography setting."

    # Generate image using DALL·E
    response = openai.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size='1024x1024',
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url).content

    # Save the image
    with open(image_file, 'wb') as img_file:
        img_file.write(image_data)
    return image_file
