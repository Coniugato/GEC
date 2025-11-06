# {{cookiecutter.project_name}}
    
     
     これは{{cookiecutter.project_name}}プロジェクトのリポジトリです。

     英語版： [README_en.md](README_en.md)

     ## セットアップ手順
        1. プロジェクトディレクトリに移動します:
        
            ```bash
            cd {{cookiecutter.project_slug}}
            ```

        2. 環境をアクティベートし、開発用依存関係をインストールします:
        
            ```bash
            source .venv/bin/activate
            uv sync
            ```     
        
        3(オプション). DVCのリモートストレージからデータとモデルをプルします:
        
            ```bash
            dvc pull
            ```    

        🎉おめでとうございます！プロジェクトのセットアップが完了しました。

    ## プロジェクト構成
    ### ファイル
    - `README_en.md`: 英語版のREADMEファイル。
    - `README_ja.md`: 日本語版のREADMEファイル。
    - `LICENSE`: プロジェクトのライセンス情報。
    - `pyproject.toml`: プロジェクトの設定と依存関係。
    - `uv.lock`: UV環境のロックファイル。
    - `dvc.yaml`: DVCパイプラインの定義。
    - `.gitignore`: Gitの無視ファイル。
    - `.dvcignore`: DVCの無視ファイル。 
    ### ディレクトリ
    - `conf/`: 実験の設定ファイル。
    - `sysconf/` : プロジェクトの設定ファイル。
    - `src/`: プロジェクトのソースコード。
    - `data/`: データセットのディレクトリ。
    - `results/`: 結果と出力を保存するディレクトリ。
    - `mlruns/`(オプション): MLflowのトラッキングデータ。
    - `framework/`: Generalized Experiment Control (GEC(c))のメインフレームワーク。 

    ## 使い方
    設定ファイルで定義された実験を実行するには、単に `dvc exp run` を実行します。
