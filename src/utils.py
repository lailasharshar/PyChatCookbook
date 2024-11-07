import os


# Create a recipe directory under the recipes directory
def create_directory(recipe):
    # Create directory for the recipe
    recipe_dir = os.path.join('recipes', recipe.replace(' ', '_').lower())
    os.makedirs(recipe_dir, exist_ok=True)
    return recipe_dir


# Given the list of recipes in the recipes file, load the names
def load_recipes(recipe_file):
    with open(recipe_file, 'r') as f:
        recipes = [line.strip() for line in f if line.strip()]
    return recipes
