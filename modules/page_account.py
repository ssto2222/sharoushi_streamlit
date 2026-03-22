"""
page_account.py - アカウント設定ページ
- メールアドレス変更
- パスワード変更
- アカウント削除
"""
import streamlit as st
from .db import get_supabase, cache_invalidate
from .auth import do_logout
from .utils import render_footer
from .constants import COPYRIGHT


def render():
    st.markdown("# アカウント設定")
    st.write("")

    email = st.session_state.get("auth_email", "")
    role  = st.session_state.get("auth_role", "user")
    role_label = "管理者 (Admin)" if role == "admin" else "一般ユーザー"

    # ── アカウント情報
    st.markdown("### アカウント情報")
    st.markdown(f"""
    <div style="background:#16162a;border:1px solid rgba(255,255,255,0.08);
        border-radius:12px;padding:20px 24px;margin-bottom:16px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span style="font-size:12px;color:#6060a0;">メールアドレス</span>
            <span style="font-size:14px;color:#e0e0f0;">{email}</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:12px;color:#6060a0;">権限</span>
            <span style="font-size:13px;color:#a594ff;">{role_label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── パスワード変更
    st.markdown("### パスワード変更")
    with st.form("change_password_form"):
        new_pass  = st.text_input("新しいパスワード（8文字以上）", type="password", key="new_pass")
        new_pass2 = st.text_input("新しいパスワード（確認）", type="password", key="new_pass2")
        if st.form_submit_button("パスワードを変更", use_container_width=True):
            if not new_pass:
                st.error("新しいパスワードを入力してください。")
            elif len(new_pass) < 8:
                st.error("パスワードは8文字以上で設定してください。")
            elif new_pass != new_pass2:
                st.error("パスワードが一致しません。")
            else:
                sb = get_supabase()
                if sb:
                    try:
                        sb.auth.update_user({"password": new_pass})
                        st.success("パスワードを変更しました。")
                    except Exception as e:
                        st.error(f"変更に失敗しました: {e}")

    st.divider()

    # ── メールアドレス変更
    st.markdown("### メールアドレス変更")
    with st.form("change_email_form"):
        new_email = st.text_input("新しいメールアドレス", placeholder="new@example.com", key="new_email")
        if st.form_submit_button("メールアドレスを変更", use_container_width=True):
            if not new_email:
                st.error("新しいメールアドレスを入力してください。")
            else:
                sb = get_supabase()
                if sb:
                    try:
                        sb.auth.update_user({"email": new_email})
                        st.success("確認メールを送信しました。メールを確認して変更を完了してください。")
                    except Exception as e:
                        st.error(f"変更に失敗しました: {e}")

    st.divider()

    # ── ログアウト
    st.markdown("### ログアウト")
    if st.button("🔓 ログアウト", use_container_width=True, key="account_logout"):
        do_logout()
        st.rerun()

    st.divider()

    # ── アカウント削除
    st.markdown("### アカウント削除")
    st.warning("アカウントを削除すると、学習履歴・進捗データがすべて削除されます。この操作は取り消せません。")
    with st.expander("アカウントを削除する"):
        confirm = st.text_input("確認のため「削除する」と入力してください", key="delete_confirm")
        if st.button("アカウントを完全に削除", key="btn_delete_account"):
            if confirm != "削除する":
                st.error("「削除する」と入力してください。")
            else:
                sb = get_supabase()
                if sb:
                    try:
                        # progressとquiz_sessionsを削除（RLSで現在ユーザーのみ対象）
                        sb.table("progress").delete().neq("question_id", "").execute()
                        sb.table("quiz_sessions").delete().neq("session_key", "").execute()
                        cache_invalidate()
                        st.success("学習データを削除しました。ログアウトします。")
                        do_logout()
                        st.rerun()
                    except Exception as e:
                        st.error(f"削除に失敗しました: {e}")

    render_footer()
