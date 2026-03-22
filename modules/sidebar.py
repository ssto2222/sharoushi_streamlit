"""
sidebar.py - サイドバー
"""
import streamlit as st
from .constants import SUBJECTS, COPYRIGHT
from .auth import do_logout, is_admin
from .utils import get_subject_stats, get_wrong_questions
from .page_dashboard import start_quiz


def render(questions, progress):
    with st.sidebar:
        st.markdown("## 📚 社労士 Study")
        st.caption("SR EXAM TRAINER")
        st.divider()

        email = st.session_state.get("auth_email", "")
        role  = st.session_state.get("auth_role", "user")
        badge = (
            '<span class="role-badge-admin">ADMIN</span>'
            if role == "admin" else
            '<span class="role-badge-user">USER</span>'
        )
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:8px;padding:10px 14px;margin-bottom:12px;">
            <div style="margin-bottom:4px;">{badge}</div>
            <div style="font-size:12px;color:#c0c0d8;word-break:break-all;">{email}</div>
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
        wrong_label = f"間違えた問題　`{wrong_count}`" if wrong_count > 0 else "間違えた問題"
        if st.button(f"⚠️  {wrong_label}", use_container_width=True):
            st.session_state.page = "wrong"
            st.rerun()

        if st.button("👤  アカウント設定", use_container_width=True):
            st.session_state.page = "account"
            st.rerun()

        # admin 専用メニュー
        if is_admin():
            st.divider()
            st.caption("管理メニュー")
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
        if st.button("プライバシーポリシー", use_container_width=True, key="sidebar_privacy"):
            st.session_state.page = "privacy"
            st.rerun()
        st.caption(f"☁️ Supabase  |  {COPYRIGHT}")
