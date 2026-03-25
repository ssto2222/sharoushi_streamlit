"""
app.py - エントリーポイント
ページルーティングのみを担当。ロジックは各モジュールに委譲。

ディレクトリ構成:
  app.py
  modules/
    __init__.py
    constants.py     # 定数（SUBJECTS, MODEL_NAME等）
    styles.py        # カスタムCSS
    db.py            # Supabase接続・キャッシュ付きデータアクセス
    auth.py          # 認証（ログイン・登録・ログアウト・権限確認）
    utils.py         # 共通ユーティリティ（統計・広告表示・フッター）
    sidebar.py       # サイドバー
    page_auth.py     # ログイン・新規登録ページ
    page_dashboard.py # ダッシュボード（ホーム）
    page_quiz.py     # 問題出題・解答・結果・弱点復習
    page_account.py  # アカウント設定
    page_admin.py    # admin: 問題生成・広告管理
    page_privacy.py  # プライバシーポリシー
"""
import streamlit as st

st.set_page_config(
    page_title="社労士 学習アプリ",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── モジュール読み込み
from modules.styles       import inject
from modules.utils        import init_state
from modules.auth         import is_logged_in, is_admin, restore_from_cookie
from modules.db           import load_questions, load_progress
from modules.sidebar      import render as render_sidebar
from modules.page_auth    import render as render_auth
from modules.page_privacy import render as render_privacy
from modules.page_dashboard import render as render_dashboard
from modules.page_quiz    import render_quiz, render_result, render_wrong_review
from modules.page_account import render as render_account
from modules.page_admin   import render_generate, render_ads_management

# ── 初期化
inject()
init_state()
restore_from_cookie()  # Cookie からセッションを復元（ページリロード対策）

# ── プライバシーポリシーは認証不要
if st.session_state.page == "privacy":
    render_privacy()
    st.stop()

# ── 未ログインはログインページへ
if not is_logged_in():
    render_auth()
    st.stop()

# ── admin専用ページへの不正アクセスをブロック
if st.session_state.page in ("generate", "ads") and not is_admin():
    st.session_state.page = "home"
    st.rerun()

# ── データ取得（キャッシュ優先）
questions = load_questions()
progress  = load_progress()

# ── サイドバー
render_sidebar(questions, progress)

# ── ページルーティング
page = st.session_state.page

if page == "home":
    render_dashboard(questions, progress)

elif page == "quiz":
    render_quiz(questions, progress)

elif page == "result":
    render_result(questions, progress)

elif page == "wrong":
    render_wrong_review(questions, progress)

elif page == "account":
    render_account()

elif page == "generate":
    render_generate()

elif page == "ads":
    render_ads_management()

else:
    st.session_state.page = "home"
    st.rerun()
