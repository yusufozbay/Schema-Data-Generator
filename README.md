# Schema Data Generator

A Streamlit web application that generates Schema.org structured data (JSON-LD and HTML Microdata) from user input content. Supports multiple schema types including FAQPage, Article, Product, Breadcrumb, LocalBusiness, HowTo, Recipe, and Person.

## Features

- ✨ **AI-Powered Generation**: Use Google Gemini AI to automatically extract and structure content
- 🌐 **Enhanced URL Fetching**: Paste a URL and automatically fetch content from any web page
  - **Bypasses 403 Errors**: Gemini AI directly accesses URLs, bypassing traditional HTTP restrictions
  - **Intelligent Extraction**: Gemini AI extracts main content while filtering out ads, navigation, and clutter
  - **Fallback Support**: Automatically falls back to traditional HTTP if needed
- 🎯 **8 Schema Types**: Support for FAQPage, Article, Product, Breadcrumb, LocalBusiness, HowTo, Recipe, and Person
- 📊 **Multiple Formats**: Generate both JSON-LD and HTML Microdata formats
- 📥 **Download Schema**: Download generated schema as a file
- 🎨 **Modern UI**: Clean, responsive Streamlit interface with dynamic examples
- ⚡ **Fast**: Built with Streamlit for instant results
- 🔄 **Flexible Input**: Natural language input or URL - AI extracts the structure

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yusufozbay/Schema-Data-Generator.git
   cd Schema-Data-Generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501`

### Usage

1. **Get a Gemini API Key (Required)**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a free API key
   - Copy the key for use in the app

2. **Select Schema Type**: Choose from:
   - **FAQPage**: For frequently asked questions
   - **Article**: For blog posts, news articles, or written content
   - **Product**: For products with pricing and availability
   - **Breadcrumb**: For navigation breadcrumb trails
   - **LocalBusiness**: For physical business locations
   - **HowTo**: For step-by-step instructions
   - **Recipe**: For cooking recipes
   - **Person**: For information about people

3. **Choose Input Mode**:
   - **Text Input**: Paste your content directly in natural language
   - **URL Input**: Paste a URL and the app will automatically fetch the page content

4. **Enter Your Content**: 
   - For **Text Input**: Simply paste your content in natural language. The AI will automatically extract and structure the relevant information based on the selected schema type.
   - For **URL Input**: Paste a URL (e.g., https://example.com/article), and the app will fetch the page content and extract relevant information.

5. **Select Format**: Choose between:
   - **JSON-LD**: JSON format that can be embedded in `<script type="application/ld+json">` tags
   - **HTML Microdata**: HTML markup with Schema.org microdata attributes

6. **Generate**: Click the "Generate Schema" button to create your schema markup

7. **Download**: Click "Download Schema" to save the generated schema to a file

## Example

### Text Input Examples:

#### FAQPage Input:
```
What is your return policy?
We accept returns within 30 days of purchase with original receipt.

Do you offer international shipping?
Yes, we ship to over 100 countries worldwide.
```

### URL Input Examples:

You can also use URL input mode to automatically fetch content from web pages:

- **Article Schema**: Paste a blog post or news article URL
- **Product Schema**: Paste a product page URL  
- **Recipe Schema**: Paste a recipe page URL
- **FAQPage Schema**: Paste an FAQ page URL
- **LocalBusiness Schema**: Paste a business website URL

The app will automatically fetch the page content and use AI to extract relevant information based on your selected schema type.

**How URL Fetching Works:**
1. **Gemini AI Direct Fetch**: First, the app uses Gemini AI to directly fetch and process the URL. Gemini's built-in web access capabilities bypass many 403 Forbidden errors and other access restrictions that traditional HTTP requests encounter.
2. **Intelligent Content Extraction**: Gemini AI intelligently extracts the main content while filtering out navigation menus, advertisements, footers, and other non-essential elements.
3. **Fallback Mechanism**: If the Gemini method encounters issues, the app automatically falls back to traditional HTTP requests with enhanced headers for maximum compatibility.

This dual approach ensures reliable content fetching from a wide variety of websites, even those with restrictive access policies.

### Article Input:
```
Title: Understanding Machine Learning
Author: Dr. Sarah Johnson
Published: 2024-01-15
Description: A comprehensive introduction to machine learning concepts
Content: Machine learning is a subset of artificial intelligence that enables systems to learn from data...
```

### Product Input:
```
Product: Wireless Bluetooth Headphones
Description: Premium headphones with active noise cancellation
Brand: AudioPro
Price: 149.99 USD
In Stock
Rating: 4.5 stars, 320 reviews
```

### Recipe Input:
```
Classic Chocolate Chip Cookies
By Chef Maria
Soft and chewy cookies perfect for any occasion

Prep: 15 minutes
Bake: 12 minutes
Serves: 24

Ingredients:
- 2 cups flour
- 1 cup butter
- 2 eggs
- 2 cups chocolate chips

Steps:
1. Preheat oven to 375°F
2. Mix dry ingredients
3. Add wet ingredients
4. Fold in chocolate chips
5. Bake for 12 minutes
```

### JSON-LD Output (FAQPage):
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is your return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We accept returns within 30 days of purchase with original receipt."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer international shipping?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we ship to over 100 countries worldwide."
      }
    }
  ]
}
```

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app" and select this repository
5. Set the main file path to `app.py`
6. Click "Deploy"

### Local Development

For local development with auto-reload:
```bash
streamlit run app.py
```

## Requirements

- Python 3.8+
- streamlit>=1.28.0
- google-generativeai>=0.3.0
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- Google Gemini API key (required for AI-powered schema generation)

See `requirements.txt` for full dependency list.

## Schema.org Benefits

Adding structured data to your website can:
- Improve search engine understanding of your content
- Enable rich results in Google Search (FAQ dropdowns, recipe cards, product info, etc.)
- Increase click-through rates from search results
- Enhance your content's discoverability
- Provide better context for voice assistants and AI

## Supported Schema Types

- **FAQPage**: Frequently asked questions with rich result support in Google Search
- **Article**: News articles, blog posts, or other written content
- **Product**: Products with pricing, availability, and rating information
- **BreadcrumbList**: Navigation breadcrumb trails for better site structure
- **LocalBusiness**: Physical business locations with contact and hours information
- **HowTo**: Step-by-step instructions and guides
- **Recipe**: Cooking recipes with ingredients, instructions, and timing
- **Person**: Information about individuals (authors, professionals, etc.)

## Technology Stack

- **Streamlit**: Modern Python framework for building web apps
- **Python**: Core logic and schema generation
- **Google Gemini AI**: Advanced AI for intelligent Q&A extraction
- **JSON**: Data interchange format for JSON-LD schemas

## License

MIT License - feel free to use this tool for any purpose.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

Potential features for future versions:
- Validation of generated schema
- Import/Export functionality  
- Additional Schema.org types (Event, Organization, VideoObject, etc.)
- Schema editing interface
- Batch processing for multiple schemas