# PrivaTranslate

ローカル翻訳システムです。プライバシーやセキュリティが心配な文章を翻訳するときに使うと便利かもしれません。また、Google翻訳やDeepLなどが使えなくなった場合にも役立ちます。

Macbook Pro M4上でGemma3:4bモデルを使用してテスト済みです。Macbook上でありながら、実用的なスピードで翻訳が可能です。

## 特徴

- ローカル環境で動作するため、プライバシーが保護されます
- インターネット接続不要（モデルダウンロード後）
- Google翻訳などの外部APIに依存しません

## 注意

本プログラムコードは、ほぼVibe codingで作成しています。

## 必要な環境

- Python 3.7以上
- Ollama（ローカルLLMサーバー）

## インストール方法

### 1. 必要なPythonライブラリのインストール

```bash
pip install -r requirements.txt
```

または、個別にインストールする場合：

```bash
pip install Flask flask-cors requests
```

### 2. Ollamaのインストールと設定

1. [Ollama](https://ollama.ai/)をインストール
2. 翻訳用のモデルをダウンロード：
   ```bash
   ollama pull gemma3:4b
   ```

## 使い方

1. Ollamaサーバーが起動していることを確認
2. Flaskアプリケーションを起動：
   ```bash
   python app.py
   ```
3. ブラウザで `index.html` を開く
4. テキストを入力して翻訳


