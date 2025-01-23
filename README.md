### Project Overview

**Platform Development:**
Using **Streamlit**, I developed an interactive platform where users can search for air fryer models and access detailed information about their appliances, including price, total score, power consumption, and energy label. For highly energy-efficient models (A++, A+, or A), the platform informs users there is no need for replacement. For less efficient models, it provides recommendations based on higher total scores, lower power consumption, and lower prices, along with tags that highlight why these recommendations are better. The platform also calculates payback periods and monthly savings after the payback period, allowing users to assess the financial benefits of switching to a more efficient model. Recommendations are enriched with extra features like being dishwasher-safe or having a transparent lid if the selected model lacks these functionalities.

**Web Scraping with Selenium:**
To gather data from **Bol.com**, I used **Selenium** to automate web scraping tasks. This included handling cookie prompts, dynamically loading content (e.g., specifications and reviews), and ensuring all reviews were fully extracted by interacting with the "Show More" button. Key product details such as model name, price, images, and pros/cons were scraped and saved into structured CSV files for efficient data management. I implemented a timeout mechanism to avoid prolonged processing on problematic URLs. Additionally, user reviews, primarily in Dutch, were translated into English using **Google Translate**, allowing analysis in a more accessible language.

**NLP for Review Analysis:**
I used **spaCy** for natural language processing (NLP) tasks such as extracting important keywords, sentiment analysis, and detecting common themes or issues in the reviews. For deeper review analysis, I leveraged **GPT-3.5** to identify key insights, such as frequently mentioned pros and cons, customer satisfaction trends, and feature-specific user sentiments. This enhanced the platform's ability to highlight what users valued most about specific models, adding a richer layer to the recommendations.

**Interactive Data Visualization with Plotly:**
Interactive charts created using **Plotly** visualize the cost comparison of appliances under various energy providers, showing how switching providers can reduce the annual energy costs of appliances. These visualizations also integrate solar panel savings calculations, enabling users to assess the potential impact of renewable energy adoption. Each chart includes shortened appliance names, and labels identify the highest score, lowest score, and the currently searched appliance.

Challenges and Solutions:
1. **Translation of Reviews:** Translating Dutch reviews into English for NLP analysis introduced some inaccuracies and loss of nuance. However, combining **spaCy** and **GPT-3.5** mitigated these limitations by identifying meaningful insights from the translated text.
2. **Data Completeness and Accuracy:** To ensure accurate recommendations, I implemented data validation techniques and provided fallback options for incomplete datasets.
3. **Energy Cost Transparency:** Predefined tariffs may not fully reflect user-specific contracts. Adding customizable tariff inputs solved this issue, giving users a more tailored analysis.
4. **Algorithm Transparency:** To build trust, the recommendation algorithms were explained within the platform, detailing scoring and prioritization criteria.

 Technologies Used:
- **SQL**: Managed and queried appliance and energy provider data for efficient data retrieval.
- **Python**: Used **Pandas** for data cleaning and manipulation, and **spaCy** with **GPT-3.5** for NLP-driven review analysis.
- **Web Scraping**: Automated data collection from Bol.com using **Selenium**.
- **Plotly**: Created interactive charts for cost and savings visualizations.
- **Streamlit**: Developed a responsive and user-friendly web application interface.
- **Google Translate API**: Translated Dutch reviews into English for analysis.

This project highlights my ability to combine backend development, NLP, data visualization, and web application development to deliver a feature-rich, user-centric platform.
