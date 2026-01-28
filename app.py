"""
OpenSSL Cryptographic Operations Web Application
Flask backend implementing RSA, SHA-512, certificates, and digital signatures
"""

from flask import Flask, render_template, request, jsonify, send_file
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import base64
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    """
    Generate RSA key pair
    Returns public and private keys in PEM format
    """
    try:
        data = request.get_json()
        key_size = int(data.get('key_size', 2048))
        
        # Validate key size
        if key_size not in [2048, 3072, 4096]:
            return jsonify({'error': 'Invalid key size. Must be 2048, 3072, or 4096'}), 400
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize private key to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        # Serialize public key to PEM format
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        return jsonify({
            'success': True,
            'private_key': private_pem,
            'public_key': public_pem,
            'key_size': key_size
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid key size parameter'}), 400
    except Exception as e:
        app.logger.error(f'Key generation error: {str(e)}')
        return jsonify({'error': 'Failed to generate keys'}), 500


@app.route('/api/hash-text', methods=['POST'])
def hash_text():
    """
    Hash text input using SHA-512
    Returns hash in hexadecimal format
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text input is required'}), 400
        
        # Create SHA-512 hash
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        digest.update(text.encode('utf-8'))
        hash_bytes = digest.finalize()
        
        # Convert to hexadecimal
        hash_hex = hash_bytes.hex()
        
        return jsonify({
            'success': True,
            'hash': hash_hex,
            'algorithm': 'SHA-512',
            'input_length': len(text)
        })
        
    except Exception as e:
        app.logger.error(f'Hash text error: {str(e)}')
        return jsonify({'error': 'Failed to hash text'}), 500


@app.route('/api/hash-file', methods=['POST'])
def hash_file():
    """
    Hash file upload using SHA-512
    Returns hash in hexadecimal format
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        file_content = file.read()
        
        # Create SHA-512 hash
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        digest.update(file_content)
        hash_bytes = digest.finalize()
        
        # Convert to hexadecimal
        hash_hex = hash_bytes.hex()
        
        return jsonify({
            'success': True,
            'hash': hash_hex,
            'algorithm': 'SHA-512',
            'filename': file.filename,
            'file_size': len(file_content)
        })
        
    except Exception as e:
        app.logger.error(f'Hash file error: {str(e)}')
        return jsonify({'error': 'Failed to hash file'}), 500


@app.route('/api/create-certificate', methods=['POST'])
def create_certificate():
    """
    Create self-signed X.509 certificate
    Returns certificate in PEM format
    """
    try:
        data = request.get_json()
        
        # Get certificate fields
        common_name = data.get('common_name', 'localhost')
        country = data.get('country', 'US')
        state = data.get('state', 'State')
        locality = data.get('locality', 'City')
        organization = data.get('organization', 'Organization')
        validity_days = int(data.get('validity_days', 365))
        key_size = int(data.get('key_size', 2048))
        
        # Validate inputs
        if not common_name:
            return jsonify({'error': 'Common name is required'}), 400
        
        if validity_days < 1 or validity_days > 3650:
            return jsonify({'error': 'Validity days must be between 1 and 3650'}), 400
        
        if key_size not in [2048, 3072, 4096]:
            return jsonify({'error': 'Invalid key size. Must be 2048, 3072, or 4096'}), 400
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        # Create subject and issuer (same for self-signed)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        
        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA512(), default_backend())
        
        # Serialize certificate to PEM format
        cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
        
        # Serialize private key to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        return jsonify({
            'success': True,
            'certificate': cert_pem,
            'private_key': private_pem,
            'common_name': common_name,
            'validity_days': validity_days,
            'key_size': key_size
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid certificate parameters'}), 400
    except Exception as e:
        app.logger.error(f'Certificate creation error: {str(e)}')
        return jsonify({'error': 'Failed to create certificate'}), 500


@app.route('/api/sign-message', methods=['POST'])
def sign_message():
    """
    Sign a message using RSA private key with SHA-512
    Returns signature in base64 format
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        private_key_pem = data.get('private_key', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not private_key_pem:
            return jsonify({'error': 'Private key is required'}), 400
        
        # Load private key
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
        except Exception:
            return jsonify({'error': 'Invalid private key format'}), 400
        
        # Sign the message
        signature = private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        
        # Encode signature to base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        return jsonify({
            'success': True,
            'signature': signature_b64,
            'algorithm': 'RSA-PSS with SHA-512',
            'message_length': len(message)
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid input parameters'}), 400
    except Exception as e:
        app.logger.error(f'Sign message error: {str(e)}')
        return jsonify({'error': 'Failed to sign message'}), 500


@app.route('/api/verify-signature', methods=['POST'])
def verify_signature():
    """
    Verify a digital signature using RSA public key
    Returns verification result
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        signature_b64 = data.get('signature', '')
        public_key_pem = data.get('public_key', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not signature_b64:
            return jsonify({'error': 'Signature is required'}), 400
        
        if not public_key_pem:
            return jsonify({'error': 'Public key is required'}), 400
        
        # Load public key
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8'),
                backend=default_backend()
            )
        except Exception:
            return jsonify({'error': 'Invalid public key format'}), 400
        
        # Decode signature from base64
        try:
            signature = base64.b64decode(signature_b64)
        except Exception:
            return jsonify({'error': 'Invalid signature format'}), 400
        
        # Verify signature
        try:
            public_key.verify(
                signature,
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA512()
            )
            valid = True
        except Exception:
            valid = False
        
        return jsonify({
            'success': True,
            'valid': valid,
            'algorithm': 'RSA-PSS with SHA-512'
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid input parameters'}), 400
    except Exception as e:
        app.logger.error(f'Verify signature error: {str(e)}')
        return jsonify({'error': 'Failed to verify signature'}), 500


if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
