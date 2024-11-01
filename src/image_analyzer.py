# image_analyzer.py

import os
import openai
import base64
from dotenv import dotenv_values

# Set up OpenAI credentials
CONFIG = dotenv_values(".env")
OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
openai.api_key = OPEN_AI_KEY

def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path):
    """Generate description of the image using GPT-4 Vision"""
    base64_image = encode_image(image_path)
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in detail, focusing on the mood, setting, and key elements. Write it as a narrative description for a story."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=100
    )
    
    return response.choices[0].message.content

def create_markdown_content(image_descriptions):
    """Create markdown content with selected images and descriptions"""
    markdown_content = "# The Tale of the Mechanical Butterfly - Key Scenes\n\n"
    
    for image_num, description in image_descriptions.items():
        markdown_content += f"## Scene {image_num}\n\n"
        markdown_content += f"![Scene {image_num}](../src/img/story_image_{image_num}.png)\n\n"
        markdown_content += f"{description}\n\n"
        markdown_content += "---\n\n"  # Add a horizontal line between scenes
    
    return markdown_content

def process_selected_images():
    """Process only images 3, 6, 9, and 12"""
    selected_images = [3, 6, 9, 12]
    img_dir = "img"
    image_descriptions = {}
    
    # Make sure the directory exists
    if not os.path.exists(img_dir):
        print(f"Error: {img_dir} directory not found")
        return
    
    # Process each image
    for image_num in selected_images:
        image_path = os.path.join(img_dir, f"story_image_{image_num}.png")
        
        if not os.path.exists(image_path):
            print(f"Warning: Image {image_num} not found at {image_path}")
            continue
            
        print(f"\nAnalyzing image {image_num}...")
        
        # Generate description
        description = analyze_image(image_path)
        image_descriptions[image_num] = description
        
        print(f"Description generated for image {image_num}")
    
    # Create and save markdown file
    markdown_content = create_markdown_content(image_descriptions)
    with open("image_explanation.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print("\nProcess complete! Check 'image_explanation.md' for the full story with images and descriptions.")

if __name__ == "__main__":
    process_selected_images()