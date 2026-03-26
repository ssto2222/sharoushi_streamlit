"""
db.py - Supabase接続 + キャッシュ付きデータアクセス層
読み取り: session_stateキャッシュ優先（DBアクセスなし）
書き込み: DB upsert + キャッシュ即時更新 or 破棄
破棄タイミング: ログイン・ログアウト・問題追加・進捗リセット・広告変更
"""
import json
import streamlit as st
from datetime import datetime
from .constants import CACHE_Q, CACHE_P, CACHE_AD, SAMPLE_QUESTIONS


# ── Supabase クライアント

@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["anon_key"]
        return create_client(url, key)
    except Exception:
        return None

def supabase_ok() -> bool:
    return get_supabase() is not None


# ── キャッシュ操作

def cache_invalidate():
    """questions / progress / ads キャッシュを全破棄。"""
    for key in (CACHE_Q, CACHE_P, CACHE_AD):
        st.session_state.pop(key, None)


# ── 問題データ

def load_questions() -> list:
    if CACHE_Q in st.session_state:
        return st.session_state[CACHE_Q]
    sb = get_supabase()
    if sb is None:
        return []
    try:
        res = sb.table("questions").select("*").execute()
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
        if not result:
            return SAMPLE_QUESTIONS
        st.session_state[CACHE_Q] = result
        return result
    except Exception as e:
        st.error(f"問題データの読み込みエラー: {e}")
        return SAMPLE_QUESTIONS


def save_questions(qs: list):
    """DB upsert後、キャッシュを破棄（次回load_questionsで再取得）。"""
    sb = get_supabase()
    if sb is None:
        return
    try:
        rows = [{
            "id": q["id"], "subject": q["subject"], "question": q["question"],
            "options": q["options"], "answer": q["answer"], "explanation": q["explanation"],
        } for q in qs]
        sb.table("questions").upsert(rows).execute()
        st.session_state.pop(CACHE_Q, None)
    except Exception as e:
        st.error(f"問題データの保存エラー: {e}")


def delete_questions_by_subject(subject_id: str) -> int:
    """指定科目の問題を全削除。削除件数を返す。"""
    sb = get_supabase()
    if sb is None:
        return 0
    try:
        qs = load_questions()
        count = len([q for q in qs if q["subject"] == subject_id])
        sb.table("questions").delete().eq("subject", subject_id).execute()
        st.session_state.pop(CACHE_Q, None)
        return count
    except Exception as e:
        st.error(f"問題削除エラー: {e}")
        return 0


def delete_all_questions() -> int:
    """全問題を削除。削除件数を返す。"""
    sb = get_supabase()
    if sb is None:
        return 0
    try:
        qs = load_questions()
        count = len(qs)
        # neq で全行削除（Supabase は条件なし delete を拒否するため）
        sb.table("questions").delete().neq("id", "").execute()
        st.session_state.pop(CACHE_Q, None)
        return count
    except Exception as e:
        st.error(f"問題全削除エラー: {e}")
        return 0


# ── 進捗データ

def load_progress() -> dict:
    if CACHE_P in st.session_state:
        return st.session_state[CACHE_P]
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
        st.session_state[CACHE_P] = prog
        return prog
    except Exception as e:
        st.error(f"進捗データの読み込みエラー: {e}")
        return {}


def save_progress_item(question_id: str, correct: bool, count: int, wrong_count: int):
    """DB upsert + キャッシュの1件だけ上書き（フル再取得なし）。"""
    sb = get_supabase()
    if sb is None:
        return
    try:
        sb.table("progress").upsert({
            "question_id": question_id, "correct": correct,
            "count": count, "wrong_count": wrong_count,
            "updated_at": datetime.now().isoformat(),
        }).execute()
        prog = st.session_state.get(CACHE_P, {})
        prog[question_id] = {"correct": correct, "count": count, "wrong_count": wrong_count}
        st.session_state[CACHE_P] = prog
    except Exception as e:
        st.error(f"進捗データの保存エラー: {e}")


# ── 広告データ

def load_ads(active_only: bool = True) -> list:
    """active_only=True: 表示用（キャッシュ使用）/ False: 管理画面用（常にDB）。"""
    if active_only and CACHE_AD in st.session_state:
        return st.session_state[CACHE_AD]
    sb = get_supabase()
    if sb is None:
        return []
    try:
        query = sb.table("ads").select("*").order("sort_order")
        if active_only:
            query = query.eq("is_active", True)
        res = query.execute()
        ads = res.data or []
        if active_only:
            st.session_state[CACHE_AD] = ads
        return ads
    except Exception as e:
        st.error(f"広告データの読み込みエラー: {e}")
        return []


def save_ad(ad: dict) -> bool:
    sb = get_supabase()
    if sb is None:
        return False
    try:
        sb.table("ads").upsert(ad).execute()
        st.session_state.pop(CACHE_AD, None)
        return True
    except Exception as e:
        st.error(f"広告の保存エラー: {e}")
        return False


def delete_ad(ad_id: int) -> bool:
    sb = get_supabase()
    if sb is None:
        return False
    try:
        sb.table("ads").delete().eq("id", ad_id).execute()
        st.session_state.pop(CACHE_AD, None)
        return True
    except Exception as e:
        st.error(f"広告の削除エラー: {e}")
        return False


# ── セッションデータ（クイズ中断・再開）

def load_sessions() -> dict:
    sb = get_supabase()
    if sb is None:
        return {}
    try:
        res = sb.table("quiz_sessions").select("*").execute()
        sess = {}
        for r in (res.data or []):
            sess[r["session_key"]] = {
                "index": r["quiz_index"], "total": r["total"],
                "score": r["score"],     "saved_at": r["saved_at"],
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
            "session_key": key, "quiz_index": index,
            "total": total, "score": score,
            "saved_at": datetime.now().isoformat(),
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
