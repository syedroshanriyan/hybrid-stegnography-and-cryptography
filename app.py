from flask import Flask, render_template, request
from PIL import Image
import os
import io
import base64
import uuid
import secrets
import hashlib

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# ================= CRYPTO HELPERS (TEXT STEGO) =================

def encrypt_with_password(plaintext: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    token = f.encrypt(plaintext)
    return salt + token

def decrypt_with_password(data: bytes, password: str) -> bytes:
    salt = data[:16]
    token = data[16:]
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    return f.decrypt(token)

# ================= BIT HELPERS =================

def bytes_to_bits(data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in data)

def bits_to_bytes(bits: str) -> bytes:
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# ================= TEXT STEGO =================

def embed_data_in_image(cover_path: str, data: bytes, output_path: str):
    image = Image.open(cover_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    length_bytes = len(data).to_bytes(4, 'big')
    full_data = length_bytes + data
    bitstring = bytes_to_bits(full_data)

    pixels = list(image.getdata())
    capacity = len(pixels) * 3
    if len(bitstring) > capacity:
        raise ValueError("Data too large for selected image.")

    new_pixels = []
    bit_i = 0
    for pixel in pixels:
        r, g, b = pixel
        if bit_i < len(bitstring):
            r = (r & ~1) | int(bitstring[bit_i])
            bit_i += 1
        if bit_i < len(bitstring):
            g = (g & ~1) | int(bitstring[bit_i])
            bit_i += 1
        if bit_i < len(bitstring):
            b = (b & ~1) | int(bitstring[bit_i])
            bit_i += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)

def extract_data_from_image(stego_path: str) -> bytes:
    image = Image.open(stego_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = list(image.getdata())
    bits = []
    for r, g, b in pixels:
        bits.append(str(r & 1))
        bits.append(str(g & 1))
        bits.append(str(b & 1))

    bits = ''.join(bits)
    length_bits = bits[:32]
    data_length = int(length_bits, 2)

    total_bits_needed = 32 + data_length * 8
    if total_bits_needed > len(bits):
        raise ValueError("Invalid or corrupted text stego image.")

    data_bits = bits[32:total_bits_needed]
    return bits_to_bytes(data_bits)

# ================= IMAGE-IN-IMAGE STEGO =================

def _nibble_keystream(password: str, index: int, channel: int) -> int:
    h = hashlib.blake2b(f"{password}:{index}:{channel}".encode(), digest_size=1).digest()[0]
    return h & 0x0F

def hide_image_lsb_password(cover, secret, password, output):
    cover = Image.open(cover).convert("RGB")
    secret = Image.open(secret).convert("RGB").resize(cover.size)

    cpix = list(cover.getdata())
    spix = list(secret.getdata())
    newpix = []

    for i, (c, s) in enumerate(zip(cpix, spix)):
        sr, sg, sb = (s[0] >> 4) & 0x0F, (s[1] >> 4) & 0x0F, (s[2] >> 4) & 0x0F
        kr, kg, kb = _nibble_keystream(password, i, 0), _nibble_keystream(password, i, 1), _nibble_keystream(password, i, 2)

        nr = (c[0] & 0xF0) | (sr ^ kr)
        ng = (c[1] & 0xF0) | (sg ^ kg)
        nb = (c[2] & 0xF0) | (sb ^ kb)
        newpix.append((nr, ng, nb))

    out = Image.new("RGB", cover.size)
    out.putdata(newpix)
    out.save(output)

def retrieve_image_lsb_password(stego, password, output):
    stego = Image.open(stego).convert("RGB")
    pix = list(stego.getdata())
    recovered = []

    for i, p in enumerate(pix):
        kr, kg, kb = _nibble_keystream(password, i, 0), _nibble_keystream(password, i, 1), _nibble_keystream(password, i, 2)
        rr = ((p[0] & 0x0F) ^ kr) << 4
        rg = ((p[1] & 0x0F) ^ kg) << 4
        rb = ((p[2] & 0x0F) ^ kb) << 4
        recovered.append((rr, rg, rb))

    img = Image.new("RGB", stego.size)
    img.putdata(recovered)
    img.save(output)

# ================= DETECTOR =================

def analyze_lsb(path):
    img = Image.open(path).convert("RGB")
    bits = [(r & 1, g & 1, b & 1) for r, g, b in img.getdata()]
    flat = [v for trip in bits for v in trip]
    ones = sum(flat)
    zeros = len(flat) - ones
    ratio = ones / len(flat)

    if 0.48 <= ratio <= 0.52:
        verdict = "Suspicious: LSB pattern appears randomized (possible steganography)."
    else:
        verdict = "Probably clean: No strong indication of steganography."

    return verdict, zeros, ones, ratio

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/text', methods=['GET', 'POST'])
def text_page():
    ctx = {"text_stego": None, "text_out": None, "error": None}
    if request.method == "POST":
        try:
            if request.form.get("action") == "hide":
                cover = request.files["cover"]
                msg = request.form["msg"]
                pw = request.form["pw"]
                cover_path = os.path.join(UPLOAD_FOLDER, f"t_cover_{uuid.uuid4().hex}.png")
                cover.save(cover_path)

                encrypted = encrypt_with_password(msg.encode(), pw)
                payload = b"T" + encrypted
                out = os.path.join(RESULT_FOLDER, f"t_stego_{uuid.uuid4().hex}.png")
                embed_data_in_image(cover_path, payload, out)
                ctx["text_stego"] = out

            elif request.form.get("action") == "extract":
                stego = request.files["stego"]
                pw = request.form["pw"]
                stego_path = os.path.join(UPLOAD_FOLDER, f"t_in_{uuid.uuid4().hex}.png")
                stego.save(stego_path)
                raw = extract_data_from_image(stego_path)
                if raw[0:1] != b"T":
                    raise ValueError("Not a valid encrypted text stego.")
                out = decrypt_with_password(raw[1:], pw)
                ctx["text_out"] = out.decode(errors="replace")

        except Exception as e:
            ctx["error"] = str(e)

    return render_template("text.html", **ctx)

@app.route('/image', methods=['GET', 'POST'])
def image_page():
    ctx = {"image_stego": None, "image_out": None, "error": None}
    if request.method == "POST":
        try:
            if request.form.get("action") == "hide":
                cover = request.files["cover"]
                secret = request.files["secret"]
                pw = request.form["pw"]
                cover_path = os.path.join(UPLOAD_FOLDER, f"i_cover_{uuid.uuid4().hex}.png")
                secret_path = os.path.join(UPLOAD_FOLDER, f"i_secret_{uuid.uuid4().hex}.png")
                cover.save(cover_path); secret.save(secret_path)

                out = os.path.join(RESULT_FOLDER, f"i_stego_{uuid.uuid4().hex}.png")
                hide_image_lsb_password(cover_path, secret_path, pw, out)
                ctx["image_stego"] = out

            elif request.form.get("action") == "extract":
                stego = request.files["stego"]
                pw = request.form["pw"]
                stego_path = os.path.join(UPLOAD_FOLDER, f"i_in_{uuid.uuid4().hex}.png")
                stego.save(stego_path)
                out = os.path.join(RESULT_FOLDER, f"i_rec_{uuid.uuid4().hex}.png")
                retrieve_image_lsb_password(stego_path, pw, out)
                ctx["image_out"] = out

        except Exception as e:
            ctx["error"] = str(e)

    return render_template("image.html", **ctx)

@app.route('/detect', methods=['GET', 'POST'])
def detect_page():
    ctx = {"prob": None, "status_code": None, "stats": None, "error": None}

    if request.method == "POST":
        try:
            img = request.files["img"]
            path = os.path.join(UPLOAD_FOLDER, f"d_{uuid.uuid4().hex}.png")
            img.save(path)

            verdict, zeros, ones, ratio = analyze_lsb(path)

            dev = abs(ratio - 0.5)

            # ---- New high accuracy probability logic ----
            if dev <= 0.003:  # VERY close to random -> strong stego
                prob = 90 + ((0.003 - dev) / 0.003) * 10  # 90-100%
            elif dev <= 0.01:  # moderately close -> possible stego
                prob = 40 + ((0.01 - dev) / 0.01) * 50  # 40-90%
            else:  # far from random -> clean image
                prob = max(0, (0.01 / dev) * 10)  # typically 0-20%

            prob = round(prob, 2)

            # ---- classification ----
            if prob >= 75:
                status_code = "suspicious"
            elif prob >= 40:
                status_code = "possible"
            else:
                status_code = "clean"

            ctx["prob"] = prob
            ctx["status_code"] = status_code
            ctx["stats"] = {"zeros": zeros, "ones": ones, "ratio": ratio}

        except Exception as e:
            ctx["error"] = str(e)

    return render_template("detect.html", **ctx)



if __name__ == '__main__':
    app.run(debug=True)
