import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS(Cross-Origin Resource Sharing)を許可する
CORS(app)

# Ollama APIのエンドポイント
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        source_text = data.get('text')
        source_lang = data.get('source_lang', 'English') # デフォルトは英語
        target_lang = data.get('target_lang', 'Japanese') # デフォルトは日本語

        if not source_text:
            return jsonify({"error": "テキストがありません"}), 400

        # --- ここが重要：Ollamaへの翻訳指示プロンプト ---
        # Google翻訳APIと違い、LLMには「何をしてほしいか」を明確に指示します。
        prompt = (
            f"You are a professional and literal translator. "
            f"Translate the following {source_lang} text to {target_lang}. "
            f"RULES: "
            f"1. Output ONLY the translated text. "
            f"2. Do NOT add any introductory phrases, explanations, or apologies. "
            f"3. Do NOT omit any sentences, phrases, or information from the original text. "
            f"4. Preserve the original formatting (like LaTeX delimiters $, $$, etc.) exactly.\n\n"
            f"{source_lang}:\n\"{source_text}\"\n\n"
            f"{target_lang}:"
        )
        
        # -----------------------------------------------
        # -----------------------------------------------

        # Ollama APIに送信するデータ
        payload = {
            "model": "gemma3:4b",  # ここで使用するモデルを指定
            "prompt": prompt,
            "stream": False  # ストリーミングをオフにして、一度に全結果を受け取る
        }

        # Ollama APIを呼び出す
        response = requests.post(OLLAMA_API_URL, data=json.dumps(payload))
        response.raise_for_status()  # エラーがあれば例外を発生

        # 応答から翻訳結果（'response'キー）を抽出
        ollama_response = response.json()
        translated_text = ollama_response.get('response', '翻訳に失敗しました。')

        # 翻訳結果をクリーンアップ（前後の空白や不要な引用符を削除）
        cleaned_text = translated_text.strip().strip('"')

        return jsonify({"translation": cleaned_text})

    except requests.exceptions.RequestException as e:
        print(f"Ollama API エラー: {e}")
        return jsonify({"error": f"Ollama APIへの接続に失敗しました: {e}"}), 500
    except Exception as e:
        print(f"サーバーエラー: {e}")
        return jsonify({"error": f"内部サーバーエラー: {e}"}), 500

if __name__ == '__main__':
    # Flaskサーバーを起動
    app.run(debug=True, port=5000)
