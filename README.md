# 🔐 OpenSSL Cryptographic Operations Web Application

A comprehensive Python-based web application demonstrating OpenSSL cryptographic operations including RSA key generation, SHA-512 hashing, X.509 certificate creation, and digital signatures.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 1. RSA Key Pair Generation
- Generate RSA public/private key pairs (2048, 3072, or 4096-bit)
- Export keys in PEM format
- Download generated keys
- Security warnings and best practices

### 2. SHA-512 Hashing
- Hash text input using SHA-512
- Hash file uploads using SHA-512 (up to 16MB)
- Display hash in hexadecimal format
- Copy hash to clipboard

### 3. X.509 Certificate Creation
- Generate self-signed certificates
- Customize certificate fields (CN, C, ST, L, O)
- Configure validity period (1-3650 days)
- Choose key size (2048, 3072, 4096-bit)
- Export certificates and private keys in PEM format

### 4. Digital Signatures
- Sign messages using RSA private keys with SHA-512
- Verify signatures using RSA public keys
- Display signatures in base64 format
- RSA-PSS signature scheme for enhanced security

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pushkarrai-code/openssl.git
   cd openssl
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Start using the cryptographic operations!**

## 📚 Project Structure

```
openssl/
├── app.py                      # Main Flask application with API endpoints
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── crypto_notebook.ipynb       # Google Colab notebook for learning
├── templates/
│   └── index.html             # Web interface HTML
├── static/
│   ├── css/
│   │   └── style.css          # Styling and responsive design
│   └── js/
│       └── script.js          # Frontend JavaScript logic
└── .gitignore                 # Git ignore file
```

## 🔌 API Endpoints

### Generate RSA Key Pair
```http
POST /api/generate-keys
Content-Type: application/json

{
  "key_size": 2048  // 2048, 3072, or 4096
}
```

**Response:**
```json
{
  "success": true,
  "private_key": "-----BEGIN PRIVATE KEY-----...",
  "public_key": "-----BEGIN PUBLIC KEY-----...",
  "key_size": 2048
}
```

### Hash Text
```http
POST /api/hash-text
Content-Type: application/json

{
  "text": "Hello, World!"
}
```

**Response:**
```json
{
  "success": true,
  "hash": "374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6c...",
  "algorithm": "SHA-512",
  "input_length": 13
}
```

### Hash File
```http
POST /api/hash-file
Content-Type: multipart/form-data

file: [binary file data]
```

**Response:**
```json
{
  "success": true,
  "hash": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce...",
  "algorithm": "SHA-512",
  "filename": "document.pdf",
  "file_size": 1024
}
```

### Create Certificate
```http
POST /api/create-certificate
Content-Type: application/json

{
  "common_name": "localhost",
  "country": "US",
  "state": "California",
  "locality": "San Francisco",
  "organization": "My Organization",
  "validity_days": 365,
  "key_size": 2048
}
```

**Response:**
```json
{
  "success": true,
  "certificate": "-----BEGIN CERTIFICATE-----...",
  "private_key": "-----BEGIN PRIVATE KEY-----...",
  "common_name": "localhost",
  "validity_days": 365,
  "key_size": 2048
}
```

### Sign Message
```http
POST /api/sign-message
Content-Type: application/json

{
  "message": "Important message",
  "private_key": "-----BEGIN PRIVATE KEY-----..."
}
```

**Response:**
```json
{
  "success": true,
  "signature": "Base64EncodedSignature...",
  "algorithm": "RSA-PSS with SHA-512",
  "message_length": 17
}
```

### Verify Signature
```http
POST /api/verify-signature
Content-Type: application/json

{
  "message": "Important message",
  "signature": "Base64EncodedSignature...",
  "public_key": "-----BEGIN PUBLIC KEY-----..."
}
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "algorithm": "RSA-PSS with SHA-512"
}
```

## 📓 Google Colab Notebook

The project includes an interactive Jupyter notebook (`crypto_notebook.ipynb`) for learning cryptographic concepts:

### Using the Notebook

