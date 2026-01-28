// Tab Navigation
function showTab(tabName, event) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Show/Hide Loading Spinner
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// Show Error Message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

// Key Generation
document.getElementById('key-gen-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const keySize = document.getElementById('key-size').value;

    try {
        const response = await fetch('/api/generate-keys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ key_size: keySize })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('public-key').value = data.public_key;
            document.getElementById('private-key').value = data.private_key;
            document.getElementById('keys-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to generate keys: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Hash Text
document.getElementById('hash-text-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const text = document.getElementById('text-input').value;

    try {
        const response = await fetch('/api/hash-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('text-hash').textContent = data.hash;
            document.getElementById('hash-text-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to hash text: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Hash File
document.getElementById('hash-file-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        showError('Please select a file');
        hideLoading();
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/hash-file', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('file-name').textContent = data.filename;
            document.getElementById('file-size').textContent = data.file_size.toLocaleString();
            document.getElementById('file-hash').textContent = data.hash;
            document.getElementById('hash-file-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to hash file: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Create Certificate
document.getElementById('cert-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const formData = {
        common_name: document.getElementById('cert-common-name').value,
        country: document.getElementById('cert-country').value,
        state: document.getElementById('cert-state').value,
        locality: document.getElementById('cert-locality').value,
        organization: document.getElementById('cert-organization').value,
        validity_days: document.getElementById('cert-validity').value,
        key_size: document.getElementById('cert-key-size').value
    };

    try {
        const response = await fetch('/api/create-certificate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('certificate').value = data.certificate;
            document.getElementById('cert-private-key').value = data.private_key;
            document.getElementById('cert-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to create certificate: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Sign Message
document.getElementById('sign-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const message = document.getElementById('sign-message').value;
    const privateKey = document.getElementById('sign-private-key').value;

    try {
        const response = await fetch('/api/sign-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, private_key: privateKey })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('signature').textContent = data.signature;
            document.getElementById('sign-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to sign message: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Verify Signature
document.getElementById('verify-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();

    const message = document.getElementById('verify-message').value;
    const signature = document.getElementById('verify-signature').value;
    const publicKey = document.getElementById('verify-public-key').value;

    try {
        const response = await fetch('/api/verify-signature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, signature: signature, public_key: publicKey })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
        } else {
            const statusDiv = document.getElementById('verify-status');
            if (data.valid) {
                statusDiv.innerHTML = '<div class="alert alert-success">✓ <strong>Signature Valid:</strong> The signature is authentic and matches the message.</div>';
            } else {
                statusDiv.innerHTML = '<div class="alert alert-error">✗ <strong>Signature Invalid:</strong> The signature does not match the message or public key.</div>';
            }
            document.getElementById('verify-result').classList.remove('hidden');
        }
    } catch (error) {
        showError('Failed to verify signature: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Download Key/Certificate Function
function downloadKey(elementId, filename) {
    const content = document.getElementById(elementId).value;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Download Signature Function
function downloadSignature() {
    const signature = document.getElementById('signature').textContent;
    const blob = new Blob([signature], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'signature.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Copy to Clipboard Function
function copyToClipboard(elementId, event) {
    const element = document.getElementById(elementId);
    const text = element.textContent || element.value;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show temporary success message
        const originalText = event.target.textContent;
        event.target.textContent = '✓ Copied!';
        event.target.style.background = '#28a745';
        
        setTimeout(() => {
            event.target.textContent = originalText;
            event.target.style.background = '';
        }, 2000);
    }).catch(err => {
        showError('Failed to copy to clipboard: ' + err.message);
    });
}
