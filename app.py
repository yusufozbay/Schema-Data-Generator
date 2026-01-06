import streamlit as st
import json

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

def generate_json_ld(faqs):
    """Generate JSON-LD schema for FAQPage."""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq['question'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq['answer']
                }
            }
            for faq in faqs
        ]
    }
    return json.dumps(schema, indent=2)

def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def generate_microdata(faqs):
    """Generate HTML microdata for FAQPage."""
    html = '<div itemscope itemtype="https://schema.org/FAQPage">\n'
    
    for faq in faqs:
        html += '  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">\n'
        html += f'    <h3 itemprop="name">{escape_html(faq["question"])}</h3>\n'
        html += '    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">\n'
        html += f'      <div itemprop="text">{escape_html(faq["answer"])}</div>\n'
        html += '    </div>\n'
        html += '  </div>\n'
    
    html += '</div>'
    return html

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
st.header("Input Your Content")

# FAQ input
faq_input = st.text_area(
    "Enter FAQ Questions and Answers (one Q&A pair per section, separated by blank lines):",
    height=200,
    placeholder="""Q: What is Schema.org?
A: Schema.org is a collaborative initiative to create structured data schemas for the web.

Q: Why use structured data?
A: Structured data helps search engines understand your content better and can improve your search appearance.""",
    key="faq_input"
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
    if not faq_input.strip():
        st.error("Please enter some FAQ content to generate schema.")
    else:
        faqs = parse_faq_input(faq_input)
        
        if len(faqs) == 0:
            st.error("Could not parse FAQ content. Please make sure to format your input with 'Q:' and 'A:' prefixes.")
        else:
            st.header("Generated Schema Output")
            
            if format_option == "JSON-LD":
                output = generate_json_ld(faqs)
            else:
                output = generate_microdata(faqs)
            
            # Display output in a code block
            st.code(output, language="json" if format_option == "JSON-LD" else "html")
            
            # Copy button
            st.download_button(
                label="📋 Download Schema",
                data=output,
                file_name=f"schema.{'json' if format_option == 'JSON-LD' else 'html'}",
                mime="application/json" if format_option == "JSON-LD" else "text/html"
            )
            
            st.success(f"✅ Generated schema for {len(faqs)} FAQ(s)")

# Example section
st.markdown("---")
st.subheader("💡 Example Input Format")
st.markdown("""
<div class="example-box">
<pre>Q: What is your return policy?
A: We accept returns within 30 days of purchase with original receipt.

Q: Do you offer international shipping?
A: Yes, we ship to over 100 countries worldwide.

Q: How long does delivery take?
A: Standard delivery takes 3-5 business days, express delivery 1-2 days.</pre>
</div>
""", unsafe_allow_html=True)

# Footer with information
st.markdown("---")
with st.expander("ℹ️ About Schema.org FAQPage"):
    st.markdown("""
    ### Benefits of FAQPage Structured Data
    
    Adding FAQPage structured data to your website can:
    - Improve search engine understanding of your content
    - Enable rich results in Google Search with expandable Q&A sections
    - Increase click-through rates from search results
    - Enhance your content's discoverability
    
    ### How to Use the Generated Schema
    
    **For JSON-LD:**
    1. Copy the generated JSON-LD code
    2. Add it to your HTML page within a `<script type="application/ld+json">` tag
    3. Place it in the `<head>` or `<body>` section of your page
    
    **For HTML Microdata:**
    1. Copy the generated HTML code
    2. Replace your existing FAQ HTML with this microdata-enhanced version
    3. Ensure the structure matches your page layout
    """)
