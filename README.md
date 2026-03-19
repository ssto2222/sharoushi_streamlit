# 社労士 学習アプリ — Streamlit

## セットアップ

```bash
# 1. 依存パッケージをインストール
pip install -r requirements.txt

# 2. アプリを起動
streamlit run app.py
```

ブラウザで http://localhost:8501 が自動的に開きます。

---

## 機能

| 機能 | 説明 |
|------|------|
| 📊 ダッシュボード | 9科目の進捗・正答率を一覧表示 |
| ▶ 科目別出題 | シャッフルして出題、解答後に解説表示 |
| ⚠️ 間違えた問題 | 誤答をまとめて復習、科目別フィルタ |
| 💾 途中再開 | 中断してもセッション復元で続きから |
| ✨ AI問題生成 | Anthropic APIキーで各科目10問ずつ自動生成 |
| 📋 JSONインポート | 自作問題の追加 |

---

## データ保存場所

```
data/
├── questions.json   # 問題データ（AIで追加可能）
├── progress.json    # 解答進捗（正解・誤答数）
└── session.json     # 中断セッション
```

---

## Supabase 連携（オプション）

複数デバイスでデータを同期したい場合は、以下を `.env` に追加してください：

```env
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_KEY=your-anon-key
```

`app.py` の `load_progress` / `save_progress` 関数を Supabase クライアントに差し替えるだけで対応できます。

---

## 問題のJSON形式

```json
[
  {
    "id": "roki_custom_001",
    "subject": "roki",
    "question": "問題文",
    "options": ["A", "B", "C", "D", "E"],
    "answer": 0,
    "explanation": "解説文"
  }
]
```

**subject の値：** roki / roan / rosai / koyo / choshu / kenpo / kokunen / konen / shaichi
