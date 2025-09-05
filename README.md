# HEICtoJPG

iPhoneのHEIC画像をWindowsで一括してJPEGまたはPNGに変換するPythonスクリプト。

## 必要環境
- Windows 10/11
- Python 3.9+ 推奨
- パッケージ
  - pillow
  - pillow-heif
  - tqdm

インストール:
```bash
pip install pillow pillow-heif tqdm
```

## 使い方
基本:
```bash
python HEICtoJPG.py --src "C:\path\to\heic_folder" --dst "C:\path\to\out"
```

オプション:
- --src
  - 変換元フォルダのパス
  - フォルダ直下の .heic/.HEIC を対象
- --dst
  - 出力先フォルダのパス
  - 無い場合は自動作成
- --png
  - PNGで保存（ロスレス）。指定しない場合はJPEG
- --quality
  - JPEGの画質 1〜100。既定は 95
  - --png 指定時は無視
- --workers
  - 並列実行数。既定はCPUコア数

例:
```bash
# 高画質JPEG（品質100）
python HEICtoJPG.py --src "C:\HEIC" --dst "C:\OUT" --quality 100

# PNG（ロスレス）
python HEICtoJPG.py --src "C:\HEIC" --dst "C:\OUT" --png

# 並列数を4に制限
python HEICtoJPG.py --src "C:\HEIC" --dst "C:\OUT" --quality 92 --workers 4
```

## ヒント
- 品質重視のJPEG出力は quality=92〜95 がバランス良好
- 画質最優先にする場合はコード内の save で subsampling=0, progressive=True を指定可能
- サブフォルダも含めたい場合は、スクリプト中の `glob("*.heic")` を `rglob("*.heic")` に変更
- 元のHEICは保管し、共有用だけJPEG/PNG化するのがおすすめ

## トラブルシューティング
- pipが通らない
  - Python再インストール時に「Add Python to PATH」を有効化
- 日本語パスで失敗する
  - 一時的に英数字パスを使用
- ダブルクリックで使いたい
  - バッチファイルを作成してコマンドを1行で呼び出すのがおすすめ

## ライセンス
- 個人利用の想定。再配布・改変は自己責任で実施してください。
このプロジェクトは、ChatGPT-5の支援を受けて作成されました。