# {{cookiecutter.project_name}}


     This is a machine learning project {{cookiecutter.project_name}} generated using Cookiecutter.

    Japanese Version: [README_ja.md](README_ja.md)

     ## Setup Instructions
     
     1. Navigate into the project directory:
     
        ```bash
        cd {{cookiecutter.project_slug}}
        ```
     
     2. Activate your environment and install development dependencies:
     
        ```bash
        source .venv/bin/activate
        uv sync
        ```
     
     3(Option). Pull data and models from DVC remote storage:
     
        ```bash
        dvc pull
        ```

      🎉Congratulations! Your project is now set up.

     ## Project Structure
     ### Files
     - `README_en.md`: This readme file.
     - `README_ja.md`: Japanese version of the readme file.
     - `LICENSE`: License information for the project.
     - `pyproject.toml`: Project configuration and dependencies.
     - `uv.lock`: UV environment lock file.
     - `dvc.yaml`: DVC pipeline definition.
     - `.gitignore`: Git ignore file.
     - `.dvcignore`: DVC ignore file.

     ### Directories
     - `conf/`: Configuration files for the experiments.
     - `sysconf/` : Project configuration files.
     - `src/`: Source code for the project.
     - `data/`: Directory for datasets.
     - `results/`: Directory for storing results and outputs.
     - `mlruns/`(Option): MLflow tracking data.
     - `framework/`: Main frameworks for Generalized Experiment Control (GEC(c)).
     
     ## Usage
     
     You can simply run `dvc exp run` to execute experiments defined in the configuration files.
     
    