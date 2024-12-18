#!/usr/bin/env bash
rm -rf ./api/local/*
gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=6 --timeout 150 