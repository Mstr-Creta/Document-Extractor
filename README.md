# 📄 Universal Document Extractor (Offline)

> A privacy-focused, offline-capable document extraction tool built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Overview
This project is a **Zero-Cost, No-API** tool that extracts structured text data from scanned documents and ID cards. Unlike other tools that require expensive cloud APIs (like Google Vision or AWS Textract), this tool runs entirely on your local machine using **EasyOCR** and **Regex** pattern matching.

It automatically identifies document types and formats the output into a clean, readable table.

## ✨ Features
* **100% Offline:** No internet connection or API keys required.
* **Auto-Detection:** Automatically identifies PAN Cards, Aadhaar Cards, Passports, and US Tax Forms.
* **Structured Output:** Converts messy OCR text into clean columns (Name, ID Number, DOB).
* **Privacy First:** Your data never leaves your computer.
* **Exportable:** View history of extracted documents in a dynamic table.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **OCR Engine:** [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Deep Learning based)
* **Data Handling:** Pandas, NumPy
* **Image Processing:** PIL (Python Imaging Library), OpenCV

