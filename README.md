Hybrid Cryptography & Steganography System

A secure data protection system that combines **Cryptography** and **Steganography** to provide an additional layer of security for sensitive information. The application supports secure text and image hiding using password-based encryption while also offering steganalysis capabilities to detect hidden content within images.


📖 Overview

Traditional encryption protects the content of a message but does not hide its existence. Steganography conceals the presence of data inside digital media but, by itself, may be vulnerable to unauthorized extraction or analysis.

This project integrates both techniques into a single system, ensuring that confidential information is **encrypted before being embedded**, providing enhanced confidentiality, integrity, and security.


✨ Features

- 🔒 Password-based text encryption
- 🖼️ Hide encrypted text inside images
- 🖼️ Hide one image inside another image
- 🔑 Password-protected image embedding
- 🔍 Steganography detection module
- 📤 Secure data extraction with authentication
- 🎯 Simple graphical user interface
- 💻 Offline desktop application


## 🏗️ System Workflow
'
                 User Input
                     │
        ┌────────────┴────────────┐
        │                         │
     Secret Text             Secret Image
        │                         │
 Password-Based          Password-Based
   Encryption          Image Encryption
        │                         │
        └────────────┬────────────┘
                     │
               LSB Embedding
                     │
               Stego Image
                     │
          Secure Transmission
                     │
        ┌────────────┴────────────┐
        │                         │
 Text Extraction          Image Extraction
        │                         │
 Password Verification    Password Verification
        │                         │
      Original Secret Data Retrieved


🛠️ Technologies Used

- Python 3.x
- Tkinter
- Pillow (PIL)
- Cryptography Library (Fernet)
- PBKDF2 Password-Based Key Derivation
- LSB (Least Significant Bit) Steganography



🔐 Text Encryption

- Password-based encryption using PBKDF2
- Secure symmetric encryption using Fernet
- Converts encrypted data into binary for embedding


🖼️ Text-in-Image Steganography

- Embeds encrypted text into an image
- Uses Least Significant Bit (LSB) embedding
- Maintains visual quality of the cover image


🖼️ Image-in-Image Steganography

- Hides a secret image inside another image
- Uses password-protected nibble masking
- Preserves image appearance while embedding data


🔍 Steganography Detection

- Detects possible hidden content inside images
- Performs LSB statistical analysis
- Estimates the likelihood of steganographic manipulation

📁 Project Structure


Hybrid-Cryptography-Steganography/
│
├── sample_images/             # Sample cover and secret images for testing
│
├── static/
│   ├── css/                   # Stylesheets
│   ├── uploads/               # User uploaded images
│   └── results/  
├── templates/
│   ├── index.html             # Home page
│   ├── text.html              # Text-in-Image Steganography
│   ├── image.html             # Image-in-Image Steganography
│   └── detect.html
├── requirements.txt
├── README.md
└── app.py


---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/syedroshanriyan/hybrid-stegnography-and-cryptography.git
```

### Navigate to the Project

```bash
cd hybrid-stegnography-and-cryptography
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```


 📸 user interaction

- Home Interface
- Text Encryption
- Text Steganography
- Image Steganography
- Steganography Detection


🎯 Applications

- Secure Communication
- Military & Defense
- Healthcare Data Protection
- Government Confidential Documents
- Digital Forensics
- Secure Image Sharing
- Corporate Information Security


🔒 Security Highlights

- Password-based authentication
- Encryption before embedding
- Multi-layer data protection
- Hidden communication channel
- Steganography detection support


🔮 Future Enhancements

- AES-256 encryption support
- Audio and video steganography
- AI-based steganalysis
- Cloud storage integration
- Drag-and-drop interface
- Cross-platform desktop application

 🤝 Contributing

Contributions are welcome.

If you'd like to improve this project, feel free to fork the repository, create a new branch, and submit a pull request.


📜 License

This project is intended for educational and research purposes.



👨‍💻 Author

**Syed Roshan Riyan**
Computer Science Engineering Student



⭐ If you found this project useful, consider giving it a star!
