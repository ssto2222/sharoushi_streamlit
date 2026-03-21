import streamlit as st
import json
import random
import time
from datetime import datetime

# ── ページ設定

st.set_page_config(
page_title="社労士 学習アプリ",
page_icon="📚",
layout="wide",
initial_sidebar_state="expanded",
)

# ── カスタムCSS

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
.stApp { background-color: #0e0e16; }
section[data-testid="stSidebar"] { background-color: #12121c !important; border-right: 1px solid rgba(255,255,255,0.07); }
section[data-testid="stSidebar"] * { color: #c8c8d8 !important; }
[data-testid="metric-container"] { background: #1a1a28; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px !important; }
[data-testid="metric-container"] label { color: #7070a0 !important; font-size: 11px !important; letter-spacing: 1px; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e0e0f0 !important; font-family: 'DM Mono', monospace !important; }
.stButton > button { background: #7c6af5 !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 500 !important; padding: 10px 24px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #9580ff !important; transform: translateY(-1px) !important; }
.question-card { background: #16162a; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px 32px; margin-bottom: 20px; }
.question-number { font-family: 'DM Mono', monospace; font-size: 11px; color: #6060a0; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; }
.question-text { font-size: 17px; line-height: 1.9; color: #e8e8f8; font-weight: 400; }
.correct-box { background: rgba(46,204,113,0.1); border: 1px solid rgba(46,204,113,0.4); border-radius: 10px; padding: 16px 20px; color: #2ecc71; font-weight: 500; margin: 12px 0; }
.wrong-box { background: rgba(231,76,60,0.1); border: 1px solid rgba(231,76,60,0.4); border-radius: 10px; padding: 16px 20px; color: #e74c3c; font-weight: 500; margin: 12px 0; }
.explanation-box { background: #1a1a2e; border: 1px solid rgba(255,255,255,0.06); border-left: 3px solid #7c6af5; border-radius: 0 10px 10px 0; padding: 18px 20px; color: #a0a0c8; font-size: 14px; line-height: 1.9; margin-top: 14px; }
.explanation-label { font-family: 'DM Mono', monospace; font-size: 10px; color: #7c6af5; letter-spacing: 2px; margin-bottom: 8px; }
.progress-outer { background: #1e1e30; border-radius: 4px; height: 6px; margin: 6px 0 10px; overflow: hidden; }
.progress-inner { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #7c6af5, #a594ff); transition: width 0.4s ease; }
.progress-inner-green { background: linear-gradient(90deg, #27ae60, #2ecc71); }
.subject-card { background: #16162a; border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 20px; margin-bottom: 10px; cursor: pointer; transition: border-color 0.2s; }
.subject-card:hover { border-color: #7c6af5; }
.subject-tag { display: inline-block; background: rgba(124,106,245,0.15); color: #a594ff; font-size: 10px; font-family: 'DM Mono', monospace; padding: 3px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 10px; }
.wrong-tag { display: inline-block; background: rgba(231,76,60,0.1); color: #e74c3c; font-size: 10px; font-family: 'DM Mono', monospace; padding: 3px 10px; border-radius: 20px; margin-left: 8px; }
.stRadio > div { gap: 8px !important; }
.stRadio > div > label { background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; padding: 14px 18px !important; width: 100% !important; color: #c8c8e8 !important; transition: all 0.15s !important; font-size: 14px !important; line-height: 1.6 !important; }
.stRadio > div > label:hover { border-color: #7c6af5 !important; background: rgba(124,106,245,0.08) !important; }
h1 { color: #e8e8f8 !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2, h3 { color: #d0d0e8 !important; font-weight: 500 !important; }
p, li { color: #9090b8 !important; }
hr { border-color: rgba(255,255,255,0.07) !important; }
.log-box { background: #0e0e16; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 14px; font-family: 'DM Mono', monospace; font-size: 12px; color: #7070a0; max-height: 300px; overflow-y: auto; }

/* ── 広告カード */
.ad-section-label {
    font-size: 10px; color: #5050a0; font-family: 'DM Mono', monospace;
    letter-spacing: 2px; margin-bottom: 10px; text-align: right;
}
.ad-card {
    display: flex; align-items: center; gap: 16px;
    background: linear-gradient(135deg, #16162a 0%, #1a1828 100%);
    border: 1px solid rgba(245,197,66,0.25);
    border-radius: 14px; padding: 16px 20px; margin-bottom: 10px;
    text-decoration: none;
    transition: border-color 0.2s, transform 0.15s;
}
.ad-card:hover { border-color: rgba(245,197,66,0.6); transform: translateY(-2px); }
.ad-card-img {
    width: 72px; height: 72px; object-fit: cover;
    border-radius: 8px; flex-shrink: 0;
}
.ad-card-img-placeholder {
    width: 72px; height: 72px; border-radius: 8px; flex-shrink: 0;
    background: rgba(124,106,245,0.15);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
}
.ad-card-body { flex: 1; min-width: 0; }
.ad-card-title {
    font-size: 14px; font-weight: 600; color: #e8e8f0;
    margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.ad-card-desc { font-size: 12px; color: #8080a8; line-height: 1.6; }
.ad-card-badge {
    font-size: 10px; font-family: 'DM Mono', monospace;
    background: rgba(245,197,66,0.15); color: #f5c542;
    padding: 2px 8px; border-radius: 4px; flex-shrink: 0;
}
</style>

""", unsafe_allow_html=True)

# ── 定数

SUBJECTS = [
{"id": "roki",    "name": "労働基準法",             "short": "労基"},
{"id": "roan",    "name": "労働安全衛生法",           "short": "労安"},
{"id": "rosai",   "name": "労働者災害補償保険法",      "short": "労災"},
{"id": "koyo",    "name": "雇用保険法",               "short": "雇用"},
{"id": "choshu",  "name": "労働保険徴収法",           "short": "徴収"},
{"id": "kenpo",   "name": "健康保険法",               "short": "健保"},
{"id": "kokunen", "name": "国民年金法",               "short": "国年"},
{"id": "konen",   "name": "厚生年金保険法",           "short": "厚年"},
{"id": "shaichi", "name": "社会保険一般常識",          "short": "社一"},
]
SUBJECT_MAP        = {s["id"]: s for s in SUBJECTS}
MODEL_NAME         = "claude-haiku-4-5-20251001"
SESSION_EXPIRE_SEC = 60 * 60 * 24  # 24時間

# ── キャッシュキー

_CACHE_Q  = "_cache_questions"
_CACHE_P  = "_cache_progress"
_CACHE_AD = "_cache_ads"

# ══════════════════════════════════════════════════════

# Supabase

# ══════════════════════════════════════════════════════

@st.cache_resource
def get_supabase():
try:
from supabase import create_client
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["anon_key"]
return create_client(url, key)
except Exception:
return None

def supabase_ok():
return get_supabase() is not None

# ══════════════════════════════════════════════════════

# 認証

# ══════════════════════════════════════════════════════

def do_login(email: str, password: str) -> tuple[bool, str]:
sb = get_supabase()
if not sb:
return False, "Supabase が設定されていません"
try:
res  = sb.auth.sign_in_with_password({"email": email, "password": password})
user = res.user
if not user:
return False, "メールアドレスまたはパスワードが違います"
if user.user_metadata.get("role") != "admin":
return False, "admin 権限がありません"
st.session_state["access_token"]  = res.session.access_token
st.session_state["refresh_token"] = res.session.refresh_token
st.session_state["login_at"]      = time.time()
st.session_state["auth_email"]    = email
cache_invalidate()
return True, ""
except Exception as e:
return False, f"ログイン失敗: {e}"

def is_logged_in() -> bool:
login_at = st.session_state.get("login_at", 0)
if time.time() - login_at > SESSION_EXPIRE_SEC:
return False
sb      = get_supabase()
if not sb:
return False
token   = st.session_state.get("access_token")
refresh = st.session_state.get("refresh_token")
if not token or not refresh:
return False
try:
sb.auth.set_session(token, refresh)
return True
except Exception:
return False

def do_logout():
sb = get_supabase()
if sb:
try:
sb.auth.sign_out()
except Exception:
pass
cache_invalidate()
for key in ["access_token", "refresh_token", "login_at", "auth_email",
"auth_user_id", "auth_logged_in", "auth_token", "auth_refresh"]:
st.session_state.pop(key, None)

# ══════════════════════════════════════════════════════

# キャッシュ管理

# 読み取り : キャッシュ優先（DB アクセスなし）

# 書き込み : DB upsert ＋ キャッシュ即時更新 or 破棄

# 破棄タイミング : ログイン・ログアウト・問題追加・進捗リセット・広告変更

# ══════════════════════════════════════════════════════

def cache_invalidate():
st.session_state.pop(_CACHE_Q,  None)
st.session_state.pop(_CACHE_P,  None)
st.session_state.pop(_CACHE_AD, None)

# ── 問題データ

def load_questions():
if _CACHE_Q in st.session_state:
return st.session_state[_CACHE_Q]
sb = get_supabase()
if sb is None:
return []
try:
res    = sb.table("questions").select("*").execute()
result = []
for r in (res.data or []):
result.append({
"id":          r["id"],
"subject":     r["subject"],
"question":    r["question"],
"options":     r["options"] if isinstance(r["options"], list)
else json.loads(r["options"]),
"answer":      r["answer"],
"explanation": r["explanation"],
})
st.session_state[_CACHE_Q] = result
return result
except Exception as e:
st.error(f"問題データの読み込みエラー: {e}")
return []

def save_questions(qs):
sb = get_supabase()
if sb is None:
return
try:
rows = [{
"id":          q["id"],
"subject":     q["subject"],
"question":    q["question"],
"options":     q["options"],
"answer":      q["answer"],
"explanation": q["explanation"],
} for q in qs]
sb.table("questions").upsert(rows).execute()
st.session_state.pop(_CACHE_Q, None)
except Exception as e:
st.error(f"問題データの保存エラー: {e}")

# ── 進捗データ

def load_progress():
if _CACHE_P in st.session_state:
return st.session_state[_CACHE_P]
sb = get_supabase()
if sb is None:
return {}
try:
res  = sb.table("progress").select("*").execute()
prog = {}
for r in (res.data or []):
prog[r["question_id"]] = {
"correct":     r["correct"],
"count":       r["count"],
"wrong_count": r["wrong_count"],
}
st.session_state[_CACHE_P] = prog
return prog
except Exception as e:
st.error(f"進捗データの読み込みエラー: {e}")
return {}

def save_progress_item(question_id, correct, count, wrong_count):
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
prog = st.session_state.get(_CACHE_P, {})
prog[question_id] = {"correct": correct, "count": count, "wrong_count": wrong_count}
st.session_state[_CACHE_P] = prog
except Exception as e:
st.error(f"進捗データの保存エラー: {e}")

# ── 広告データ

def load_ads(active_only: bool = True):
"""
active_only=True  → 有効な広告のみ（表示用）
active_only=False → 全件（管理画面用）
キャッシュは表示用（active_only）のみ利用。管理画面は常に DB から取得。
"""
if active_only and _CACHE_AD in st.session_state:
return st.session_state[_CACHE_AD]
sb = get_supabase()
if sb is None:
return []
try:
query = sb.table("ads").select("*").order("sort_order")
if active_only:
query = query.eq("is_active", True)
res  = query.execute()
ads  = res.data or []
if active_only:
st.session_state[_CACHE_AD] = ads
return ads
except Exception as e:
st.error(f"広告データの読み込みエラー: {e}")
return []

def save_ad(ad: dict):
"""広告を upsert してキャッシュ破棄。"""
sb = get_supabase()
if sb is None:
return False
try:
sb.table("ads").upsert(ad).execute()
st.session_state.pop(_CACHE_AD, None)
return True
except Exception as e:
st.error(f"広告の保存エラー: {e}")
return False

def delete_ad(ad_id: int):
"""広告を削除してキャッシュ破棄。"""
sb = get_supabase()
if sb is None:
return False
try:
sb.table("ads").delete().eq("id", ad_id).execute()
st.session_state.pop(_CACHE_AD, None)
return True
except Exception as e:
st.error(f"広告の削除エラー: {e}")
return False

# ── セッションデータ

def load_sessions():
sb = get_supabase()
if sb is None:
return {}
try:
res  = sb.table("quiz_sessions").select("*").execute()
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

def save_session_item(key, index, total, score):
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

def clear_session(key):
sb = get_supabase()
if sb is None:
return
try:
sb.table("quiz_sessions").delete().eq("session_key", key).execute()
except Exception:
pass

# ══════════════════════════════════════════════════════

# ユーティリティ

# ══════════════════════════════════════════════════════

def get_subject_stats(subject_id, questions, progress):
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

def get_wrong_questions(questions, progress, subject_id=None):
result = []
for q in questions:
p = progress.get(q["id"], {})
if p.get("wrong_count", 0) > 0 and not p.get("correct", False):
if subject_id is None or q["subject"] == subject_id:
result.append(q)
return result

def render_ads():
"""有効な広告をカード形式で表示（弱点復習ページ用）。"""
ads = load_ads(active_only=True)
if not ads:
return
st.markdown(’<div class="ad-section-label">PR・おすすめ教材</div>’, unsafe_allow_html=True)
for ad in ads:
img_html = (
f’<img src="{ad["image_url"]}" class="ad-card-img" onerror="this.style.display='none'">’
if ad.get("image_url") else
f’<div class="ad-card-img-placeholder">{ad.get("emoji", "📖")}</div>’
)
st.markdown(f"""
<a href="{ad.get('link_url','#')}" target="_blank" class="ad-card" rel="noopener noreferrer">
{img_html}
<div class="ad-card-body">
<div class="ad-card-title">{ad.get(‘title’,’’)}</div>
<div class="ad-card-desc">{ad.get(‘description’,’’)}</div>
</div>
<div class="ad-card-badge">詳細 →</div>
</a>
""", unsafe_allow_html=True)
st.write("")

# ── セッション state 初期化

def init_state():
defaults = {
"page":             "home",
"quiz_questions":   [],
"quiz_index":       0,
"quiz_score":       0,
"quiz_subject":     None,
"quiz_mode":        None,
"answered":         False,
"selected_option":  None,
"api_key":          "",
"gen_log":          [],
"auth_logged_in":   False,
"auth_user_id":     None,
"auth_email":       None,
"auth_token":       None,
"auth_refresh":     None,
"ad_edit_id":       None,  # 編集中の広告ID
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
<div style="max-width:420px;margin:60px auto;text-align:center;">
<div style="font-size:48px;">📚</div>
<div style="font-size:26px;font-weight:700;color:#e8e8f8;margin-top:8px;">社労士 Study</div>
<div style="font-size:12px;color:#5050a0;font-family:'DM Mono',monospace;letter-spacing:2px;margin-top:4px;">SR EXAM TRAINER</div>
</div>
""", unsafe_allow_html=True)

```
_, col, _ = st.columns([1, 2, 1])
with col:
    st.markdown("""
    <div style="background:#16162a;border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;padding:36px 32px;">
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
        st.warning("Supabase が未設定です。.streamlit/secrets.toml を確認してください。")
```

# ── クイズ開始

def start_quiz(subject_id, mode, questions, progress):
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

# ── サイドバー

def render_sidebar(questions, progress):
with st.sidebar:
st.markdown("## 📚 社労士 Study")
st.caption("SR EXAM TRAINER")
st.divider()

```
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

    if st.button("📢  広告管理", use_container_width=True):
        st.session_state.page    = "ads"
        st.session_state.ad_edit_id = None
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

# ══════════════════════════════════════════════════════

# ページ描画

# ══════════════════════════════════════════════════════

questions = load_questions()
progress  = load_progress()
render_sidebar(questions, progress)

# ─── HOME ────────────────────────────────────────────

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

# ─── QUIZ ────────────────────────────────────────────

elif st.session_state.page == "quiz":
qs    = st.session_state.quiz_questions
total = len(qs)

```
if st.session_state.get("quiz_saved_session") and not st.session_state.get("session_confirmed"):
    saved = st.session_state.quiz_saved_session
    st.info(f"前回の続きがあります（{saved['index']}/{saved['total']}問）。再開しますか？")
    col_a, col_b = st.columns(2)
    if col_a.button("▶ 続きから再開"):
        st.session_state.quiz_index        = saved["index"]
        st.session_state.quiz_score        = saved["score"]
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

subj_info          = SUBJECT_MAP.get(st.session_state.quiz_subject, {"name": "全科目", "short": "--"})
col_back, col_meta = st.columns([1, 5])
if col_back.button("← 戻る"):
    save_session_item(st.session_state.quiz_session_key, idx, total, st.session_state.quiz_score)
    st.session_state.page              = "home"
    st.session_state.session_confirmed = False
    st.rerun()

with col_meta:
    st.markdown(f"**{subj_info['name']}**　`{idx + 1} / {total} 問`")

bar_pct = round((idx + 1) / total * 100)
st.markdown(f'<div class="progress-outer"><div class="progress-inner" style="width:{bar_pct}%"></div></div>', unsafe_allow_html=True)
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
        prog       = load_progress()
        existing   = prog.get(q["id"], {"correct": False, "count": 0, "wrong_count": 0})
        new_count  = existing["count"] + 1
        new_wrong  = existing["wrong_count"]
        if is_correct:
            new_correct = True
            st.session_state.quiz_score += 1
        else:
            new_correct = False
            new_wrong  += 1
        save_progress_item(q["id"], new_correct, new_count, new_wrong)
        save_session_item(st.session_state.quiz_session_key, idx, total, st.session_state.quiz_score)
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
        st.markdown(f'<div class="wrong-box">✗ 不正解　正解：{labels[q["answer"]]}　{correct_text}</div>', unsafe_allow_html=True)

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
st.markdown(f"<div style='text-align:center;font-size:56px;font-weight:700;color:#a594ff;font-family:DM Mono,monospace;'>{score} / {total}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;font-size:16px;color:#7070a0;margin-top:8px;'>正答率　{pct}%</div>", unsafe_allow_html=True)
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

# ─── WRONG REVIEW ────────────────────────────────────

elif st.session_state.page == "wrong":
wrong_qs = get_wrong_questions(questions, progress)
st.markdown("# ⚠️ 間違えた問題")
st.caption(f"要復習の問題が **{len(wrong_qs)}** 件あります")
st.write("")

```
# ── 広告スペース（弱点復習ページ上部）
render_ads()

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
            cache_invalidate()
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
                    "page":               "quiz",
                    "quiz_questions":     [q],
                    "quiz_index":         0,
                    "quiz_score":         0,
                    "quiz_subject":       q["subject"],
                    "quiz_mode":          "single",
                    "quiz_session_key":   f"single_{q['id']}",
                    "quiz_saved_session": None,
                    "answered":           False,
                    "selected_option":    None,
                    "session_confirmed":  True,
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

# ─── GENERATE ────────────────────────────────────────

elif st.session_state.page == "generate":
st.markdown("# ✨ 問題を生成・追加")
st.write("")

```
with st.expander("🔑 Anthropic API キー設定", expanded=not bool(st.session_state.api_key)):
    api_key = st.text_input("API キー", value=st.session_state.api_key, type="password", placeholder="sk-ant-...")
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

        def log(msg, ok=True):
            prefix = "✓ " if ok else "✗ "
            logs.append(prefix + msg)
            log_area.markdown('<div class="log-box">' + "<br>".join(logs[-30:]) + "</div>", unsafe_allow_html=True)

        try:
            client = anthropic.Anthropic(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"APIクライアントの初期化に失敗しました: {repr(e)}")
            st.stop()

        qs = load_questions()

        for sid in selected:
            subj      = SUBJECT_MAP[sid]
            existing  = [q for q in qs if q["subject"] == sid]
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
                msg      = client.messages.create(model=MODEL_NAME, max_tokens=4096, messages=[{"role": "user", "content": prompt}])
                raw_text = msg.content[0].text.strip()

                if "```" in raw_text:
                    for part in raw_text.split("```"):
                        part = part.strip()
                        if part.startswith("json"):
                            part = part[4:].strip()
                        if part.startswith("["):
                            raw_text = part
                            break

                start_i = raw_text.find("[")
                end_i   = raw_text.rfind("]")
                if start_i == -1 or end_i == -1:
                    raise ValueError(f"JSONの [ ] が見つかりません。応答: {raw_text[:200]}")
                raw_text = raw_text[start_i:end_i + 1]

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
    "id": "roki_custom_001", "subject": "roki",
    "question": "問題文をここに入力",
    "options": ["選択肢A", "選択肢B", "選択肢C", "選択肢D", "選択肢E"],
    "answer": 0, "explanation": "解説文をここに入力",
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
    cols[i % 3].markdown(f"""
    <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
        border-radius:10px;padding:14px;margin:4px 0;">
        <div style="font-size:11px;color:#6060a0;font-family:'DM Mono',monospace;">{s['short']}</div>
        <div style="font-size:20px;font-weight:700;color:#a594ff;font-family:'DM Mono',monospace;">
            {count}<span style="font-size:12px;color:#5050a0;">問</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

# ─── ADS MANAGEMENT ──────────────────────────────────

elif st.session_state.page == "ads":
st.markdown("# 📢 広告管理")
st.caption("弱点復習ページに表示するおすすめ教材を管理します")
st.write("")

```
# ── 広告一覧
ads = load_ads(active_only=False)

if ads:
    st.markdown("### 現在の広告")
    for ad in ads:
        status_color = "#2ecc71" if ad.get("is_active") else "#7070a0"
        status_label = "公開中" if ad.get("is_active") else "非公開"
        with st.container():
            col_info, col_actions = st.columns([5, 2])
            with col_info:
                img_tag = ""
                if ad.get("image_url"):
                    img_tag = f'<img src="{ad["image_url"]}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;margin-right:12px;vertical-align:middle;">'
                st.markdown(f"""
                <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
                    border-radius:10px;padding:14px 18px;display:flex;align-items:center;">
                    {img_tag}
                    <div style="flex:1;">
                        <div style="font-size:13px;font-weight:600;color:#e0e0f0;">{ad.get('title','')}</div>
                        <div style="font-size:11px;color:#6060a0;margin-top:2px;">
                            表示順: {ad.get('sort_order', 0)}　|　
                            <span style="color:{status_color};">● {status_label}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_actions:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("編集", key=f"edit_{ad['id']}"):
                        st.session_state.ad_edit_id = ad["id"]
                        st.rerun()
                with c2:
                    if st.button("削除", key=f"del_{ad['id']}"):
                        if delete_ad(ad["id"]):
                            st.success("削除しました")
                            st.rerun()
    st.divider()
else:
    st.info("広告はまだありません。下のフォームから追加してください。")
    st.write("")

# ── 追加 / 編集フォーム
edit_id  = st.session_state.get("ad_edit_id")
edit_ad  = next((a for a in ads if a["id"] == edit_id), {}) if edit_id else {}
form_title = f"### ✏️ 広告を編集" if edit_id else "### ➕ 広告を追加"
st.markdown(form_title)

with st.form("ad_form", clear_on_submit=True):
    title       = st.text_input("タイトル *",
                    value=edit_ad.get("title", ""),
                    placeholder="例: ユーキャン 社労士 通信講座")
    description = st.text_area("説明文",
                    value=edit_ad.get("description", ""),
                    placeholder="例: 合格率業界トップクラス。初学者でも安心のカリキュラム。",
                    height=80)
    link_url    = st.text_input("リンクURL *",
                    value=edit_ad.get("link_url", ""),
                    placeholder="https://example.com/affiliate?id=xxx")
    image_url   = st.text_input("画像URL（空欄の場合は絵文字表示）",
                    value=edit_ad.get("image_url", ""),
                    placeholder="https://example.com/image.jpg")
    col_emoji, col_order, col_active = st.columns([2, 2, 2])
    with col_emoji:
        emoji = st.text_input("絵文字（画像なし時）",
                    value=edit_ad.get("emoji", "📖"),
                    max_chars=2)
    with col_order:
        sort_order = st.number_input("表示順（小さいほど上）",
                    value=int(edit_ad.get("sort_order", len(ads) + 1)),
                    min_value=1, max_value=999)
    with col_active:
        st.write("")
        is_active = st.checkbox("公開する", value=edit_ad.get("is_active", True))

    col_save, col_cancel = st.columns([3, 1])
    with col_save:
        submitted = st.form_submit_button(
            "💾 保存" if edit_id else "➕ 追加",
            use_container_width=True
        )
    with col_cancel:
        cancelled = st.form_submit_button("キャンセル", use_container_width=True)

    if submitted:
        if not title or not link_url:
            st.error("タイトルとリンクURLは必須です。")
        else:
            ad_data = {
                "title":       title,
                "description": description,
                "link_url":    link_url,
                "image_url":   image_url,
                "emoji":       emoji or "📖",
                "sort_order":  sort_order,
                "is_active":   is_active,
            }
            if edit_id:
                ad_data["id"] = edit_id
            if save_ad(ad_data):
                st.success("保存しました！")
                st.session_state.ad_edit_id = None
                st.rerun()

    if cancelled:
        st.session_state.ad_edit_id = None
        st.rerun()

# ── プレビュー
if ads:
    st.divider()
    st.markdown("### 👁️ 表示プレビュー")
    st.caption("弱点復習ページでの見え方")
    render_ads()
```