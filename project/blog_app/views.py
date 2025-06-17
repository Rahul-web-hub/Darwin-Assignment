from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import torch
import re

# Initialize generator once at app startup
TITLE_GENERATOR = None

def get_generator():
    global TITLE_GENERATOR
    if TITLE_GENERATOR is None:
        TITLE_GENERATOR = pipeline(
            'text-generation',
            model='gpt2-medium',
            device='cuda' if torch.cuda.is_available() else 'cpu',
            torch_dtype=torch.float16 if torch.cuda.is_available() else None
        )
    return TITLE_GENERATOR

def clean_title(title):
    """Remove unwanted characters and format the title properly"""
    title = re.sub(r'^[^a-zA-Z0-9"\']+', '', title)  # Remove leading special chars
    title = re.sub(r'[^a-zA-Z0-9\s\'",.!?-]+$', '', title)  # Remove trailing garbage
    title = title.replace('"', '').strip()
    return title[0].upper() + title[1:]  # Capitalize first letter

@csrf_exempt
def suggest_titles(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method allowed"}, status=405)
    
    try:
        content = request.POST.get('content', '') or json.loads(request.body).get('content', '')
        
        if not content or len(content) < 20:
            return JsonResponse({
                "titles": [
                    "Please provide more content (minimum 20 characters)",
                    "Your blog content seems too short",
                    "Need more details to generate good titles"
                ]
            }, status=400)
        
        # Generate exactly 3 titles
        titles = generate_titles(content[:500])  # Truncate to first 500 chars
        return JsonResponse({"titles": titles[:3]})  # Ensure only 3 returned
    
    except Exception as e:
        print(f"Error generating titles: {str(e)}")
        return JsonResponse({
            "titles": [
                "How to Master Your Content Strategy",
                "The Ultimate Guide to Engaging Blog Posts",
                "10 Tips for Writing Captivating Content"
            ]
        }, status=500)

def generate_titles(content):
    generator = get_generator()
    
    # Improved prompt engineering
    prompt = f"""Generate three distinct, engaging blog title options about: "{content[:200]}"
1. """
    
    try:
        results = generator(
            prompt,
            max_length=30,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            num_beams=3,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        
        # Process output to extract exactly 3 clean titles
        output = results[0]['generated_text']
        titles = []
        
        # Extract numbered titles
        for line in output.split('\n'):
            if re.match(r'^\d+\.', line):  # Find numbered lines
                title = clean_title(line.split('.', 1)[1])
                if 10 < len(title) < 80:  # Reasonable length check
                    titles.append(title)
                    if len(titles) >= 3:
                        break
        
        # Fallback if we didn't get 3 good titles
        while len(titles) < 3:
            fallbacks = [
                f"The Complete Guide to {content[:30]}",
                f"5 Essential Tips About {content[:20]}",
                f"{content[:25]}: What You Need to Know"
            ]
            titles.append(fallbacks[len(titles)])
        
        return titles[:3]
    
    except Exception as e:
        print(f"Generation error: {str(e)}")
        raise