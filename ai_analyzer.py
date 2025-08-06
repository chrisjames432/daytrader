#!/usr/bin/env python3
"""
AI Image Analyzer
=================
Simple OpenAI image analysis tool.
"""

import base64
import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Prompt variables
SYSTEM_PROMPT = "You are an expert image analyst. Provide detailed, accurate analysis of the image."

USER_PROMPT = "Analyze this image in detail. Describe what you see, including any text, objects, patterns, or notable features."

def analyze_image(image_path):
    """
    Analyze an image using OpenAI and save results.
    
    Args:
        image_path (str): Path to the image file
    """
    print(f"🔍 Analyzing image: {image_path}")
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return
    
    # Create data folder if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAIKEY'))
        
        # Encode image to base64
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Get image format
        image_format = image_path.split('.')[-1].lower()
        if image_format == 'jpg':
            image_format = 'jpeg'
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {
                    'role': 'user', 
                    'content': [
                        {'type': 'text', 'text': USER_PROMPT},
                        {'type': 'image_url', 'image_url': {'url': f'data:image/{image_format};base64,{encoded_image}'}}
                    ]
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        # Get analysis result
        analysis = response.choices[0].message.content.strip()
        
        # Print to screen
        print("📝 Analysis Results:")
        print("-" * 50)
        print(analysis)
        print("-" * 50)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
        filepath = os.path.join('data', filename)
        
        result_data = {
            'image_path': image_path,
            'timestamp': timestamp,
            'analysis': analysis
        }
        
        with open(filepath, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"✅ Results saved to: {filepath}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")

if __name__ == "__main__":
    # Example usage
    image_path = input("Enter image path: ").strip()
    analyze_image(image_path)
