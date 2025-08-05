# KM PyAPI Framework

A lightweight FastAPI-inspired REST API framework with automatic validation, built-in security, and OpenAPI documentation.

**Author:** [KM Fazle Rabbi](https://kmfazle.dev)  
**GitHub:** [@km-fazle](https://github.com/km-fazle)  
**LinkedIn:** [km-fazle](https://linkedin.com/in/km-fazle)

## Installation

### From PyPI (Recommended)
```bash
pip install km-pyapi
```

### From Source
```bash
git clone https://github.com/km-fazle/Python-API-Framework.git
cd Python-API-Framework
pip install -e .
```

## Features

- 🚀 **FastAPI-based**: Built on top of FastAPI for high performance
- 🔐 **JWT Authentication**: Secure token-based authentication
- 📝 **Automatic Validation**: Request/response validation with Pydantic
- 📚 **OpenAPI Documentation**: Auto-generated API docs at `/docs`
- 🗄️ **SQLAlchemy ORM**: Database integration with SQLAlchemy
- 🧪 **Comprehensive Testing**: Full test suite with pytest
- 🔧 **Easy Configuration**: Environment-based configuration
- 🛡️ **Security**: Password hashing, CORS, and input validation
- 📦 **Production Ready**: Proper packaging and deployment setup

## Quick Start

### Installation

1. Install the package:
```bash
pip install km-pyapi
```

2. Create a new project directory:
```bash
mkdir my-api-project
cd my-api-project
```

3. Set up environment variables (optional):
```bash
# Create .env file with your configuration
echo "DATABASE_URL=sqlite:///./app.db" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
```

### Running the Application

#### Development Mode
```bash
km-pyapi --reload
```

#### Production Mode
```bash
km-pyapi --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/token` | Login and get access token |
| GET | `/api/v1/auth/me` | Get current user info |
| GET | `/api/v1/auth/users` | Get all users (admin) |

### Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/items/` | Get all items |
| POST | `/api/v1/items/` | Create new item |
| GET | `/api/v1/items/my-items` | Get user's items |
| GET | `/api/v1/items/{id}` | Get specific item |
| PUT | `/api/v1/items/{id}` | Update item |
| DELETE | `/api/v1/items/{id}` | Delete item |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/api/v1/health` | API health check |

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword123"
```

### 3. Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My First Item",
       "description": "This is a description of my item"
     }'
```

### 4. Get All Items

```bash
curl -X GET "http://localhost:8000/api/v1/items/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Configuration

The framework uses Pydantic settings for configuration. You can configure it through environment variables or a `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./app.db

# JWT Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=KM PyAPI Framework

# CORS
BACKEND_CORS_ORIGINS=["*"]

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Development

### Running Tests

If you're developing the framework:

```bash
# Clone the repository
git clone https://github.com/km-fazle/Python-API-Framework.git
cd Python-API-Framework

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=py_api_framework
```

## Project Structure

```
py_api_framework/
├── py_api_framework/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── auth.py              # Authentication logic
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/
│       ├── __init__.py      # Routers package
│       ├── auth.py          # Authentication routes
│       └── items.py         # Items routes
├── tests/
│   ├── __init__.py          # Tests package
│   ├── test_auth.py         # Authentication tests
│   └── test_items.py        # Items tests
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
└── README.md               # This file
```

## Database

The framework uses SQLAlchemy with SQLite by default. For production, you can switch to PostgreSQL or MySQL by updating the `DATABASE_URL` in your configuration.

### Database Models

- **User**: Authentication and user management
- **Item**: Main business entity with ownership

## Security Features

- **JWT Tokens**: Secure authentication with configurable expiration
- **Password Hashing**: Bcrypt-based password hashing
- **CORS Protection**: Configurable CORS middleware
- **Input Validation**: Automatic request validation with Pydantic
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install km-pyapi

EXPOSE 8000

CMD ["km-pyapi", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://user:password@localhost/dbname
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or need help, please open an issue on GitHub.

## Author

**KM Fazle Rabbi** - Full Stack Developer & Software Engineer

- 🌐 **Website**: [kmfazle.dev](https://kmfazle.dev)
- 💼 **LinkedIn**: [km-fazle](https://linkedin.com/in/km-fazle)
- 🐙 **GitHub**: [@km-fazle](https://github.com/km-fazle)

## Changelog

### v0.1.0
- Initial release
- JWT authentication
- CRUD operations for items
- Comprehensive test suite
- OpenAPI documentation
- PyPI package available as `km-pyapi` 