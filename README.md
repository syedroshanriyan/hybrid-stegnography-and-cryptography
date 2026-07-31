# 🔐 ***Hybrid Cryptography & Steganography System***

A secure web-based application that combines **Cryptography** and **Steganography** to provide multi-layered protection for sensitive information. The system supports password-based encryption for text and images, secure LSB-based data embedding, and steganalysis to detect hidden content within digital images.

---

## 📖 Overview

Traditional encryption protects the contents of a message but does not conceal its existence. Steganography hides confidential information inside digital media, making communication less noticeable. However, steganography alone may still be vulnerable to extraction and analysis.

This project integrates **Cryptography** and **Steganography** into a single secure framework, ensuring that sensitive information is first encrypted and then invisibly embedded inside images for enhanced confidentiality and protection.

---

# ✨ Features

- 🔒 Password-based text encryption
- 🖼️ Secure Text-in-Image Steganography
- 🖼️ Secure Image-in-Image Steganography
- 🔑 Password-protected image embedding
- 🔍 LSB-based Steganography Detection
- 📤 Secure data extraction with authentication
- 🌐 Web-based user interface using Flask
- 💻 Offline execution with local processing

---

# 🏗️ System Workflow

```text
                         User Input
                             │
             ┌───────────────┴───────────────┐
             │                               │
        Secret Text                    Secret Image
             │                               │
     Password-Based                 Password-Based
        Encryption                 Image Encryption
             │                               │
             └───────────────┬───────────────┘
                             │
                      LSB Embedding
                             │
                        Stego Image
                             │
                  Secure Image Transmission
                             │
             ┌───────────────┴───────────────┐
             │                               │
      Text Extraction                 Image Extraction
             │                               │
     Password Verification      Password Verification
             │                               │
             └───────────────┬───────────────┘
                             │
                  Original Secret Data
```

---

# 🛠️ Technologies Used

- Python 3.x
- Flask
- HTML5
- CSS3
- Pillow (PIL)
- Cryptography (Fernet)
- PBKDF2 Password-Based Key Derivation
- Least Significant Bit (LSB) Steganography

---

# 📌 Modules

## 🔐 Text Encryption

- Password-based encryption using PBKDF2
- Secure symmetric encryption with Fernet
- Converts encrypted data into binary before embedding

---

## 🖼️ Text-in-Image Steganography

- Embeds encrypted text inside images
- Uses LSB (Least Significant Bit) embedding
- Preserves visual quality of the cover image

---

## 🖼️ Image-in-Image Steganography

- Hides one image inside another image
- Uses password-protected nibble masking
- Maintains image quality while embedding secret data

---

## 🔍 Steganography Detection

- Detects hidden information inside images
- Performs LSB statistical analysis
- Estimates the probability of steganographic manipulation

---

# 📁 Project Structure

```
Hybrid-Cryptography-Steganography/
│
├── sample_images/   #Sample cover and secret images
│  
├── static/
│   ├── css  #Stylesheet      
│   │
│   ├── uploads/  #Uploaded user images
│   │  
│   └── results/  #Generated stego images and extracted outputs
│       
├── templates/
│   ├── index.html
│   ├── text.html
│   ├── image.html
│   └── detect.html
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/syedroshanriyan/hybrid-stegnography-and-cryptography.git
```

---

## 2️⃣ Navigate to the Project Directory

```bash
cd hybrid-stegnography-and-cryptography
```

---

## 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the Application

```bash
python app.py
```

---

## 5️⃣ Open in Browser

Visit:

```
http://127.0.0.1:5000/
```

---

# 📸 User Interface

The application provides an intuitive web interface consisting of:

- 🏠 Home Page
- 🔐 Text Encryption
- 🖼️ Text-in-Image Module
- 🖼️ Image-in-Image Module
- 🔍 Steganography Detection


---

# 🎯 Applications

- Secure Communication
- Military & Defense
- Healthcare Data Protection
- Government Confidential Documents
- Digital Forensics
- Secure Image Sharing
- Corporate Information Security

---

# 🔒 Security Highlights

- Password-Based Authentication
- Multi-layer Security Architecture
- Encryption Before Embedding
- Hidden Communication Channel
- Secure Data Recovery
- LSB Steganography Detection

---

# 🔮 Future Enhancements

- AES-256 Encryption
- Audio Steganography
- Video Steganography
- AI-Based Steganalysis
- Cloud Storage Integration
- Drag-and-Drop Interface
- Cross-Platform Deployment

---

# 🤝 Contributing

Contributions are welcome.

If you have ideas for improving this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 📜 License

This project is developed for **educational**, **academic**, and **research** purposes.

---

# 👨‍💻 Author

### **Syed Roshan Riyan**

**Bachelor of Engineering (Computer Science)**

GitHub: https://github.com/syedroshanriyan
Linkedin: https://www.linkedin.com/in/syed-roshan-riyan-b871273b0/

---

## ⭐ Support

If you found this project useful, please consider **starring** the repository.

It helps others discover the project and motivates future improvements.
