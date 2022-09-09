#!/bin/sh

sed -i s/httpbin.icu/$HOST/g /app/settings.py

python main.py
