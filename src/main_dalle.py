import os
import time
import openai
import requests
from dotenv import dotenv_values

# Set up OpenAI credentials
CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def generate_image_prompt(description):
    """Generate image using DALL-E with specific style instructions"""
    style_prompt = f"{description} Style should be detailed and atmospheric, blending Victorian steampunk with magical realism."
    response = openai.images.generate(
        model="dall-e-3",
        prompt=style_prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

def save_image(image_url, save_path):
    """Download and save the image"""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Failed to download image, status code: {response.status_code}")
        return False

def main():
    # Create output directory if it doesn't exist
    os.makedirs("img", exist_ok=True)
    
    # Pre-defined story prompts
    story_prompts = [
        "A cozy, cluttered workshop at sunset, with warm golden light streaming through dusty windows. Vintage tools, half-finished inventions, and mysterious blueprints scatter the wooden workbench. A young inventor in round glasses looks determined, holding a peculiar brass and copper device.",
        "Close-up of weathered hands carefully assembling a small mechanical butterfly with intricate gears, crystal wings, and delicate copper wiring. Soft blue energy glows from within its core. Tools and spare parts surround the work area.",
        "The mechanical butterfly takes its first flight in the workshop, leaving a trail of sparkling light. The inventor watches in wonder as books and papers flutter in the wake of its crystalline wings. Dust motes dance in the air.",
        "The butterfly escapes through an open window into a dark cityscape. Victorian-style buildings and glowing streetlamps dot the horizon. The mechanical creation shimmers against the starlit sky, drawing curious onlookers below.",
        "In a moonlit garden, the butterfly lands on a wilting flower. As it touches the petals, magical energy flows from its wings, causing the flower to bloom and glow with new life. Other flowers begin to turn toward its light.",
        "The news spreads through the city - children point skyward, artists sketch frantically, and scholars debate as the mechanical butterfly brings color and light to grey urban corners. The inventor follows its trail through crowded streets.",
        "A group of shadowy figures in top hats and dark coats attempt to catch the butterfly with nets and mechanical traps. Their devices cast ominous shadows on cobblestone streets. The butterfly narrowly evades capture.",
        "The mechanical butterfly finds refuge in an abandoned greenhouse, where it begins to repair broken glass panels and revive long-dead plants. The structure glows from within like a beacon in the night.",
        "The inventor rushes to defend their creation as the shadowy figures surround the greenhouse. Steam rises from their dark machinery, creating an eerie fog around the glowing structure.",
        "Inside the greenhouse, the butterfly multiplies its magic - creating more mechanical-organic hybrids that fill the air with dancing lights. Plants spiral upward in impossible patterns.",
        "The shadowy figures witness the beauty of the butterfly's creation and lower their weapons. The greenhouse has become a magnificent fusion of nature and technology, with the inventor standing proudly in its center.",
        "Dawn breaks over the city, now transformed. Mechanical butterflies soar between buildings trailing light, plants grow in elegant spirals, and the once-grey streets shimmer with color. The inventor watches from their workshop window, smiling as their creation changes the world."
    ]
    
    # Generate and save each image in sequence
    for i, prompt in enumerate(story_prompts):
        print(f"\nGenerating image {i + 1} of 12...")
        print(f"Current prompt: {prompt[:100]}...")  # Print first 100 chars of prompt for reference
        
        image_url = generate_image_prompt(prompt)
        save_path = f"img/story_image_{i + 1}.png"
        
        if save_image(image_url, save_path):
            print(f"Successfully saved image {i + 1}")
        else:
            print(f"Failed to save image {i + 1}")
        
        # Add a small delay between generations to prevent rate limiting
        time.sleep(2)

if __name__ == "__main__":
    main()