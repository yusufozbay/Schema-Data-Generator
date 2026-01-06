# Schema Data Generator

A web application that generates Schema.org structured data (JSON-LD and HTML Microdata) from user input content. Perfect for creating FAQPage schema markup that improves your content's visibility in search engines.

## Features

- ✨ **Easy to Use**: Simple textarea input for FAQ content
- 🎯 **Multiple Formats**: Generate both JSON-LD and HTML Microdata formats
- 📋 **Copy to Clipboard**: One-click copying of generated schema
- 🎨 **Modern UI**: Clean, responsive design that works on all devices
- ⚡ **No Build Required**: Pure HTML/CSS/JavaScript - just open and use

## Getting Started

### Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yusufozbay/Schema-Data-Generator.git
   cd Schema-Data-Generator
   ```

2. Open `index.html` in your web browser:
   - Double-click the file, or
   - Right-click and select "Open with" your preferred browser, or
   - Use a local server: `python -m http.server 8000` (then visit http://localhost:8000)

### Usage

1. **Enter Your FAQ Content**: In the input textarea, enter your questions and answers using this format:
   ```
   Q: Your question here?
   A: Your answer here.

   Q: Another question?
   A: Another answer.
   ```

2. **Select Format**: Choose between:
   - **JSON-LD**: JSON format that can be embedded in `<script type="application/ld+json">` tags
   - **HTML Microdata**: HTML markup with Schema.org microdata attributes

3. **Generate**: Click the "Generate Schema" button to create your schema markup

4. **Copy**: Click "Copy to Clipboard" to copy the generated schema for use in your website

## Example

### Input:
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

## Schema.org FAQPage Benefits

Adding FAQPage structured data to your website can:
- Improve search engine understanding of your content
- Enable rich results in Google Search with expandable Q&A sections
- Increase click-through rates from search results
- Enhance your content's discoverability

## Browser Compatibility

Works with all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

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