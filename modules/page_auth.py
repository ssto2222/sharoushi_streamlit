"""
page_auth.py - ログイン・新規登録ページ
"""
import streamlit as st
from .auth import do_login, do_register
from .db import supabase_ok
from .utils import render_footer
from .constants import APP_NAME


def render():
    st.markdown(f"""
    <div style="max-width:420px;margin:60px auto;text-align:center;">
        <div style="font-size:48px;">📚</div>
        <div style="font-size:26px;font-weight:700;color:#e8e8f8;margin-top:8px;">{APP_NAME}</div>
        <div style="font-size:12px;color:#5050a0;font-family:'DM Mono',monospace;letter-spacing:2px;margin-top:4px;">SR EXAM TRAINER</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        tab_login, tab_register = st.tabs(["ログイン", "新規登録"])

        with tab_login:
            st.write("")
            email_l    = st.text_input("メールアドレス", placeholder="you@example.com", key="login_email")
            password_l = st.text_input("パスワード", type="password", placeholder="••••••••", key="login_pass")
            st.write("")
            if st.button("ログイン", use_container_width=True, key="btn_login"):
                if not email_l or not password_l:
                    st.error("メールアドレスとパスワードを入力してください。")
                else:
                    with st.spinner("認証中..."):
                        ok, msg = do_login(email_l, password_l)
                    if ok:
                        st.success("ログインしました！")
                        st.rerun()
                    else:
                        st.error(msg)

        with tab_register:
            st.write("")
            st.caption("アカウントを作成して学習を始めましょう。")
            email_r     = st.text_input("メールアドレス", placeholder="you@example.com", key="reg_email")
            password_r  = st.text_input("パスワード（8文字以上）", type="password", placeholder="••••••••", key="reg_pass")
            password_r2 = st.text_input("パスワード（確認）", type="password", placeholder="••••••••", key="reg_pass2")
            st.markdown("""
            <div style="background:rgba(124,106,245,0.07);border:1px solid rgba(124,106,245,0.15);
                border-radius:8px;padding:10px 14px;margin:8px 0;font-size:11px;color:#7070a0;line-height:1.7;">
                登録することで
                <a href="#" style="color:#7c6af5;">プライバシーポリシー</a>
                に同意したものとみなします。
            </div>
            """, unsafe_allow_html=True)
            if st.button("アカウント作成", use_container_width=True, key="btn_register"):
                if not email_r or not password_r:
                    st.error("メールアドレスとパスワードを入力してください。")
                elif len(password_r) < 8:
                    st.error("パスワードは8文字以上で設定してください。")
                elif password_r != password_r2:
                    st.error("パスワードが一致しません。")
                else:
                    with st.spinner("登録中..."):
                        ok, msg = do_register(email_r, password_r)
                    if ok:
                        if msg == "registered_check_email":
                            st.success("確認メールを送信しました。メールを確認してログインしてください。")
                        else:
                            st.success("登録完了！")
                            st.rerun()
                    else:
                        st.error(msg)

        st.write("")
        if st.button("プライバシーポリシーを読む", key="btn_privacy_auth"):
            st.session_state.page = "privacy"
            st.rerun()

        if not supabase_ok():
            st.warning("Supabase が未設定です。.streamlit/secrets.toml を確認してください。")

    render_footer()
