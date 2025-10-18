# Project Report Generator API

A FastAPI-based backend for generating professional project reports with AI assistance.

## Features

- Generate DOCX and PDF reports
- AI-powered abstract and conclusion generation
- Text improvement and rewording
- Plagiarism checking (requires external API key)
- Multiple formatting styles (IEEE, Springer)
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API key (for AI features)
- (Optional) Plagiarism checking API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapi-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the API keys in `.env`

## Running the Application

1. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at:
   - Main endpoint: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

## API Endpoints

### Report Generation
- `POST /generate-report` - Generate a report in DOCX and PDF formats
- `GET /download/{filename}` - Download a generated file

### AI Features
- `POST /ai/abstract` - Generate an abstract
- `POST /ai/conclusion` - Generate a conclusion
- `POST /ai/reword` - Improve text grammar and flow
- `POST /ai/synopsis` - Generate a 2-page summary
- `POST /ai/plagiarism` - Check text for plagiarism

## Deployment

### Production Deployment with Gunicorn

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t report-generator .
   ```

2. Run the container:
   ```bash
   docker run -d --name report-generator -p 8000:8000 --env-file .env report-generator
   ```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| GEMINI_API_KEY | Google Gemini API key | Yes | - |
| PLAGIARISM_API_KEY | Plagiarism checking API key | No | - |
| PORT | Port to run the server on | No | 8000 |
| ENVIRONMENT | Application environment | No | development |
| UPLOAD_FOLDER | Directory to store uploaded files | No | ./uploads |
| OUTPUT_FOLDER | Directory to store generated files | No | ./output |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
