"""
utils.py - 共通ユーティリティ（統計・広告レンダリング・フッター等）
"""
import streamlit as st
from .constants import COPYRIGHT, APP_NAME
from .db import load_ads


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
    return {"total": total, "answered": answered, "correct": correct,
            "wrong": wrong, "rate": rate}


def get_wrong_questions(questions: list, progress: dict, subject_id: str = None) -> list:
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
    st.markdown('<div class="ad-section-label">PR・おすすめ教材</div>', unsafe_allow_html=True)
    for ad in ads:
        img_html = (
            f'<img src="{ad["image_url"]}" class="ad-card-img" onerror="this.style.display=\'none\'">'
            if ad.get("image_url") else
            f'<div class="ad-card-img-placeholder">{ad.get("emoji", "")}</div>'
        )
        st.markdown(f"""
        <a href="{ad.get("link_url", "#")}" target="_blank" class="ad-card" rel="noopener noreferrer">
            {img_html}
            <div class="ad-card-body">
                <div class="ad-card-title">{ad.get("title", "")}</div>
                <div class="ad-card-desc">{ad.get("description", "")}</div>
            </div>
            <div class="ad-card-badge">詳細 →</div>
        </a>
        """, unsafe_allow_html=True)
    st.write("")


def render_footer():
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("プライバシーポリシー", key="footer_privacy_btn", use_container_width=True):
            st.session_state["page"] = "privacy"
            st.rerun()
    st.markdown(f'<div style="text-align:center;padding:4px 0 16px;color:#3a3a5a;font-size:11px;">{COPYRIGHT}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def init_state():
    """session_state の初期値をセット。"""
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
        "auth_role":        None,
        "auth_email":       None,
        "ad_edit_id":       None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
