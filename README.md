# 📑 AI-Powered Legal Document Analyzer

An intelligent system that analyzes legal documents using advanced AI to provide summaries, extract key entities, and identify important clauses.

## ✨ Features

- **Document Analysis**: Upload and analyze legal PDF documents
- **Smart Summarization**: Get concise summaries of legal documents using Hugging Face's BART model
- **Entity Extraction**: Identify and extract key legal entities and clauses
- **User-Friendly Interface**: Clean and intuitive Streamlit-based frontend
- **Real-time Processing**: Fast and efficient document processing
- **Error Handling**: Robust error handling and user feedback

## 🚀 Tech Stack

### Backend
- FastAPI - Modern, fast web framework
- PyMuPDF - PDF text extraction
- Hugging Face Transformers - Text summarization and entity extraction
- Python 3.8+

### Frontend
- Streamlit - Interactive web interface
- Requests - API communication

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/vaishalis27/LegalDocumentAnalyser.git
cd LegalDocumentAnalyser
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. Install backend dependencies:
```bash
cd LDA/backend
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd ../frontend
pip install -r requirements.txt
```

5. Set up environment variables:
Create a `.env` file in the `LDA/backend` directory:
```
HF_API_KEY=your_huggingface_api_key_here
```

## 🚀 Running the Application

1. Start the backend server:
```bash
cd LDA/backend
uvicorn main:app --reload
```

2. Start the frontend application:
```bash
cd LDA/frontend
streamlit run app.py
```

3. Open your browser and navigate to:
```
http://localhost:8501
```

## 📝 Usage

1. Upload a legal PDF document using the file uploader
2. Wait for the document to be processed
3. View the generated summary
4. Explore detected entities and clauses
5. Access the raw text preview if needed

## 🔒 Security Features

- File type validation (PDF only)
- File size limits (max 10MB)
- Secure API key handling
- Input validation and sanitization

## 🧪 Testing

The application includes comprehensive error handling for:
- Invalid file types
- File size limits
- Empty or corrupted PDFs
- API connection issues
- Processing errors

## 📊 Performance

- Efficient PDF text extraction
- Optimized text processing
- Asynchronous file handling
- Background task management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for providing the AI models
- FastAPI team for the excellent web framework
- Streamlit team for the beautiful UI framework
- PyMuPDF team for the PDF processing capabilities

## 📞 Support

For support, please open an issue in the GitHub repository or contact 00vaishalisingh00@gmail.com

---

Made with ❤️ by [Vaishali Singh] 