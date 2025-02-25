# QR Code Generator - Version 1

<img src="https://raw.githubusercontent.com/catab60/qr_code/refs/heads/main/example.bmp" width="300" height="300">

This is a QR Code generator built entirely from scratch, without using any external libraries. It was an incredibly challenging project that took me three days of focused effort. This journey has been a huge learning experience, pushing me to understand QR code structures deeply.

## About the Project

This is **Version 1**, and it currently supports **Version 1 QR codes (21x21 modules)**. The framework for supporting larger QR codes is already in place, but there are still many bugs to fix before they become fully functional.

### Features:
- **Full support for Version 1 QR codes**
- **Manually implemented Position Patterns, Timing Patterns, and Error Correction**
- **Custom masking algorithm**
- **No external libraries used – everything is built from scratch!**

## Future Improvements
- **Fixing bugs in larger QR code versions**
- **Adding GUI interface**
- **Adding more customization options**

## Usage Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/catab60/qr_code.git
   cd qr_code
   ```
2. Edit the script's starting variables to match your desired output.
   
3. Run the script:
   ```bash
   python qr_code.py
   ```
4. The program will generate a QR Code as BMP image file.

## Learning Experience
This project was a deep dive into QR code generation, teaching me about data encoding, error correction, and matrix structuring. Every part of the process, from binary encoding to final rendering, was a challenge that helped me grow as a programmer.

### Contributions
If you want to contribute or help fix bugs for larger QR code versions, feel free to submit a pull request!

---
Stay tuned for updates as I refine and expand this QR code generator!

