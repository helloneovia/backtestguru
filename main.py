#!/usr/bin/env python3
"""
Script de dÃ©marrage Ã  la racine pour Nixpacks
"""
import sys
import os

# Ajouter le rÃ©pertoire backend au path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Changer vers le rÃ©pertoire backend
os.chdir(backend_path)

# Importer l'app depuis le backend
import importlib.util
spec = importlib.util.spec_from_file_location("backend_main", os.path.join(backend_path, "main.py"))
backend_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_main)

# DÃ©marrer l'application
import uvicorn
port = int(os.environ.get("PORT", 8000))
uvicorn.run(backend_main.app, host="0.0.0.0", port=port)