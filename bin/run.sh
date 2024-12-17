#!/usr/bin/env bash
rm -rf 
gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4