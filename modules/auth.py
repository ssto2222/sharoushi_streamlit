"""
auth.py - 認証・セッション管理
role: "admin" -> 全機能
      "user"  -> 学習機能のみ（問題生成・広告管理不可）
"""
import time
import streamlit as st
from datetime import datetime, timedelta
from .constants import SESSION_EXPIRE_SEC
from .db import get_supabase, cache_invalidate

_COOKIE_NAME    = "sharoushi_refresh"
_COOKIE_EXPIRE_DAYS = 30


def _cm():
    """CookieManager を返す（同一キーで重複排除される）。"""
    import extra_streamlit_components as stx
    return stx.CookieManager(key="_sharoushi_cm")


def _save_auth_cookie(refresh_token: str) -> None:
    try:
        expires = datetime.now() + timedelta(days=_COOKIE_EXPIRE_DAYS)
        _cm().set(_COOKIE_NAME, refresh_token, expires_at=expires, key="_set_refresh")
    except Exception:
        pass


def _delete_auth_cookie() -> None:
    try:
        _cm().delete(_COOKIE_NAME, key="_del_refresh")
    except Exception:
        pass


def restore_from_cookie() -> bool:
    """ページロード時に Cookie から Supabase セッションを復元する。"""
    if st.session_state.get("access_token"):
        return True
    try:
        refresh = _cm().get(_COOKIE_NAME)
        if not refresh:
            return False
        sb = get_supabase()
        if not sb:
            return False
        res = sb.auth.refresh_session(refresh)
        if res and res.session:
            _store_session(res)
            return True
    except Exception:
        pass
    return False


def _store_session(res):
    """ログイン/登録成功時にトークンとユーザー情報をセッションに保存。"""
    user = res.user
    role = user.user_metadata.get("role", "user")
    st.session_state["access_token"]  = res.session.access_token
    st.session_state["refresh_token"] = res.session.refresh_token
    st.session_state["login_at"]      = time.time()
    st.session_state["auth_email"]    = user.email
    st.session_state["auth_role"]     = role
    cache_invalidate()
    _save_auth_cookie(res.session.refresh_token)


def do_login(email: str, password: str) -> tuple[bool, str]:
    sb = get_supabase()
    if not sb:
        return False, "Supabase が設定されていません"
    try:
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        if not res.user:
            return False, "メールアドレスまたはパスワードが違います"
        _store_session(res)
        return True, ""
    except Exception as e:
        return False, f"ログイン失敗: {e}"


def do_register(email: str, password: str) -> tuple[bool, str]:
    """一般ユーザー新規登録。role は常に 'user'。"""
    sb = get_supabase()
    if not sb:
        return False, "Supabase が設定されていません"
    try:
        res = sb.auth.sign_up({
            "email":    email,
            "password": password,
            "options":  {"data": {"role": "user"}},
        })
        if not res.user:
            return False, "登録に失敗しました"
        if res.session:
            _store_session(res)
            return True, "registered_and_logged_in"
        return True, "registered_check_email"
    except Exception as e:
        return False, f"登録失敗: {e}"


def do_logout():
    sb = get_supabase()
    if sb:
        try:
            sb.auth.sign_out()
        except Exception:
            pass
    cache_invalidate()
    _delete_auth_cookie()
    for key in ["access_token", "refresh_token", "login_at",
                "auth_email", "auth_role", "auth_user_id"]:
        st.session_state.pop(key, None)


def is_logged_in() -> bool:
    # 24時間チェック
    login_at = st.session_state.get("login_at", 0)
    if time.time() - login_at > SESSION_EXPIRE_SEC:
        return False

    sb = get_supabase()
    if not sb:
        return False
    token   = st.session_state.get("access_token")
    refresh = st.session_state.get("refresh_token")
    if not token or not refresh:
        return False
    try:
        res = sb.auth.set_session(token, refresh)
        # ── トークンが更新された場合は session_state を上書き ──
        if res and res.session:
            st.session_state["access_token"]  = res.session.access_token
            st.session_state["refresh_token"] = res.session.refresh_token
        return True
    except Exception:
        # set_session 失敗時はリフレッシュを試みる
        try:
            res = sb.auth.refresh_session(refresh)
            if res and res.session:
                st.session_state["access_token"]  = res.session.access_token
                st.session_state["refresh_token"] = res.session.refresh_token
                st.session_state["login_at"]      = time.time()
                return True
        except Exception:
            pass
        return False


def is_admin() -> bool:
    return st.session_state.get("auth_role") == "admin"
