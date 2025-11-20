# General Experiment Control (GEC)

英語版: [readme_en.md](readme_en.md)

## 概要

General Experiment Control (GEC) は、機械学習実験の管理と制御を目的としたフレームワークです。`uv`、`dvc`、`hydra`、`mlflow`などを組み合わせて、実験の設定、追跡、再現性を向上させます。

また、本プロジェクトで使用されているサードパーティライブラリの一覧については、[NOTICES](NOTICES) を参照してください。

## プロジェクトの作り方
`cookiecutter`をなんらかの形でインストールした上で、以下のコマンドを実行してください。
```
cookiecutter https://github.com/Coniugato/GEC.git
```
このワンライナーで、`git`、`uv`、`dvc`などの初期化が完了されたプロジェクトが生成されます。その後、生成されたディレクトリに移動して、`src`ディレクトリや`conf`ディレクトリ、`dvc.yaml`などを編集してプロジェクトをカスタマイズすることができます。
