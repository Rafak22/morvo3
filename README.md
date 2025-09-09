# MORVO - مساعدك التسويقي الذكي 🤖

MORVO is an AI-powered marketing assistant that helps businesses analyze and improve their online presence. It provides personalized marketing advice, website analysis, and strategic recommendations in Arabic.

## Features

- 💬 Interactive Chat Interface
- 🌐 Website Analysis
- 📊 Marketing Strategy Recommendations
- 🎯 Personalized Advice
- 🔍 SEO Insights
- 📈 Performance Metrics

## Technologies Used

- Frontend: Streamlit
- Backend: FastAPI
- AI: OpenAI GPT-4
- Vector Store: ChromaDB
- RAG (Retrieval Augmented Generation)
- Web Scraping: BeautifulSoup4

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/Rafak22/morvo3.git
cd morvo3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
# Start the backend server
uvicorn main:app --reload

# In another terminal, start the Streamlit frontend
streamlit run streamlit_app.py
```

## Deployment

This application is deployed on Streamlit Cloud and can be accessed at: [MORVO App](https://morvo.streamlit.app)

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

MIT License

## Author

- [@Rafak22](https://github.com/Rafak22)
