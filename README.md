# Kaution2Invest

Kaution2Invest is a Streamlit application that helps Swiss renters visualize how their rental deposit could grow if invested over time, compared to leaving it as a standard 0% deposit.

## Features

- Input fields for monthly rent, deposit duration, and expected return rate
- Comparison table showing investment growth over different time horizons
- Interactive visualization chart comparing 0% return vs. investment return
- Multilingual support (German and English)

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## Requirements

- Streamlit 1.30.0 or higher (uses the `st.query_params` API)

## Embedding in a Website

The application can be embedded in a website using an iframe. It also supports language synchronization with the parent website.

### Basic Embedding

```html
<iframe src="https://your-streamlit-app-url" width="100%" height="800" frameborder="0"></iframe>
```

### Language Synchronization

The app can detect and use the language of the parent website by passing a language parameter in the URL:

```html
<iframe src="https://your-streamlit-app-url/?lang=de" width="100%" height="800" frameborder="0"></iframe>
```

#### Supported Languages

The application currently supports the following languages with their exact parameter values:

| Language | Parameter Value | Example URL                                |
|----------|----------------|-------------------------------------------|
| German   | `de`           | `https://your-streamlit-app-url/?lang=de` |
| English  | `en`           | `https://your-streamlit-app-url/?lang=en` |

**Important Notes:**
- The parameter values are case-sensitive and must be lowercase (`de`, not `DE` or `De`)
- If an unsupported language code is provided, the app will default to German
- If no language parameter is provided, the app will default to German

You can dynamically change the language by updating the iframe src:

```javascript
// Change the Streamlit app language to match your website language
function updateAppLanguage(lang) {
    document.getElementById('streamlit-iframe').src = `https://your-streamlit-app-url/?lang=${lang}`;
}
```

See the included `embed_example.html` for a complete implementation example.

## Example Scenario

For a monthly rent of 1,800 CHF with a 3-month deposit (5,400 CHF total):

- At 0% return: Your deposit remains 5,400 CHF forever
- At 3% annual return: After 7 years (average Swiss rental duration), your deposit could grow to approximately 6,700 CHF

## Contributing

Feel free to submit issues or pull requests with improvements.

