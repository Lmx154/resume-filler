# 📝 Resume Filler

Resume Filler is a local, privacy-focused tool designed to streamline job applications by auto-filling forms using data extracted from your resume. Leveraging AI, it processes your resume and scraped job application data securely on your machine, offering customizable enhancements tailored to specific job requirements.

## ✨ Features

- 🔒 **Local Processing**: All data remains on your computer, ensuring privacy and security
- 🤖 **AI-Powered Auto-Fill**: Uses AI (via OpenAI or Ollama) to generate responses for job application forms based on your resume
- 📄 **Resume Parsing**: Upload resumes in PDF, DOCX, or TXT formats to extract structured data
- 🎯 **Application Enhancement**: Customize responses with options like clarity, professional tone, keyword optimization, or achievement focus
- ⚙️ **Configurable Settings**: Supports OpenAI API integration or local Ollama models for offline processing
- 💅 **User-Friendly Interface**: Built with Tailwind CSS and Vite for a modern, responsive frontend

## 🚀 Installation

### Prerequisites

- Node.js (v18+ recommended) for the frontend
- Python (v3.9+) for the backend
- Git to clone the repository
- Optional: Ollama for local AI processing (COMING SOON!)

### Steps

1. Clone the Repository
```bash
git clone https://github.com/lmx154/lmx154-resume-filler.git
cd lmx154-resume-filler
```

2. Set Up the Frontend
```bash
npm install
npm run dev
```

3. Set Up the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Configure Environment
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
```

5. Start the Backend
```bash
uvicorn main:app --reload --port 8000
```

## 📖 Usage

### 🚀 Launch the Application
1. Start both frontend and backend servers
2. Open your browser to `http://localhost:5173`

### 📤 Upload a Resume
1. Navigate to Resume > Upload Resume
2. Upload a PDF, DOCX, or TXT file

### 📝 Upload Job Application Data
1. Go to Application > Upload Application
2. Upload scraped job application data

### ✨ Enhance Application
1. Select Application > Enhance Application
2. Configure enhancement options
3. Review AI-generated responses

### ⚙️ Configure Settings
- Configure OpenAI credentials under Settings > API Key
- Set up Ollama under Settings > Ollama for local processing

## 🏗️ Technical Architecture

### Directory Structure
```
lmx154-resume-filler/
├── index.html          # Frontend entry point
├── main.js            # Core frontend logic
├── package.json       # Frontend dependencies
├── postcss.config.js  # PostCSS configuration
├── style.css         # Custom styles
├── tailwind.config.js # Tailwind configuration
└── backend/          # Backend FastAPI application
    ├── config.py
    ├── main.py
    ├── requirements.txt
    ├── models/
    ├── routes/
    └── services/
```

### 🛠️ Technology Stack
- Frontend: Vite, JavaScript, Tailwind CSS
- Backend: FastAPI, Python, Pydantic
- AI: OpenAI API or Ollama (local LLM support comin soon!)
- File Handling: PyPDF2, python-docx

### 🔌 API Endpoints
- `GET /api/resume/upload`: Retrieve last uploaded resume
- `POST /api/resume/upload`: Upload and parse resume
- `POST /api/application/extract`: Process application text
- `POST /api/application/enhance`: Generate responses
- `GET /api/settings/openai`: Fetch OpenAI settings
- `POST /api/settings/openai`: Update OpenAI settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## 💡 Development Tips

- Use `npm run dev` and `uvicorn main:app --reload --port 8000` for live reload
- Test API endpoints with Postman or curl
- Maintain consistent code formatting

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- Built with ❤️ by Luis


Questions? Open an issue.