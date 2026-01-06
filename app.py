import streamlit as st
import json
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup

def fetch_url_content(url):
    """Fetch and extract text content from a URL.
    
    Security Note: This function fetches content from user-provided URLs.
    Basic validation is implemented to allow only http:// and https:// protocols.
    Users should be aware that this could be used to fetch content from any
    publicly accessible web page.
    """
    try:
        # Validate URL scheme
        if not url.startswith(('http://', 'https://')):
            return None, "Invalid URL: Only http:// and https:// protocols are supported"
        
        # Add timeout and headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n'.join(lines)
        
        return content, None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching URL: {str(e)}"
    except Exception as e:
        return None, f"Error processing URL content: {str(e)}"


def generate_schema_with_ai(input_text, schema_type, api_key):
    """Generate schema data using Gemini AI based on the selected schema type."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompts = {
            "FAQPage": f"""You are an AI assistant that extracts questions and answers from FAQ content.

Given the following FAQ content, identify all question and answer pairs. The content may or may not have Q: and A: prefixes.

FAQ Content:
{input_text}

Extract each question and its corresponding answer, and return the result as a valid JSON object with this exact structure:
{{
  "mainEntity": [
    {{"question": "First question text here", "answer": "First answer text here"}},
    {{"question": "Second question text here", "answer": "Second answer text here"}}
  ]
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Ensure the JSON is valid and properly formatted
- Extract all question-answer pairs in the order they appear
- Remove any Q: or A: prefixes if present
- If the content doesn't contain clear Q&A pairs, return {{"mainEntity": []}}""",

            "Article": f"""You are an AI assistant that extracts article information from content.

Given the following content about an article:
{input_text}

Extract the article information and return a valid JSON object with this structure:
{{
  "headline": "Main article title",
  "author": "Author name",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "description": "Brief description of the article",
  "articleBody": "Full article text or summary",
  "image": "URL to article image (if mentioned)"
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Use today's date if publication date is not specified
- If a field is not found, use a reasonable default or empty string
- Extract information intelligently from the provided content""",

            "Product": f"""You are an AI assistant that extracts product information from content.

Given the following content about a product:
{input_text}

Extract the product information and return a valid JSON object with this structure:
{{
  "name": "Product name",
  "description": "Product description",
  "image": "URL to product image (if mentioned)",
  "brand": "Brand name",
  "offers": {{
    "price": "0.00",
    "priceCurrency": "USD",
    "availability": "InStock"
  }},
  "aggregateRating": {{
    "ratingValue": "0.0",
    "reviewCount": "0"
  }}
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract all mentioned product details
- Use reasonable defaults for missing information""",

            "Breadcrumb": f"""You are an AI assistant that extracts breadcrumb navigation from content.

Given the following content about a breadcrumb trail:
{input_text}

Extract the breadcrumb items and return a valid JSON object with this structure:
{{
  "itemListElement": [
    {{"position": 1, "name": "Home", "item": "https://example.com"}},
    {{"position": 2, "name": "Category", "item": "https://example.com/category"}},
    {{"position": 3, "name": "Current Page", "item": "https://example.com/category/page"}}
  ]
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract breadcrumb items in order
- If URLs are not provided, use placeholder URLs like https://example.com""",

            "LocalBusiness": f"""You are an AI assistant that extracts local business information from content.

Given the following content about a local business:
{input_text}

Extract the business information and return a valid JSON object with this structure:
{{
  "name": "Business name",
  "description": "Business description",
  "image": "URL to business image (if mentioned)",
  "address": {{
    "streetAddress": "Street address",
    "addressLocality": "City",
    "addressRegion": "State/Region",
    "postalCode": "Postal code",
    "addressCountry": "Country"
  }},
  "telephone": "Phone number",
  "openingHours": "Mo-Fr 09:00-17:00",
  "priceRange": "$$"
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract all mentioned business details
- Use empty strings for missing information""",

            "HowTo": f"""You are an AI assistant that extracts how-to instructions from content.

Given the following content about a how-to guide:
{input_text}

Extract the how-to information and return a valid JSON object with this structure:
{{
  "name": "How to do something",
  "description": "Brief description of what this guide teaches",
  "totalTime": "PT30M",
  "step": [
    {{"name": "Step 1", "text": "Description of step 1"}},
    {{"name": "Step 2", "text": "Description of step 2"}},
    {{"name": "Step 3", "text": "Description of step 3"}}
  ]
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract all steps in order
- Use ISO 8601 duration format for totalTime (e.g., PT30M for 30 minutes)
- If time is not specified, estimate based on steps""",

            "Recipe": f"""You are an AI assistant that extracts recipe information from content.

Given the following content about a recipe:
{input_text}

Extract the recipe information and return a valid JSON object with this structure:
{{
  "name": "Recipe name",
  "description": "Recipe description",
  "image": "URL to recipe image (if mentioned)",
  "author": "Author name",
  "prepTime": "PT15M",
  "cookTime": "PT30M",
  "totalTime": "PT45M",
  "recipeYield": "4 servings",
  "recipeIngredient": [
    "Ingredient 1",
    "Ingredient 2",
    "Ingredient 3"
  ],
  "recipeInstructions": [
    {{"name": "Step 1", "text": "First instruction"}},
    {{"name": "Step 2", "text": "Second instruction"}}
  ]
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract all recipe details including ingredients and steps
- Use ISO 8601 duration format for times (e.g., PT30M for 30 minutes)""",

            "Person": f"""You are an AI assistant that extracts person information from content.

Given the following content about a person:
{input_text}

Extract the person information and return a valid JSON object with this structure:
{{
  "name": "Full name",
  "jobTitle": "Job title or profession",
  "description": "Brief biography or description",
  "image": "URL to person's image (if mentioned)",
  "url": "URL to person's website or profile",
  "email": "Email address",
  "telephone": "Phone number",
  "address": {{
    "addressLocality": "City",
    "addressRegion": "State/Region",
    "addressCountry": "Country"
  }}
}}

Important:
- Only return the JSON object, nothing else
- Do not include any markdown formatting or code blocks
- Extract all mentioned person details
- Use empty strings for missing information"""
        }
        
        prompt = prompts.get(schema_type, prompts["FAQPage"])
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        elif result_text.startswith('```'):
            result_text = result_text[3:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        # Parse the JSON response
        data = json.loads(result_text)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Failed to parse AI response as JSON: {str(e)}"
    except Exception as e:
        return None, f"AI parsing error: {str(e)}"

def parse_faq_input(input_text):
    """Parse FAQ input text into structured questions and answers."""
    faqs = []
    sections = input_text.strip().split('\n\n')
    
    for section in sections:
        lines = section.strip().split('\n')
        question = ''
        answer = ''
        
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.upper().startswith('Q:'):
                question = trimmed_line[2:].strip()
            elif trimmed_line.upper().startswith('A:'):
                answer = trimmed_line[2:].strip()
            elif question and not answer:
                question += ' ' + trimmed_line
            elif answer:
                answer += ' ' + trimmed_line
        
        if question and answer:
            faqs.append({'question': question, 'answer': answer})
    
    return faqs

def generate_json_ld(data, schema_type):
    """Generate JSON-LD schema based on schema type."""
    schemas = {
        "FAQPage": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item['question'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item['answer']
                    }
                }
                for item in data.get('mainEntity', [])
            ]
        },
        "Article": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": data.get('headline', ''),
            "author": {
                "@type": "Person",
                "name": data.get('author', '')
            },
            "datePublished": data.get('datePublished', ''),
            "dateModified": data.get('dateModified', ''),
            "description": data.get('description', ''),
            "articleBody": data.get('articleBody', ''),
            "image": data.get('image', '')
        },
        "Product": {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": data.get('name', ''),
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "brand": {
                "@type": "Brand",
                "name": data.get('brand', '')
            },
            "offers": {
                "@type": "Offer",
                "price": data.get('offers', {}).get('price', '0.00'),
                "priceCurrency": data.get('offers', {}).get('priceCurrency', 'USD'),
                "availability": f"https://schema.org/{data.get('offers', {}).get('availability', 'InStock')}"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": data.get('aggregateRating', {}).get('ratingValue', '0.0'),
                "reviewCount": data.get('aggregateRating', {}).get('reviewCount', '0')
            }
        },
        "Breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": item['position'],
                    "name": item['name'],
                    "item": item['item']
                }
                for item in data.get('itemListElement', [])
            ]
        },
        "LocalBusiness": {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": data.get('name', ''),
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": data.get('address', {}).get('streetAddress', ''),
                "addressLocality": data.get('address', {}).get('addressLocality', ''),
                "addressRegion": data.get('address', {}).get('addressRegion', ''),
                "postalCode": data.get('address', {}).get('postalCode', ''),
                "addressCountry": data.get('address', {}).get('addressCountry', '')
            },
            "telephone": data.get('telephone', ''),
            "openingHours": data.get('openingHours', ''),
            "priceRange": data.get('priceRange', '')
        },
        "HowTo": {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": data.get('name', ''),
            "description": data.get('description', ''),
            "totalTime": data.get('totalTime', ''),
            "step": [
                {
                    "@type": "HowToStep",
                    "name": step['name'],
                    "text": step['text']
                }
                for step in data.get('step', [])
            ]
        },
        "Recipe": {
            "@context": "https://schema.org",
            "@type": "Recipe",
            "name": data.get('name', ''),
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "author": {
                "@type": "Person",
                "name": data.get('author', '')
            },
            "prepTime": data.get('prepTime', ''),
            "cookTime": data.get('cookTime', ''),
            "totalTime": data.get('totalTime', ''),
            "recipeYield": data.get('recipeYield', ''),
            "recipeIngredient": data.get('recipeIngredient', []),
            "recipeInstructions": [
                {
                    "@type": "HowToStep",
                    "name": step['name'],
                    "text": step['text']
                }
                for step in data.get('recipeInstructions', [])
            ]
        },
        "Person": {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": data.get('name', ''),
            "jobTitle": data.get('jobTitle', ''),
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "url": data.get('url', ''),
            "email": data.get('email', ''),
            "telephone": data.get('telephone', ''),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": data.get('address', {}).get('addressLocality', ''),
                "addressRegion": data.get('address', {}).get('addressRegion', ''),
                "addressCountry": data.get('address', {}).get('addressCountry', '')
            }
        }
    }
    
    schema = schemas.get(schema_type, schemas["FAQPage"])
    return json.dumps(schema, indent=2)