1. **Upload to Google Colab:**
   - Go to [Google Colab](https://colab.research.google.com/)
   - Click "File" → "Upload notebook"
   - Upload `crypto_notebook.ipynb`

2. **Or open directly:**
   ```
   https://colab.research.google.com/github/pushkarrai-code/openssl/blob/main/crypto_notebook.ipynb
   ```

3. **Run the cells to learn:**
   - RSA key generation with explanations
   - SHA-512 hashing examples
   - Certificate creation walkthroughs
   - Digital signature demonstrations
   - Interactive experiments

## 🔒 Security Considerations

### Best Practices Implemented

✅ **No server-side key storage** - Keys are generated and returned to the client immediately

✅ **Secure random number generation** - Uses cryptographically secure RNG

✅ **Input validation** - All user inputs are validated

✅ **Security warnings** - Users are warned about private key security

✅ **Modern algorithms** - Uses SHA-512 and RSA-PSS

### Important Security Notes

⚠️ **Development Use Only** - This application is designed for educational purposes

⚠️ **HTTPS in Production** - Always use HTTPS in production environments

⚠️ **Key Management** - Never share private keys or store them insecurely

⚠️ **Self-Signed Certificates** - Only use self-signed certificates for development/testing

⚠️ **Production Systems** - Consult security experts for production cryptographic systems

## 🌐 Deployment Options

### Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add gunicorn to requirements.txt:
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Render

1. Create a `render.yaml`:
   ```yaml
   services:
     - type: web
       name: openssl-crypto
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app
   ```

2. Connect your GitHub repository to Render

### PythonAnywhere

1. Upload files to PythonAnywhere
2. Create a new web app with Flask
3. Configure WSGI file to point to `app.py`
4. Install requirements in the PythonAnywhere console

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t openssl-crypto .
docker run -p 5000:5000 openssl-crypto
```

## 🛠️ Technology Stack

- **Backend:**
  - Python 3.8+
  - Flask 3.0.0 (Web framework)
  - cryptography 41.0.7 (OpenSSL wrapper)

- **Frontend:**
  - HTML5
  - CSS3 (with responsive design)
  - JavaScript (ES6+)
  - No external frameworks (vanilla JS)

- **Cryptographic Algorithms:**
  - RSA (2048/3072/4096-bit)
  - SHA-512
  - RSA-PSS (Probabilistic Signature Scheme)
  - X.509 certificates

## 📸 Screenshots

### Key Generation Interface
The application provides a clean interface for generating RSA key pairs with customizable key sizes.

### Hashing Operations
Users can hash text or files using SHA-512 with instant results displayed in hexadecimal format.

### Certificate Creation
Generate self-signed X.509 certificates with customizable fields and validity periods.

### Digital Signatures
Sign and verify messages using RSA keys with clear visual feedback on signature validity.

## 🧪 Testing

### Manual Testing

1. **Test Key Generation:**
   - Generate keys with different sizes (2048, 3072, 4096)
   - Download and verify PEM format

2. **Test Hashing:**
   - Hash various text inputs
   - Upload and hash files
   - Verify deterministic behavior

3. **Test Certificates:**
   - Create certificates with different parameters
   - Verify certificate validity periods
   - Check PEM format

4. **Test Signatures:**
   - Sign messages with generated keys
   - Verify valid signatures
   - Test with invalid/tampered messages

### Example Test Flow

```python
# Generate keys
keys = generate_keys(2048)

# Sign a message
message = "Test message"
signature = sign_message(message, keys['private_key'])

# Verify signature
is_valid = verify_signature(message, signature, keys['public_key'])
assert is_valid == True

# Test with tampered message
tampered = "Test message!"
is_valid = verify_signature(tampered, signature, keys['public_key'])
assert is_valid == False
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Pushkar Rai**
- GitHub: [@pushkarrai-code](https://github.com/pushkarrai-code)

## 🙏 Acknowledgments

- [cryptography](https://cryptography.io/) - Python cryptographic library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [OpenSSL](https://www.openssl.org/) - Cryptographic toolkit

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/pushkarrai-code/openssl/issues)
- Check the [documentation](https://github.com/pushkarrai-code/openssl/wiki)

## 🔄 Version History

- **v1.0.0** (2024) - Initial release
  - RSA key generation
  - SHA-512 hashing
  - X.509 certificate creation
  - Digital signatures
  - Google Colab notebook
  - Responsive web interface

---

**⚠️ Educational Purpose Disclaimer:** This application is designed for educational and development purposes. For production cryptographic systems, always consult with security experts and follow industry best practices.