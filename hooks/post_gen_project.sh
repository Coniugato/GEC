#!/bin/bash
cd {{cookiecutter.project_slug}}

echo "Initializing Git repository..."
git init


echo "Initializing DVC..."

echo "MLFLOW_TRACKING_URI={{ cookiecutter.mlflow_tracking_uri }}" > .env

echo "Setting up uv environment..."

uv venv

source .venv/bin/activate

uv sync

dvc init

dvc add data

git add .
git commit -m "Initial commit from cookiecutter template"

echo "Project {{ cookiecutter.project_name }} is ready!"