def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def generate_microdata(data, schema_type):
    """Generate HTML microdata based on schema type."""
    if schema_type == "FAQPage":
        html = '<div itemscope itemtype="https://schema.org/FAQPage">\n'
        for item in data.get('mainEntity', []):
            html += '  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">\n'
            html += f'    <h3 itemprop="name">{escape_html(item["question"])}</h3>\n'
            html += '    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">\n'
            html += f'      <div itemprop="text">{escape_html(item["answer"])}</div>\n'
            html += '    </div>\n'
            html += '  </div>\n'
        html += '</div>'
        return html
    elif schema_type == "Article":
        html = '<article itemscope itemtype="https://schema.org/Article">\n'
        html += f'  <h1 itemprop="headline">{escape_html(data.get("headline", ""))}</h1>\n'
        html += f'  <div itemprop="author" itemscope itemtype="https://schema.org/Person">\n'
        html += f'    <span itemprop="name">{escape_html(data.get("author", ""))}</span>\n'
        html += '  </div>\n'
        html += f'  <meta itemprop="datePublished" content="{data.get("datePublished", "")}">\n'
        html += f'  <meta itemprop="dateModified" content="{data.get("dateModified", "")}">\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += f'  <div itemprop="articleBody">{escape_html(data.get("articleBody", ""))}</div>\n'
        html += '</article>'
        return html
    elif schema_type == "Product":
        html = '<div itemscope itemtype="https://schema.org/Product">\n'
        html += f'  <h1 itemprop="name">{escape_html(data.get("name", ""))}</h1>\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += f'  <div itemprop="brand" itemscope itemtype="https://schema.org/Brand">\n'
        html += f'    <span itemprop="name">{escape_html(data.get("brand", ""))}</span>\n'
        html += '  </div>\n'
        html += '  <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n'
        html += f'    <span itemprop="price">{data.get("offers", {}).get("price", "0.00")}</span>\n'
        html += f'    <meta itemprop="priceCurrency" content="{data.get("offers", {}).get("priceCurrency", "USD")}">\n'
        html += '  </div>\n'
        html += '</div>'
        return html
    elif schema_type == "Breadcrumb":
        html = '<ol itemscope itemtype="https://schema.org/BreadcrumbList">\n'
        for item in data.get('itemListElement', []):
            html += '  <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">\n'
            html += f'    <a itemprop="item" href="{escape_html(item["item"])}">\n'
            html += f'      <span itemprop="name">{escape_html(item["name"])}</span>\n'
            html += '    </a>\n'
            html += f'    <meta itemprop="position" content="{item["position"]}">\n'
            html += '  </li>\n'
        html += '</ol>'
        return html
    elif schema_type == "LocalBusiness":
        html = '<div itemscope itemtype="https://schema.org/LocalBusiness">\n'
        html += f'  <h1 itemprop="name">{escape_html(data.get("name", ""))}</h1>\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += '  <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">\n'
        html += f'    <span itemprop="streetAddress">{escape_html(data.get("address", {}).get("streetAddress", ""))}</span>,\n'
        html += f'    <span itemprop="addressLocality">{escape_html(data.get("address", {}).get("addressLocality", ""))}</span>,\n'
        html += f'    <span itemprop="addressRegion">{escape_html(data.get("address", {}).get("addressRegion", ""))}</span>\n'
        html += f'    <span itemprop="postalCode">{escape_html(data.get("address", {}).get("postalCode", ""))}</span>\n'
        html += '  </div>\n'
        html += f'  <div itemprop="telephone">{escape_html(data.get("telephone", ""))}</div>\n'
        html += '</div>'
        return html
    elif schema_type == "HowTo":
        html = '<div itemscope itemtype="https://schema.org/HowTo">\n'
        html += f'  <h1 itemprop="name">{escape_html(data.get("name", ""))}</h1>\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += '  <ol>\n'
        for step in data.get('step', []):
            html += '    <li itemprop="step" itemscope itemtype="https://schema.org/HowToStep">\n'
            html += f'      <strong itemprop="name">{escape_html(step["name"])}</strong>: \n'
            html += f'      <span itemprop="text">{escape_html(step["text"])}</span>\n'
            html += '    </li>\n'
        html += '  </ol>\n'
        html += '</div>'
        return html
    elif schema_type == "Recipe":
        html = '<div itemscope itemtype="https://schema.org/Recipe">\n'
        html += f'  <h1 itemprop="name">{escape_html(data.get("name", ""))}</h1>\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += f'  <div itemprop="author" itemscope itemtype="https://schema.org/Person">\n'
        html += f'    <span itemprop="name">{escape_html(data.get("author", ""))}</span>\n'
        html += '  </div>\n'
        html += '  <div>Ingredients:</div>\n'
        html += '  <ul>\n'
        for ingredient in data.get('recipeIngredient', []):
            html += f'    <li itemprop="recipeIngredient">{escape_html(ingredient)}</li>\n'
        html += '  </ul>\n'
        html += '  <div>Instructions:</div>\n'
        html += '  <ol>\n'
        for step in data.get('recipeInstructions', []):
            html += '    <li itemprop="recipeInstructions" itemscope itemtype="https://schema.org/HowToStep">\n'
            html += f'      <span itemprop="text">{escape_html(step["text"])}</span>\n'
            html += '    </li>\n'
        html += '  </ol>\n'
        html += '</div>'
        return html
    elif schema_type == "Person":
        html = '<div itemscope itemtype="https://schema.org/Person">\n'
        html += f'  <h1 itemprop="name">{escape_html(data.get("name", ""))}</h1>\n'
        html += f'  <div itemprop="jobTitle">{escape_html(data.get("jobTitle", ""))}</div>\n'
        html += f'  <div itemprop="description">{escape_html(data.get("description", ""))}</div>\n'
        html += f'  <div itemprop="email">{escape_html(data.get("email", ""))}</div>\n'
        html += f'  <div itemprop="telephone">{escape_html(data.get("telephone", ""))}</div>\n'
        html += '</div>'
        return html
    else:
        return "Microdata not available for this schema type"

