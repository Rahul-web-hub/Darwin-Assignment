from transformers import pipeline
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def suggest_titles(request):
    if request.method == 'POST':
        content = request.POST.get('content', '') or json.loads(request.body).get('content', '')
        
        if not content or len(content) < 20:
            return JsonResponse({
                "titles": [
                    "Please provide more content (minimum 20 characters)",
                    "Your blog content seems too short",
                    "Need more details to generate good titles"
                ]
            }, status=400)
        
        try:
            titles = generate_titles(content)
            return JsonResponse({"titles": titles})
        except Exception as e:
            return JsonResponse({
                "error": str(e),
                "titles": [
                    "AI Failed: Using Default Title 1",
                    "AI Failed: Using Default Title 2",
                    "AI Failed: Using Default Title 3"
                ]
            }, status=500)

def clean_title(title):
    """Remove garbage from generated titles"""
    title = re.sub(r'^[^a-zA-Z0-9"\']+', '', title)  # Remove leading special chars
    title = re.sub(r'[^a-zA-Z0-9\s\'",.!?-]+$', '', title)  # Remove trailing garbage
    return title.strip()

def generate_titles(content):
    # Initialize with optimized parameters
    generator = pipeline(
        'text-generation',
        model='gpt2-medium',
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )
    
    # Clean and truncate content
    clean_content = ' '.join(content[:250].split())  # Remove extra whitespace
    
    # Generate in one batch with better prompt
    results = generator(
        f"Generate three distinct blog title options about: {clean_content}\n1.",
        max_length=50,
        num_return_sequences=1,
        temperature=0.9,
        top_p=0.9,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    
    # Process output
    generated_text = results[0]['generated_text']
    titles = []
    
    # Extract just the numbered titles
    for line in generated_text.split('\n'):
        if re.match(r'^\d+\.', line):  # Find numbered lines
            title = clean_title(line.split('.', 1)[1])
            if 10 < len(title) < 80:  # Reasonable length
                titles.append(title)
    
    # Fallback if not enough titles
    while len(titles) < 3:
        titles.append(f"Great Title About {clean_content[:30]}...")
    
    return titles[:3]  # Return exactly 3 titles