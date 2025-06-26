#!/usr/bin/env bash

# Установка Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# Установка зависимостей из requirements.txt
pip install -r requirements.txt
