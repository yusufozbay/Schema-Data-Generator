# Schema Data Generator

A Streamlit web application that generates Schema.org structured data (JSON-LD and HTML Microdata) from user input content. Perfect for creating FAQPage schema markup that improves your content's visibility in search engines.

## Features

- ✨ **AI-Powered Parsing**: Use Google Gemini AI to automatically extract Q&A pairs from any format
- 🎯 **Multiple Formats**: Generate both JSON-LD and HTML Microdata formats
- 📥 **Download Schema**: Download generated schema as a file
- 🎨 **Modern UI**: Clean, responsive Streamlit interface
- ⚡ **Fast**: Built with Streamlit for instant results
- 🔄 **Flexible Input**: No need for Q:/A: prefixes with AI mode

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

1. **Get a Gemini API Key (Optional but Recommended)**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a free API key
   - Copy the key for use in the app

2. **Enter Your FAQ Content**: 
   - **With AI (Recommended)**: Simply paste your Q&A content in any format. The AI will automatically detect questions and answers:
     ```
     What is your return policy?
     We accept returns within 30 days of purchase with original receipt.

     Do you offer international shipping?
     Yes, we ship to over 100 countries worldwide.
     ```
   
   - **Without AI**: Use the traditional format with Q: and A: prefixes:
     ```
     Q: Your question here?
     A: Your answer here.

     Q: Another question?
     A: Another answer.
     ```

3. **Select Format**: Choose between:
   - **JSON-LD**: JSON format that can be embedded in `<script type="application/ld+json">` tags
   - **HTML Microdata**: HTML markup with Schema.org microdata attributes

4. **Generate**: Click the "Generate Schema" button to create your schema markup

5. **Download**: Click "Download Schema" to save the generated schema to a file

## Example

### Input (AI Mode - No prefixes needed):
```
What is your return policy?
We accept returns within 30 days of purchase with original receipt.

Do you offer international shipping?
Yes, we ship to over 100 countries worldwide.
```

### Input (Traditional Mode):
```
Q: What is your return policy?
A: We accept returns within 30 days of purchase with original receipt.

Q: Do you offer international shipping?
A: Yes, we ship to over 100 countries worldwide.
```

### JSON-LD Output:
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
- google-generativeai>=0.3.0 (for AI-powered parsing)
- Google Gemini API key (optional, for AI features)

See `requirements.txt` for full dependency list.

## Schema.org FAQPage Benefits

Adding FAQPage structured data to your website can:
- Improve search engine understanding of your content
- Enable rich results in Google Search with expandable Q&A sections
- Increase click-through rates from search results
- Enhance your content's discoverability

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
- Support for other Schema.org types (HowTo, Article, Product, etc.)
- Validation of generated schema
- Import/Export functionality
- Additional input formats
- Schema templates