# Page configuration
st.set_page_config(
    page_title="Schema Data Generator",
    page_icon="📋",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
    h1 {
        color: #667eea;
    }
    .output-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .example-box {
        background-color: #f0f4ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Schema Data Generator")
st.markdown("**Generate JSON-LD and HTML Microdata for your content**")

# Main content
st.header("Select Schema Type")

# Schema type selector
schema_type = st.selectbox(
    "Choose the type of schema you want to generate:",
    ["FAQPage", "Article", "Product", "Breadcrumb", "LocalBusiness", "HowTo", "Recipe", "Person"],
    key="schema_type"
)

st.header("Input Your Content")

# API Key input
api_key = st.text_input(
    "Google Gemini API Key (required for AI-powered generation):",
    type="password",
    help="Enter your Google Gemini API key to enable AI-powered schema generation. Get your free API key at https://makersuite.google.com/app/apikey"
)

# Input mode selection
input_mode = st.radio(
    "Select Input Mode:",
    ["Text Input", "URL Input"],
    help="Choose whether to paste text directly or fetch content from a URL"
)

# Dynamic placeholder based on schema type
placeholders = {
    "FAQPage": """What is Schema.org?
Schema.org is a collaborative initiative to create structured data schemas for the web.

Why use structured data?
Structured data helps search engines understand your content better and can improve your search appearance.""",
    "Article": """Title: Understanding Schema.org
Author: John Doe
Published: 2024-01-15
Description: A comprehensive guide to understanding and implementing Schema.org structured data.
Content: Schema.org is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet...""",
    "Product": """Product Name: Wireless Bluetooth Headphones
Description: Premium wireless headphones with noise cancellation
Brand: TechAudio
Price: 149.99
Currency: USD
Availability: In Stock
Rating: 4.5 out of 5
Reviews: 250""",
    "Breadcrumb": """Home > Electronics > Audio > Headphones
or
Home (https://example.com) > Electronics (https://example.com/electronics) > Headphones (https://example.com/electronics/headphones)""",
    "LocalBusiness": """Business Name: Joe's Coffee Shop
Description: Artisan coffee and fresh pastries in downtown
Address: 123 Main Street, Springfield, IL 62701, USA
Phone: (555) 123-4567
Hours: Monday-Friday 7AM-6PM, Saturday-Sunday 8AM-5PM
Price Range: $$""",
    "HowTo": """How to Make French Press Coffee

This guide will teach you how to make perfect French press coffee at home.

Step 1: Boil water to 200°F
Step 2: Add coarsely ground coffee to the French press (2 tablespoons per cup)
Step 3: Pour hot water over the grounds and stir
Step 4: Place the lid on and let it steep for 4 minutes
Step 5: Slowly press down the plunger
Step 6: Pour and enjoy immediately""",
    "Recipe": """Recipe Name: Classic Chocolate Chip Cookies
Author: Chef Sarah
Description: Soft and chewy chocolate chip cookies that everyone loves
Prep Time: 15 minutes
Cook Time: 12 minutes
Servings: 24 cookies

Ingredients:
- 2 1/4 cups all-purpose flour
- 1 tsp baking soda
- 1 cup butter, softened
- 3/4 cup sugar
- 2 eggs
- 2 cups chocolate chips

Instructions:
1. Preheat oven to 375°F
2. Mix flour and baking soda in a bowl
3. Cream together butter and sugar
4. Beat in eggs one at a time
5. Gradually blend in flour mixture
6. Stir in chocolate chips
7. Drop rounded tablespoons onto baking sheet
8. Bake for 9-11 minutes until golden brown""",
    "Person": """Name: Dr. Jane Smith
Job Title: Chief Technology Officer
Description: Software engineer and technology leader with 15 years of experience in cloud computing and AI
Email: jane.smith@example.com
Phone: (555) 987-6543
Location: San Francisco, CA, USA
Website: https://janesmith.dev"""
}

# Content input based on selected mode
content_input = ""
url_input = ""

if input_mode == "Text Input":
    content_input = st.text_area(
        f"Enter {schema_type} Content (AI will extract and structure the information):",
        height=250,
        placeholder=placeholders.get(schema_type, ""),
        key="content_input"
    )
else:  # URL Input
    url_input = st.text_input(
        "Enter URL to fetch content from:",
        placeholder="https://example.com/page",
        help="Paste a URL and the app will fetch the content, then use Gemini AI to extract relevant information for the selected schema type",
        key="url_input"
    )

# Format selection
col1, col2 = st.columns(2)
with col1:
    format_option = st.radio(
        "Select Output Format:",
        ["JSON-LD", "HTML Microdata"],
        key="format_option"
    )

# Generate button
if st.button("Generate Schema", type="primary"):
    # Validate inputs based on mode
    if input_mode == "Text Input" and not content_input.strip():
        st.error("Please enter some content to generate schema.")
    elif input_mode == "URL Input" and not url_input.strip():
        st.error("Please enter a URL to fetch content from.")
    elif not api_key:
        st.error("Please provide a Google Gemini API key for AI-powered schema generation.")
    else:
        # Fetch content from URL if in URL mode
        final_content = content_input
        if input_mode == "URL Input":
            with st.spinner("Fetching content from URL..."):
                fetched_content, fetch_error = fetch_url_content(url_input)
                if fetch_error:
                    st.error(fetch_error)
                    st.stop()
                else:
                    final_content = fetched_content
                    st.success("✅ Successfully fetched content from URL")
                    with st.expander("View fetched content"):
                        st.text_area("Fetched Content", final_content, height=200, disabled=True)
        
        with st.spinner(f"Using AI to generate {schema_type} schema..."):
            data, error = generate_schema_with_ai(final_content, schema_type, api_key)
            
            if error:
                st.error(f"Schema generation failed: {error}")
            elif not data:
                st.error("Could not generate schema. Please check your input and try again.")
            else:
                st.info(f"✨ AI successfully generated {schema_type} schema")
                st.header("Generated Schema Output")
                
                if format_option == "JSON-LD":
                    output = generate_json_ld(data, schema_type)
                else:
                    output = generate_microdata(data, schema_type)
                
                # Display output in a code block
                st.code(output, language="json" if format_option == "JSON-LD" else "html")
                
                # Download button
                st.download_button(
                    label="📋 Download Schema",
                    data=output,
                    file_name=f"{schema_type.lower()}_schema.{'json' if format_option == 'JSON-LD' else 'html'}",
                    mime="application/json" if format_option == "JSON-LD" else "text/html"
                )
                
                st.success(f"✅ Generated {schema_type} schema successfully")

# Example section
st.markdown("---")
st.subheader("💡 Example Input Formats by Schema Type")

with st.expander("FAQPage Examples"):
    st.markdown("""
```
What is your return policy?
We accept returns within 30 days of purchase with original receipt.

Do you offer international shipping?
Yes, we ship to over 100 countries worldwide.
```
""")

with st.expander("Article Examples"):
    st.markdown("""
```
Title: The Ultimate Guide to Coffee Brewing
Author: John Coffee
Published: 2024-01-15
Description: Learn professional coffee brewing techniques
Content: Coffee brewing is an art and science...
```
""")

with st.expander("Product Examples"):
    st.markdown("""
```
Product: Premium Wireless Headphones
Description: Studio-quality sound with active noise cancellation
Brand: AudioPro
Price: 299.99 USD
In Stock
4.8 stars from 1250 reviews
```
""")

with st.expander("Breadcrumb Examples"):
    st.markdown("""
```
Home > Products > Electronics > Headphones
or
Home (/) > Shop (/shop) > Headphones (/shop/headphones)
```
""")

with st.expander("LocalBusiness Examples"):
    st.markdown("""
```
Business: The Coffee House
Description: Artisan coffee and homemade pastries
Address: 456 Oak Street, Portland, OR 97201, USA
Phone: (503) 555-1234
Hours: Mon-Fri 6AM-8PM, Sat-Sun 7AM-9PM
$$
```
""")

with st.expander("HowTo Examples"):
    st.markdown("""
```
How to Change a Tire

Learn how to safely change a flat tire in 6 easy steps.

1. Park on a flat surface and engage parking brake
2. Loosen the lug nuts slightly
3. Jack up the vehicle
4. Remove the lug nuts and tire
5. Mount the new tire and hand-tighten lug nuts
6. Lower vehicle and fully tighten lug nuts
```
""")

with st.expander("Recipe Examples"):
    st.markdown("""
```
Perfect Chocolate Cake
By Chef Maria
A rich, moist chocolate cake that's perfect for any occasion

Prep: 20 minutes
Bake: 35 minutes
Serves: 12

Ingredients:
- 2 cups all-purpose flour
- 2 cups sugar
- 3/4 cup cocoa powder
- 2 eggs
- 1 cup milk
- 1/2 cup vegetable oil

Steps:
1. Preheat oven to 350°F
2. Mix dry ingredients
3. Add wet ingredients and beat well
4. Pour into greased pan
5. Bake for 35 minutes
```
""")

with st.expander("Person Examples"):
    st.markdown("""
```
Dr. Emily Chen
Chief Data Scientist
Award-winning data scientist specializing in machine learning and AI ethics
Email: emily.chen@example.com
Phone: (415) 555-7890
Based in: Seattle, WA, USA
Website: https://emilychen.ai
```
""")

# Footer with information
st.markdown("---")
with st.expander("ℹ️ About Schema.org Structured Data"):
    st.markdown("""
    ### Benefits of Schema.org Structured Data
    
    Adding structured data to your website can:
    - Improve search engine understanding of your content
    - Enable rich results in Google Search (rich snippets, knowledge panels, etc.)
    - Increase click-through rates from search results
    - Enhance your content's discoverability
    - Provide better context for voice assistants and AI
    
    ### Supported Schema Types
    
    This tool supports the following Schema.org types:
    - **FAQPage**: Frequently Asked Questions pages
    - **Article**: News articles, blog posts, or other written content
    - **Product**: Products for sale with pricing and availability
    - **BreadcrumbList**: Navigation breadcrumb trails
    - **LocalBusiness**: Physical business locations
    - **HowTo**: Step-by-step instructions and guides
    - **Recipe**: Cooking recipes with ingredients and instructions
    - **Person**: Information about people (authors, professionals, etc.)
    
    ### AI-Powered Generation
    
    With a Google Gemini API key, you can:
    - Paste content in any natural format
    - AI automatically extracts and structures the relevant information
    - No need to manually format your input
    - Get your free API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
    
    ### How to Use the Generated Schema
    
    **For JSON-LD:**
    1. Copy the generated JSON-LD code
    2. Add it to your HTML page within a `<script type="application/ld+json">` tag
    3. Place it in the `<head>` or `<body>` section of your page
    
    **For HTML Microdata:**
    1. Copy the generated HTML code
    2. Replace your existing HTML with this microdata-enhanced version
    3. Ensure the structure matches your page layout
    
    ### Testing Your Schema
    
    After implementing, test your schema with:
    - [Google Rich Results Test](https://search.google.com/test/rich-results)
    - [Schema.org Validator](https://validator.schema.org/)
    """)
