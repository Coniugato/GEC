#!/bin/bash
cd {{cookiecutter.project_slug}}

echo "Initializing Git repository..."
git init


echo "Initializing DVC..."

echo "MLFLOW_TRACKING_URI={{ cookiecutter.mlflow_tracking_uri }}" > .env

echo "Setting up uv environment..."

uv venv

source .venv/bin/activate

if [ "{{ cookiecutter.additional_dependency_file }}" != "" ]; then
    cat {{ cookiecutter.additional_dependency_file }} >> pyproject.toml
else
    # if exists, add from the path in the env variable ADDITIONAL_DEP_FILE
    if [ -n "$ADDITIONAL_DEP_FILE" ] && [ -f "$ADDITIONAL_DEP_FILE" ]; then
        cat "$ADDITIONAL_DEP_FILE" >> pyproject.toml
    else
        echo "No additional dependency file provided."
    fi
fi

uv sync

dvc init

dvc add data

python - <<EOF
import os
cookiecutter_input_key = "{{ cookiecutter.wandb_api_key }}"

system_env_key = os.environ.get("WANDB_API_KEY", "")
final_api_key = ""

if cookiecutter_input_key.strip():
    final_api_key = cookiecutter_input_key
elif system_env_key.strip():
    print(f"Info: 'wandb_api_key' was not provided via cookiecutter. Using system environment variable WANDB_API_KEY.")
    final_api_key = system_env_key

env_file_path = ".env"

env_content = f"WANDB_API_KEY={final_api_key}\n"

with open(env_file_path, "a") as f:
    f.write(env_content)

if final_api_key:
    print(".env file has been updated with WANDB_API_KEY.")
else:
    print("Warning: No WANDB_API_KEY found in input or environment variables. .env created with empty key.")
EOF


#scriptの中のすべてのコマンドにchmod u+xを付与し、./.venv/binに移動
ls
chmod u+x scripts/*
mv scripts/* .venv/bin/
mv .venv/bin/batch_setting.sh scripts/batch_setting.sh
mv .venv/bin/batch_run.sh scripts/batch_run.sh

git add -A
git commit -m "Initial commit from cookiecutter template"

echo "Project {{ cookiecutter.project_name }} is ready!"

