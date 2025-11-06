# General Experiment Control (GEC)

Japanese Version: [readme_ja.md](readme_ja.md)

## Overview
General Experiment Control (GEC) is a framework designed for managing and controlling machine learning experiments. It combines tools such as `uv`, `dvc`, `hydra`, and `mlflow` to enhance experiment configuration, tracking, and reproducibility.

Also see [NOTICES](NOTICES) for the list of third-party libraries used in this project.

## How to Create a Project
After installing `cookiecutter` in some way, run the following command:
```
cookiecutter GEC
```
This one-liner generates a project with initialized `git`, `uv`, `dvc`, and more. After that, you can navigate to the generated directory and customize the project by editing the `src` directory, `conf` directory, `dvc.yaml`, and so on.