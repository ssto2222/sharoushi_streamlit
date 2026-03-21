import streamlit as st
import json
import random
from datetime import datetime

# ── ページ設定 ──────────────────────────────────────────

st.set_page_config(
page_title="社労士 学習アプリ",
page_icon="📚",
layout="wide",
initial_sidebar_state="expanded",
)

# ── カスタムCSS ──────────────────────────────────────────

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }

.stApp { background-color: #0e0e16; }
section[data-testid="stSidebar"] { background-color: #12121c !important; border-right: 1px solid rgba(255,255,255,0.07); }
section[data-testid="stSidebar"] * { color: #c8c8d8 !important; }

[data-testid="metric-container"] {
    background: #1a1a28;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="metric-container"] label { color: #7070a0 !important; font-size: 11px !important; letter-spacing: 1px; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e0e0f0 !important; font-family: 'DM Mono', monospace !important; }

.stButton > button {
    background: #7c6af5 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans JP', sans-serif !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: #9580ff !important; transform: translateY(-1px) !important; }

.btn-secondary > button {
    background: #1e1e30 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #c0c0d8 !important;
}
.btn-secondary > button:hover { border-color: #7c6af5 !important; color: white !important; }

.question-card {
    background: #16162a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
}
.question-number {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #6060a0;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.question-text { font-size: 17px; line-height: 1.9; color: #e8e8f8; font-weight: 400; }

.correct-box {
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.4);
    border-radius: 10px;
    padding: 16px 20px;
    color: #2ecc71;
    font-weight: 500;
    margin: 12px 0;
}
.wrong-box {
    background: rgba(231,76,60,0.1);
    border: 1px solid rgba(231,76,60,0.4);
    border-radius: 10px;
    padding: 16px 20px;
    color: #e74c3c;
    font-weight: 500;
    margin: 12px 0;
}
.explanation-box {
    background: #1a1a2e;
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #7c6af5;
    border-radius: 0 10px 10px 0;
    padding: 18px 20px;
    color: #a0a0c8;
    font-size: 14px;
    line-height: 1.9;
    margin-top: 14px;
}
.explanation-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #7c6af5;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.progress-outer {
    background: #1e1e30;
    border-radius: 4px;
    height: 6px;
    margin: 6px 0 10px;
    overflow: hidden;
}
.progress-inner {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #7c6af5, #a594ff);
    transition: width 0.4s ease;
}
.progress-inner-green { background: linear-gradient(90deg, #27ae60, #2ecc71); }

.subject-card {
    background: #16162a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s;
}
.subject-card:hover { border-color: #7c6af5; }
.subject-tag {
    display: inline-block;
    background: rgba(124,106,245,0.15);
    color: #a594ff;
    font-size: 10px;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-bottom: 10px;
}
.wrong-tag {
    display: inline-block;
    background: rgba(231,76,60,0.1);
    color: #e74c3c;
    font-size: 10px;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 8px;
}

.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
    background: #1a1a2e !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    width: 100% !important;
    color: #c8c8e8 !important;
    transition: all 0.15s !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
.stRadio > div > label:hover { border-color: #7c6af5 !important; background: rgba(124,106,245,0.08) !important; }

h1 { color: #e8e8f8 !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2, h3 { color: #d0d0e8 !important; font-weight: 500 !important; }
p, li { color: #9090b8 !important; }
hr { border-color: rgba(255,255,255,0.07) !important; }

.log-box {
    background: #0e0e16;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 14px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #7070a0;
    max-height: 300px;
    overflow-y: auto;
}

/* ログインページ */
.login-container {
    max-width: 420px;
    margin: 80px auto;
    background: #16162a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 48px 40px;
}
.login-title {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #e8e8f8;
    margin-bottom: 8px;
}
.login-subtitle {
    text-align: center;
    font-size: 13px;
    color: #6060a0;
    margin-bottom: 32px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
}
.admin-badge {
    display: inline-block;
    background: rgba(124,106,245,0.2);
    color: #a594ff;
    font-size: 10px;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
</style>

""", unsafe_allow_html=True)

# ── 定数 ──────────────────────────────────────────────

SUBJECTS = [
{"id": "roki",    "name": "労働基準法",           "short": "労基"},
{"id": "roan",    "name": "労働安全衛生法",         "short": "労安"},
{"id": "rosai",   "name": "労働者災害補償保険法",    "short": "労災"},
{"id": "koyo",    "name": "雇用保険法",             "short": "雇用"},
{"id": "choshu",  "name": "労働保険徴収法",         "short": "徴収"},
{"id": "kenpo",   "name": "健康保険法",             "short": "健保"},
{"id": "kokunen", "name": "国民年金法",             "short": "国年"},
{"id": "konen",   "name": "厚生年金保険法",         "short": "厚年"},
{"id": "shaichi", "name": "社会保険一般常識",        "short": "社一"},
]
SUBJECT_MAP = {s["id"]: s for s in SUBJECTS}
MODEL_NAME = "claude-haiku-4-5-20251001"

# ══════════════════════════════════════════════════════

# Supabase クライアント

# ══════════════════════════════════════════════════════

@st.cache_resource
def get_supabase():
"""Supabaseクライアントを返す。secrets未設定時はNone。"""
try:
from supabase import create_client, Client
url  = st.secrets["supabase"]["url"]
key  = st.secrets["supabase"]["anon_key"]
return create_client(url, key)
except Exception:
return None

def supabase_ok() -> bool:
return get_supabase() is not None

# ══════════════════════════════════════════════════════

# 認証ユーティリティ

# ══════════════════════════════════════════════════════

def do_login(email: str, password: str) -> tuple[bool, str]:
"""Supabase Auth でログインし、admin ロールか確認する。"""
sb = get_supabase()
if sb is None:
return False, "Supabase が設定されていません。"
try:
res = sb.auth.sign_in_with_password({"email": email, "password": password})
user = res.user
if user is None:
return False, "メールアドレスまたはパスワードが正しくありません。"

```
    # user_metadata の role が "admin" か確認
    role = (user.user_metadata or {}).get("role", "")
    if role != "admin":
        sb.auth.sign_out()
        return False, "admin 権限がありません。"

    # セッション情報を st.session_state に保存
    st.session_state["auth_user_id"]    = user.id
    st.session_state["auth_email"]      = user.email
    st.session_state["auth_logged_in"]  = True
    st.session_state["auth_token"]      = res.session.access_token
    st.session_state["auth_refresh"]    = res.session.refresh_token
    return True, ""
except Exception as e:
    return False, str(e)
```

def do_logout():
sb = get_supabase()
if sb:
try:
sb.auth.sign_out()
except Exception:
pass
for key in ["auth_user_id", "auth_email", "auth_logged_in", "auth_token", "auth_refresh"]:
st.session_state.pop(key, None)

def is_logged_in() -> bool:
"""ログイン済みかどうか確認。トークンの有効性も検証。"""
if not st.session_state.get("auth_logged_in"):
return False
# トークンをセットして有効性を確認
sb = get_supabase()
if sb is None:
return False
try:
token   = st.session_state.get("auth_token", "")
refresh = st.session_state.get("auth_refresh", "")
if not token:
return False
session = sb.auth.set_session(token, refresh)
if session and session.user:
# トークンが更新された場合は保存
if session.session:
st.session_state["auth_token"]   = session.session.access_token
st.session_state["auth_refresh"] = session.session.refresh_token
return True
return False
except Exception:
return False

# ══════════════════════════════════════════════════════

# データ I/O (Supabase)

# ══════════════════════════════════════════════════════

def load_questions() -> list[dict]:
sb = get_supabase()
if sb is None:
return []
try:
res = sb.table("questions").select("*").execute()
rows = res.data or []
# DB行をアプリ形式に変換
questions = []
for r in rows:
questions.append({
"id":          r["id"],
"subject":     r["subject"],
"question":    r["question"],
"options":     r["options"] if isinstance(r["options"], list) else json.loads(r["options"]),
"answer":      r["answer"],
"explanation": r["explanation"],
})
return questions
except Exception as e:
st.error(f"問題データの読み込みエラー: {e}")
return []

def save_questions(qs: list[dict]):
"""問題リストをSupabaseにupsertする。"""
sb = get_supabase()
if sb is None:
return
try:
rows = []
for q in qs:
rows.append({
"id":          q["id"],
"subject":     q["subject"],
"question":    q["question"],
"options":     q["options"],
"answer":      q["answer"],
"explanation": q["explanation"],
})
sb.table("questions").upsert(rows).execute()
except Exception as e:
st.error(f"問題データの保存エラー: {e}")

def load_progress() -> dict:
sb = get_supabase()
if sb is None:
return {}
try:
res = sb.table("progress").select("*").execute()
prog = {}
for r in (res.data or []):
prog[r["question_id"]] = {
"correct":     r["correct"],
"count":       r["count"],
"wrong_count": r["wrong_count"],
}
return prog
except Exception as e:
st.error(f"進捗データの読み込みエラー: {e}")
return {}

def save_progress_item(question_id: str, correct: bool, count: int, wrong_count: int):
"""1問分の進捗をSupabaseにupsertする。"""
sb = get_supabase()
if sb is None:
return
try:
sb.table("progress").upsert({
"question_id": question_id,
"correct":     correct,
"count":       count,
"wrong_count": wrong_count,
"updated_at":  datetime.now().isoformat(),
}).execute()
except Exception as e:
st.error(f"進捗データの保存エラー: {e}")

def reset_progress_item(question_id: str):
"""1問の進捗をリセット。"""
save_progress_item(question_id, False, 0, 0)

def load_sessions() -> dict:
sb = get_supabase()
if sb is None:
return {}
try:
res = sb.table("quiz_sessions").select("*").execute()
sess = {}
for r in (res.data or []):
sess[r["session_key"]] = {
"index":    r["quiz_index"],
"total":    r["total"],
"score":    r["score"],
"saved_at": r["saved_at"],
}
return sess
except Exception:
return {}

def save_session_item(key: str, index: int, total: int, score: int):
sb = get_supabase()
if sb is None:
return
try:
sb.table("quiz_sessions").upsert({
"session_key": key,
"quiz_index":  index,
"total":       total,
"score":       score,
"saved_at":    datetime.now().isoformat(),
}).execute()
except Exception as e:
st.error(f"セッション保存エラー: {e}")

def clear_session(key: str):
sb = get_supabase()
if sb is None:
return
try:
sb.table("quiz_sessions").delete().eq("session_key", key).execute()
except Exception:
pass

# ── ユーティリティ ────────────────────────────────────

def get_subject_stats(subject_id: str, questions: list, progress: dict) -> dict:
qs       = [q for q in questions if q["subject"] == subject_id]
total    = len(qs)
answered = sum(1 for q in qs if q["id"] in progress)
correct  = sum(1 for q in qs if progress.get(q["id"], {}).get("correct", False))
wrong    = sum(
1 for q in qs
if not progress.get(q["id"], {}).get("correct", False)
and progress.get(q["id"], {}).get("wrong_count", 0) > 0
)
rate = round(correct / answered * 100) if answered > 0 else 0
return {"total": total, "answered": answered, "correct": correct, "wrong": wrong, "rate": rate}

def get_wrong_questions(questions: list, progress: dict, subject_id: str = None) -> list:
result = []
for q in questions:
p = progress.get(q["id"], {})
if p.get("wrong_count", 0) > 0 and not p.get("correct", False):
if subject_id is None or q["subject"] == subject_id:
result.append(q)
return result

# ── セッション state 初期化 ───────────────────────────

def init_state():
defaults = {
"page":              "home",
"quiz_questions":    [],
"quiz_index":        0,
"quiz_score":        0,
"quiz_subject":      None,
"quiz_mode":         None,
"answered":          False,
"selected_option":   None,
"api_key":           "",
"gen_log":           [],
"auth_logged_in":    False,
"auth_user_id":      None,
"auth_email":        None,
"auth_token":        None,
"auth_refresh":      None,
}
for k, v in defaults.items():
if k not in st.session_state:
st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════

# ログインページ

# ══════════════════════════════════════════════════════

def render_login_page():
st.markdown("""
<div style="max-width:420px;margin:60px auto;">
<div style="text-align:center;margin-bottom:32px;">
<div style="font-size:48px;">📚</div>
<div style="font-size:26px;font-weight:700;color:#e8e8f8;margin-top:8px;">社労士 Study</div>
<div style="font-size:12px;color:#5050a0;font-family:'DM Mono',monospace;letter-spacing:2px;margin-top:4px;">SR EXAM TRAINER</div>
</div>
</div>
""", unsafe_allow_html=True)

```
# フォームを中央のカラムに配置
_, col, _ = st.columns([1, 2, 1])
with col:
    st.markdown("""
    <div style="background:#16162a;border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;padding:36px 32px;margin-top:0;">
        <div style="text-align:center;margin-bottom:24px;">
            <span style="background:rgba(124,106,245,0.2);color:#a594ff;font-size:10px;
                font-family:'DM Mono',monospace;padding:4px 14px;border-radius:4px;letter-spacing:2px;">
                ADMIN LOGIN
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    email    = st.text_input("メールアドレス", placeholder="admin@example.com")
    password = st.text_input("パスワード", type="password", placeholder="••••••••")

    if st.button("ログイン", use_container_width=True):
        if not email or not password:
            st.error("メールアドレスとパスワードを入力してください。")
        else:
            with st.spinner("認証中…"):
                ok, msg = do_login(email, password)
            if ok:
                st.success("ログインしました！")
                st.rerun()
            else:
                st.error(f"ログイン失敗: {msg}")

    if not supabase_ok():
        st.warning("⚠️ Supabase が未設定です。`.streamlit/secrets.toml` を確認してください。")
```

# ── クイズ開始 ────────────────────────────────────────

def start_quiz(subject_id: str, mode: str, questions: list, progress: dict):
if mode == "wrong":
qs = get_wrong_questions(questions, progress, subject_id if subject_id != "all" else None)
elif subject_id == "all":
qs = questions[:]
else:
qs = [q for q in questions if q["subject"] == subject_id]

```
if not qs:
    st.warning("この条件の問題がありません。")
    return

random.shuffle(qs)
session_key = f"{subject_id}_{mode}"
saved       = load_sessions().get(session_key)

st.session_state.update({
    "page":               "quiz",
    "quiz_questions":     qs,
    "quiz_index":         0,
    "quiz_score":         0,
    "quiz_subject":       subject_id,
    "quiz_mode":          mode,
    "quiz_session_key":   session_key,
    "quiz_saved_session": saved,
    "answered":           False,
    "selected_option":    None,
    "session_confirmed":  False,
})
```

# ── サイドバー ────────────────────────────────────────

def render_sidebar(questions, progress):
with st.sidebar:
st.markdown("## 📚 社労士 Study")
st.caption("SR EXAM TRAINER")
st.divider()

```
    # ログイン情報
    email = st.session_state.get("auth_email", "")
    st.markdown(f"""
    <div style="background:rgba(124,106,245,0.1);border:1px solid rgba(124,106,245,0.2);
        border-radius:8px;padding:10px 14px;margin-bottom:12px;">
        <div style="font-size:10px;color:#7c6af5;font-family:'DM Mono',monospace;letter-spacing:1px;">ADMIN</div>
        <div style="font-size:12px;color:#c0c0d8;margin-top:2px;word-break:break-all;">{email}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔓 ログアウト", use_container_width=True):
        do_logout()
        st.rerun()

    st.divider()

    if st.button("🏠  ダッシュボード", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    wrong_count = len(get_wrong_questions(questions, progress))
    wrong_label = f"⚠️  間違えた問題　`{wrong_count}`" if wrong_count > 0 else "⚠️  間違えた問題"
    if st.button(wrong_label, use_container_width=True):
        st.session_state.page = "wrong"
        st.rerun()

    if st.button("✨  問題を生成・追加", use_container_width=True):
        st.session_state.page = "generate"
        st.rerun()

    st.divider()
    st.caption("科目別")

    for s in SUBJECTS:
        stats = get_subject_stats(s["id"], questions, progress)
        label = f"**{s['short']}**　{stats['answered']}/{stats['total']}"
        if stats["wrong"] > 0:
            label += f"　🔴{stats['wrong']}"
        if st.button(label, key=f"nav_{s['id']}", use_container_width=True):
            start_quiz(s["id"], "all", questions, progress)
            st.rerun()

    st.divider()
    st.caption("☁️ データはSupabaseに保存されます")
```

# ══════════════════════════════════════════════════════

# 認証ガード

# ══════════════════════════════════════════════════════

if not is_logged_in():
render_login_page()
st.stop()

# ════════════════════════════════════════════════════════

# ログイン済み: データ読み込み & ページ描画

# ════════════════════════════════════════════════════════

questions = load_questions()
progress  = load_progress()
render_sidebar(questions, progress)

# ─── HOME ─────────────────────────────────────────────

if st.session_state.page == "home":
st.markdown("# 学習ダッシュボード")
st.caption("今日も合格に向けて一歩ずつ")
st.write("")

```
total_q     = len(questions)
total_ans   = sum(1 for q in questions if q["id"] in progress)
total_cor   = sum(1 for q in questions if progress.get(q["id"], {}).get("correct", False))
total_wrong = len(get_wrong_questions(questions, progress))
accuracy    = f"{round(total_cor / total_ans * 100)}%" if total_ans > 0 else "--"

c1, c2, c3, c4 = st.columns(4)
c1.metric("総問題数", total_q)
c2.metric("解答済み", total_ans)
c3.metric("正答率",   accuracy)
c4.metric("要復習",   total_wrong)

st.write("")
st.markdown("### 科目別進捗")

cols = st.columns(3)
for i, s in enumerate(SUBJECTS):
    stats     = get_subject_stats(s["id"], questions, progress)
    pct       = round(stats["answered"] / stats["total"] * 100) if stats["total"] > 0 else 0
    bar_color = "progress-inner-green" if stats["rate"] >= 80 else ""

    with cols[i % 3]:
        wrong_badge = f'<span class="wrong-tag">要復習 {stats["wrong"]}</span>' if stats["wrong"] > 0 else ""
        st.markdown(f"""
        <div class="subject-card">
            <div><span class="subject-tag">{s['short']}</span>{wrong_badge}</div>
            <div style="font-size:15px;font-weight:500;color:#e0e0f0;margin:8px 0 12px;">{s['name']}</div>
            <div class="progress-outer"><div class="progress-inner {bar_color}" style="width:{pct}%"></div></div>
            <div style="display:flex;justify-content:space-between;font-size:12px;color:#7070a0;">
                <span>✓ 正解 {stats['correct']}</span>
                <span>✗ 要復習 {stats['wrong']}</span>
                <span style="color:#a594ff;font-family:'DM Mono',monospace;">{stats['rate']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶ {s['short']} を始める", key=f"start_{s['id']}", use_container_width=True):
            start_quiz(s["id"], "all", questions, progress)
            st.rerun()
```

# ─── QUIZ ─────────────────────────────────────────────

elif st.session_state.page == "quiz":
qs    = st.session_state.quiz_questions
total = len(qs)

```
if st.session_state.get("quiz_saved_session") and not st.session_state.get("session_confirmed"):
    saved = st.session_state.quiz_saved_session
    st.info(f"前回の続きがあります（{saved['index']}/{saved['total']}問）。再開しますか？")
    col_a, col_b = st.columns(2)
    if col_a.button("▶ 続きから再開"):
        st.session_state.quiz_index  = saved["index"]
        st.session_state.quiz_score  = saved["score"]
        st.session_state.session_confirmed = True
        st.rerun()
    if col_b.button("↺ 最初からやり直す"):
        clear_session(st.session_state.quiz_session_key)
        st.session_state.session_confirmed = True
        st.rerun()
    st.stop()

if not st.session_state.get("session_confirmed"):
    st.session_state.session_confirmed = True

idx = st.session_state.quiz_index

subj_info  = SUBJECT_MAP.get(st.session_state.quiz_subject, {"name": "全科目", "short": "--"})
col_back, col_meta = st.columns([1, 5])
if col_back.button("← 戻る"):
    save_session_item(
        st.session_state.quiz_session_key,
        idx, total, st.session_state.quiz_score
    )
    st.session_state.page = "home"
    st.session_state.session_confirmed = False
    st.rerun()

with col_meta:
    st.markdown(f"**{subj_info['name']}**　`{idx + 1} / {total} 問`")

pct = round((idx + 1) / total * 100)
st.markdown(f"""
<div class="progress-outer">
    <div class="progress-inner" style="width:{pct}%"></div>
</div>
""", unsafe_allow_html=True)
st.write("")

q      = qs[idx]
q_subj = SUBJECT_MAP.get(q["subject"], {"name": ""})
labels = ["Ａ", "Ｂ", "Ｃ", "Ｄ", "Ｅ"]

st.markdown(f"""
<div class="question-card">
    <div class="question-number">Q {str(idx + 1).zfill(2)} ─ {q_subj['name']}</div>
    <div class="question-text">{q['question']}</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.answered:
    choice = st.radio(
        "選択してください",
        options=list(range(len(q["options"]))),
        format_func=lambda i: f"{labels[i]}　{q['options'][i]}",
        key=f"radio_{idx}",
        label_visibility="collapsed",
    )
    if st.button("解答する", key=f"answer_{idx}"):
        is_correct = (choice == q["answer"])
        prog = load_progress()
        existing = prog.get(q["id"], {"correct": False, "count": 0, "wrong_count": 0})
        new_count = existing["count"] + 1
        new_wrong = existing["wrong_count"]
        if is_correct:
            new_correct = True
            st.session_state.quiz_score += 1
        else:
            new_correct = False
            new_wrong  += 1

        save_progress_item(q["id"], new_correct, new_count, new_wrong)
        save_session_item(
            st.session_state.quiz_session_key,
            idx, total, st.session_state.quiz_score
        )

        st.session_state.selected_option = choice
        st.session_state.answered        = True
        st.rerun()

else:
    selected   = st.session_state.selected_option
    is_correct = (selected == q["answer"])

    for i, opt in enumerate(q["options"]):
        if i == q["answer"]:
            icon = "✅"
        elif i == selected and not is_correct:
            icon = "❌"
        else:
            icon = "　"
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid rgba(255,255,255,0.08);
            border-radius:10px;padding:12px 18px;margin:6px 0;font-size:14px;color:#c0c0e0;">
            {icon} {labels[i]}　{opt}
        </div>
        """, unsafe_allow_html=True)

    if is_correct:
        st.markdown('<div class="correct-box">✓ 正解！</div>', unsafe_allow_html=True)
    else:
        correct_text = q["options"][q["answer"]]
        st.markdown(
            f'<div class="wrong-box">✗ 不正解　正解：{labels[q["answer"]]}　{correct_text}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"""
    <div class="explanation-box">
        <div class="explanation-label">EXPLANATION</div>
        {q['explanation']}
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    next_label = "次の問題 →" if idx + 1 < total else "結果を見る 🎯"
    if st.button(next_label, key=f"next_{idx}"):
        if idx + 1 >= total:
            clear_session(st.session_state.quiz_session_key)
            st.session_state.page = "result"
        else:
            st.session_state.quiz_index     += 1
            st.session_state.answered        = False
            st.session_state.selected_option = None
        st.rerun()
```

# ─── RESULT ──────────────────────────────────────────

elif st.session_state.page == "result":
score = st.session_state.quiz_score
total = len(st.session_state.quiz_questions)
pct   = round(score / total * 100) if total > 0 else 0
icon  = "🎯" if pct >= 70 else "📚" if pct >= 50 else "💪"

```
st.write("")
st.markdown(f"<div style='text-align:center;font-size:56px;'>{icon}</div>", unsafe_allow_html=True)
st.markdown(
    f"<div style='text-align:center;font-size:56px;font-weight:700;color:#a594ff;"
    f"font-family:DM Mono,monospace;'>{score} / {total}</div>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div style='text-align:center;font-size:16px;color:#7070a0;margin-top:8px;'>正答率　{pct}%</div>",
    unsafe_allow_html=True,
)
st.write("")

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("間違いを復習する", use_container_width=True):
        start_quiz("all", "wrong", questions, progress)
        st.rerun()
with col3:
    if st.button("ホームに戻る", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
```

# ─── WRONG REVIEW ─────────────────────────────────────

elif st.session_state.page == "wrong":
wrong_qs = get_wrong_questions(questions, progress)
st.markdown("# ⚠️ 間違えた問題")
st.caption(f"要復習の問題が **{len(wrong_qs)}** 件あります")
st.write("")

```
if wrong_qs:
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("📝 まとめて復習する", use_container_width=True):
            start_quiz("all", "wrong", questions, progress)
            st.rerun()
    with col2:
        if st.button("🗑️ 全てリセット", use_container_width=True):
            prog = load_progress()
            for qid in prog:
                save_progress_item(qid, False, 0, 0)
            st.success("リセットしました")
            st.rerun()

    st.write("")
    for q in wrong_qs:
        s  = SUBJECT_MAP.get(q["subject"], {"short": "--", "name": "--"})
        p  = progress.get(q["id"], {})
        wc = p.get("wrong_count", 0)
        col_q, col_btn = st.columns([5, 1])
        with col_q:
            st.markdown(f"""
            <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
                border-radius:10px;padding:14px 18px;margin:4px 0;
                display:flex;align-items:center;gap:14px;">
                <span style="background:rgba(231,76,60,0.1);color:#e74c3c;font-size:10px;
                    font-family:'DM Mono',monospace;padding:3px 8px;border-radius:4px;white-space:nowrap;">
                    {s['short']}
                </span>
                <span style="flex:1;font-size:13px;color:#a0a0c8;">{q['question'][:60]}…</span>
                <span style="font-size:11px;font-family:'DM Mono',monospace;color:#e74c3c;">×{wc}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            if st.button("解く", key=f"wrong_solve_{q['id']}"):
                st.session_state.update({
                    "page":             "quiz",
                    "quiz_questions":   [q],
                    "quiz_index":       0,
                    "quiz_score":       0,
                    "quiz_subject":     q["subject"],
                    "quiz_mode":        "single",
                    "quiz_session_key": f"single_{q['id']}",
                    "quiz_saved_session": None,
                    "answered":         False,
                    "selected_option":  None,
                    "session_confirmed": True,
                })
                st.rerun()
else:
    st.markdown("""
    <div style="text-align:center;padding:60px;color:#5050a0;">
        <div style="font-size:40px;margin-bottom:16px;">✨</div>
        <div>間違えた問題はありません！</div>
    </div>
    """, unsafe_allow_html=True)
```

# ─── GENERATE ─────────────────────────────────────────

elif st.session_state.page == "generate":
st.markdown("# ✨ 問題を生成・追加")
st.write("")

```
with st.expander("🔑 Anthropic API キー設定", expanded=not bool(st.session_state.api_key)):
    api_key = st.text_input(
        "API キー",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
    )
    if st.button("保存"):
        st.session_state.api_key = api_key
        st.success("保存しました！")

st.divider()

st.markdown("### 🤖 AI で問題を自動生成")
st.caption(f"科目を選択して「生成開始」を押すと、各科目10問を自動生成して追加します。（使用モデル: `{MODEL_NAME}`）")

selected = st.multiselect(
    "生成する科目を選択",
    options=[s["id"] for s in SUBJECTS],
    format_func=lambda x: f"{SUBJECT_MAP[x]['short']} - {SUBJECT_MAP[x]['name']}",
    default=[],
)

if st.button("🚀 選択科目を生成開始", disabled=not (selected and st.session_state.api_key)):
    if not st.session_state.api_key:
        st.error("APIキーを入力してください。")
    elif not selected:
        st.warning("科目を選択してください。")
    else:
        try:
            import anthropic
        except ImportError:
            st.error("anthropic パッケージがインストールされていません。")
            st.stop()

        log_area = st.empty()
        logs     = []

        def log(msg: str, ok: bool = True):
            prefix = "✓ " if ok else "✗ "
            logs.append(prefix + msg)
            log_area.markdown(
                '<div class="log-box">' + "<br>".join(logs[-30:]) + "</div>",
                unsafe_allow_html=True,
            )

        try:
            client = anthropic.Anthropic(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"APIクライアントの初期化に失敗しました: {repr(e)}")
            st.stop()

        qs = load_questions()

        for sid in selected:
            subj     = SUBJECT_MAP[sid]
            existing = [q for q in qs if q["subject"] == sid]
            start_idx = len(existing) + 1

            log(f"{subj['name']} の問題を生成中…")

            prompt = (
                f"社会保険労務士試験の「{subj['name']}」に関する5択問題を10問作成してください。\n"
                f"必ずJSON配列のみ返してください（前後の説明文・```マークは絶対に不要）。\n"
                f"フォーマット例:\n"
                f'[{{"id":"{sid}_{str(start_idx).zfill(3)}","subject":"{sid}",'
                f'"question":"問題文","options":["選択肢A","選択肢B","選択肢C","選択肢D","選択肢E"],'
                f'"answer":0,"explanation":"解説文"}}]\n\n'
                f"ルール:\n"
                f"- answer は 0〜4 の整数（0始まりインデックス）\n"
                f"- 実際の法令条文に基づく正確な内容\n"
                f"- 本試験レベルの難易度\n"
                f"- IDは {sid}_{str(start_idx).zfill(3)} 〜 {sid}_{str(start_idx + 9).zfill(3)}\n"
                f"- 10問ちょうど生成すること"
            )

            try:
                msg = client.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                )

                raw_text = msg.content[0].text.strip()

                if "```" in raw_text:
                    parts = raw_text.split("```")
                    for part in parts:
                        part = part.strip()
                        if part.startswith("json"):
                            part = part[4:].strip()
                        if part.startswith("["):
                            raw_text = part
                            break

                start = raw_text.find("[")
                end   = raw_text.rfind("]")
                if start == -1 or end == -1:
                    raise ValueError(f"JSONの [ ] が見つかりません。応答: {raw_text[:200]}")
                raw_text = raw_text[start:end + 1]

                new_qs       = json.loads(raw_text)
                existing_ids = {q["id"] for q in qs}
                added        = [q for q in new_qs if q["id"] not in existing_ids]

                valid_added = []
                for q in added:
                    required = {"id", "subject", "question", "options", "answer", "explanation"}
                    if not required.issubset(q.keys()):
                        log(f"  → 問題 {q.get('id','?')} のフィールドが不足 (スキップ)", ok=False)
                        continue
                    if not isinstance(q["options"], list) or len(q["options"]) != 5:
                        log(f"  → 問題 {q.get('id','?')} の選択肢が5個でない (スキップ)", ok=False)
                        continue
                    if not isinstance(q["answer"], int) or not (0 <= q["answer"] <= 4):
                        log(f"  → 問題 {q.get('id','?')} の answer が不正 (スキップ)", ok=False)
                        continue
                    valid_added.append(q)

                if valid_added:
                    save_questions(valid_added)
                    qs.extend(valid_added)
                total_now = len([q for q in qs if q["subject"] == sid])
                log(f"{subj['name']}: {len(valid_added)}問追加（合計 {total_now}問）")

            except json.JSONDecodeError as e:
                log(f"{subj['name']}: JSONパースエラー - {repr(e)}", ok=False)
            except Exception as e:
                log(f"{subj['name']}: エラー - {repr(e)}", ok=False)

        log("すべての生成が完了しました！")
        st.success("問題の生成が完了しました！")

st.divider()

st.markdown("### 📋 JSON で問題を追加")
st.caption("以下の形式で問題をインポートできます。")

sample_json = json.dumps([{
    "id": "roki_custom_001",
    "subject": "roki",
    "question": "問題文をここに入力",
    "options": ["選択肢A", "選択肢B", "選択肢C", "選択肢D", "選択肢E"],
    "answer": 0,
    "explanation": "解説文をここに入力",
}], ensure_ascii=False, indent=2)

json_input = st.text_area("JSON を貼り付け", placeholder=sample_json, height=180)
if st.button("📥 インポート"):
    try:
        new_qs       = json.loads(json_input)
        qs           = load_questions()
        existing_ids = {q["id"] for q in qs}
        added        = [q for q in new_qs if q["id"] not in existing_ids]
        if added:
            save_questions(added)
        st.success(f"{len(added)} 問を追加しました！")
        st.rerun()
    except Exception as e:
        st.error(f"JSON の形式が正しくありません: {e}")

st.divider()

st.markdown("### 📊 現在の問題数")
qs   = load_questions()
cols = st.columns(3)
for i, s in enumerate(SUBJECTS):
    count = len([q for q in qs if q["subject"] == s["id"]])
    pct   = min(count / 200 * 100, 100)
    cols[i % 3].markdown(f"""
    <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
        border-radius:10px;padding:14px;margin:4px 0;">
        <div style="font-size:11px;color:#6060a0;font-family:'DM Mono',monospace;">{s['short']}</div>
        <div style="font-size:20px;font-weight:700;color:#a594ff;font-family:'DM Mono',monospace;">
            {count}<span style="font-size:12px;color:#5050a0;">/200</span>
        </div>
        <div class="progress-outer"><div class="progress-inner" style="width:{pct}%"></div></div>
    </div>
    """, unsafe_allow_html=True)
```