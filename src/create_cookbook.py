import os
import docx
from utils import create_directory, load_recipes
from doc_utils import add_page_break_if_needed, add_recipe_to_document
from ai_utils import generate_recipe_prompt, create_recipe_script, get_image_for_recipe

# Read the list of recipes from recipes.txt
recipes = load_recipes('recipes.txt')

# Create a new Word document
doc = docx.Document()

is_first_recipe = True
os.makedirs('recipes', exist_ok=True)
# Iterate through each recipe
for recipe_name in recipes:
    try:
        # Create directory for the recipe
        recipe_dir = create_directory(recipe_name)
        # Create prompt for the recipe
        recipe_prompt = generate_recipe_prompt(recipe_name)
        # Generate and return the JSON for the generated recipe
        recipe_data = create_recipe_script(os.path.join(recipe_dir, 'recipe.json'), recipe_prompt)
        # Create an image of the dish
        image_file = get_image_for_recipe(recipe_data, recipe_name, os.path.join(recipe_dir, 'img.png'))
        add_page_break_if_needed(doc, is_first_recipe)
        is_first_recipe = False
        # Add the recipe to the document file
        add_recipe_to_document(doc, recipe_data, image_file)
    except Exception as e:
        print(f"Error generating recipe data for {recipe_name}: {e}")
        continue

# Save the Word document
doc.save('Cookbook.docx')

print("Cookbook created successfully!")