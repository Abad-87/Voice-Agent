=======
# Healthcare Voice AI System

A fully deployable, production-ready Healthcare Voice AI system built with FastAPI, featuring speech-to-text, text-to-speech, symptom assessment, appointment management, and comprehensive safety guardrails.

## 🚀 Features

### Core Voice AI
- **Speech-to-Text**: Multi-language support (English + Hindi) using Deepgram
- **Text-to-Speech**: Empathetic voice synthesis with ElevenLabs
- **Natural Conversations**: Context-aware responses with interruption handling
- **Low Latency**: Optimized for real-time interactions

### Healthcare Features
- **Symptom Understanding**: Non-diagnostic assessment with urgency classification
- **Appointment Management**: Book, reschedule, cancel appointments with calendar integration
- **Medication Support**: Reminders and refill alerts (no dosage decisions)
- **Remote Monitoring**: Daily health check-ins with trend analysis
- **Clinical Documentation**: Voice dictation to structured SOAP notes
- **Mental Health Support**: Crisis detection and resource referral
- **Emergency Detection**: Real-time escalation for critical symptoms

### Safety & Compliance
- **Medical Disclaimers**: Always included in responses
- **No Diagnosis/Prescription**: Strict enforcement of healthcare boundaries
- **Indian Healthcare Compliance**: Follows local regulations
- **Emergency Protocols**: Immediate escalation for critical situations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Voice Input   │ -> │   STT (Deepgram)│ -> │   LLM (Grok)    │
│   (Audio)       │    │                 │    │   Processing    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│   TTS (Eleven)  │ <- │   Safety        │ <- ┌─────────────────┐
│   (Audio)       │    │   Guardrails    │    │   Response      │
└─────────────────┘    └─────────────────┘    │   Generation    │
                                              └─────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Database Layer                            │
│   PostgreSQL + Redis for data storage and caching          │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + Redis
- **AI Models**: Grok Fast (LLM), Deepgram (STT), ElevenLabs (TTS)
- **Authentication**: JWT-based user authentication
- **Deployment**: Docker + Docker Compose
- **Task Queue**: Celery for background jobs
- **Monitoring**: Health checks and logging

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- API Keys for:
  - ElevenLabs (TTS)
  - Deepgram (STT)
  - Twilio (SMS reminders)
  - Google Calendar (optional)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd healthcare-voice-ai
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` with your API keys and configuration:
```bash
# Required API Keys
ELEVENLABS_API_KEY=your-elevenlabs-key
DEEPGRAM_API_KEY=your-deepgram-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### 3. Deploy with Docker
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec healthcare-voice-ai alembic upgrade head

# Or manually initialize
docker-compose exec healthcare-voice-ai python -c "
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('Database initialized')
"
```

### 5. Setup Ollama (LLM)
```bash
# Pull the required model
docker-compose exec ollama ollama pull phi

# Verify model is loaded
docker-compose exec ollama ollama list
```

## 📖 API Usage

### Authentication
```bash
# Register a new user
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "securepassword",
    "full_name": "John Doe",
    "phone": "+1234567890"
  }'

# Login to get access token
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=patient@example.com&password=securepassword"
```

### Voice Chat
```bash
# Upload audio file for voice chat
curl -X POST "http://localhost:8000/voice-chat" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "audio_file=@audio.wav"
```

### Appointment Management
```bash
# Book an appointment
curl -X POST "http://localhost:8000/appointments" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_name": "Dr. Smith",
    "specialty": "Cardiology",
    "appointment_datetime": "2024-01-15T10:00:00",
    "notes": "Follow-up visit"
  }'

# Get appointments
curl -X GET "http://localhost:8000/appointments" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT signing key (change in production)
- `OLLAMA_URL`: Ollama API endpoint
- `ELEVENLABS_API_KEY`: ElevenLabs API key for TTS
- `DEEPGRAM_API_KEY`: Deepgram API key for STT
- `TWILIO_*`: Twilio credentials for SMS
- `GOOGLE_CALENDAR_CREDENTIALS`: Path to Google Calendar credentials

### Voice Configuration
- **STT**: Deepgram with fallback to faster-whisper
- **TTS**: ElevenLabs with fallback to Piper
- **Languages**: English (primary), Hindi support
- **Voice**: Empathetic female voice (customizable)

## 🏥 Healthcare Safety Features

### Symptom Assessment
- **Urgency Levels**: Emergency, Medium, Low
- **Keywords Detection**: Automatic emergency flagging
- **Follow-up Questions**: Structured symptom gathering
- **Disclaimer Integration**: Every response includes medical disclaimer

### Emergency Protocols
- **Immediate Escalation**: Critical symptoms trigger emergency response
- **Resource Referral**: Direct to emergency services
- **Conversation Stop**: Auto-termination for safety

### Compliance
- **No Diagnosis**: Strict prohibition on medical diagnosis
- **No Prescriptions**: Medication guidance limited to reminders
- **Doctor Referral**: Always recommend professional consultation
- **Data Privacy**: HIPAA-compliant data handling

## 📊 Monitoring & Logging

### Health Checks
```bash
# Service health check
curl http://localhost:8000/health

# Individual service checks
docker-compose ps
```

### Logs
```bash
# View application logs
docker-compose logs healthcare-voice-ai

# View all service logs
docker-compose logs
```

### Metrics
- **Celery Flower**: http://localhost:5555
- **API Documentation**: http://localhost:8000/docs
- **Health Dashboard**: Integrated health monitoring

## 🧪 Testing

### Unit Tests
```bash
# Run tests
docker-compose exec healthcare-voice-ai pytest

# Run with coverage
docker-compose exec healthcare-voice-ai pytest --cov=. --cov-report=html
```

### Integration Tests
```bash
# Test voice pipeline
python test_voice_pipeline.py

# Test healthcare logic
python test_healthcare_features.py
```

## 🚀 Production Deployment

### Cloud Deployment
```bash
# Build for production
docker build -t healthcare-voice-ai:latest .

# Deploy to cloud (example with AWS)
# 1. Push image to ECR
# 2. Deploy with ECS/Fargate
# 3. Configure load balancer
# 4. Set up RDS (PostgreSQL) and ElastiCache (Redis)
```

### Scaling Considerations
- **Horizontal Scaling**: Multiple app instances behind load balancer
- **Database**: Read replicas for high traffic
- **Redis**: Cluster mode for high availability
- **Voice Processing**: Async processing with Celery workers

### Security
- **API Keys**: Store in AWS Secrets Manager or similar
- **Database**: Encrypted at rest and in transit
- **Network**: VPC isolation with security groups
- **Monitoring**: CloudWatch alarms and logging

## 📝 Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload

# Run Celery worker
celery -A tasks worker --loglevel=info
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system is designed to assist with healthcare management but is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.

## 📞 Support

For support and questions:
- Email: support@healthcare-voice-ai.com
- Documentation: https://docs.healthcare-voice-ai.com
- Issues: GitHub Issues

---

**Built with ❤️ for safer, more accessible healthcare**
