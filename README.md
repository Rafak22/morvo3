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

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Rafak22/morvo3.git
cd morvo3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with:
```
BACKEND_URL=http://127.0.0.1:8000
OPENAI_API_KEY=your_api_key_here
```

4. Run the application locally:
```bash
# Start the backend server
uvicorn main:app --reload

# In another terminal, start the Streamlit frontend
streamlit run streamlit_app.py
```

## Cloud Deployment

### Backend Deployment (Render.com)

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     - `OPENAI_API_KEY`: Your OpenAI API key

### Frontend Deployment (Streamlit Cloud)

1. Go to share.streamlit.io
2. Connect your GitHub repository
3. Set Environment Variables:
   - `BACKEND_URL`: Your Render.com backend URL (e.g., https://morvo-backend.onrender.com)
   - `OPENAI_API_KEY`: Your OpenAI API key

## Usage

The application will work both locally and in the cloud:
- Locally: Uses http://127.0.0.1:8000 as backend
- Cloud: Uses the BACKEND_URL environment variable

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

MIT License

## Author

- [@Rafak22](https://github.com/Rafak22)