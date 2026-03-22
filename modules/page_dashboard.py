"""
page_dashboard.py - ホーム（学習ダッシュボード）
"""
import streamlit as st
from .constants import SUBJECTS
from .utils import get_subject_stats, render_footer
from .db import load_sessions


def start_quiz(subject_id, mode, questions, progress):
    from .utils import get_wrong_questions
    from .db import load_sessions

    if mode == "wrong":
        qs = get_wrong_questions(questions, progress, subject_id if subject_id != "all" else None)
    elif subject_id == "all":
        qs = questions[:]
    else:
        qs = [q for q in questions if q["subject"] == subject_id]

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


def render(questions, progress):
    st.markdown("# 学習ダッシュボード")
    st.caption("今日も合格に向けて一歩ずつ")
    st.write("")

    from .utils import get_wrong_questions
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
        topics    = SUBJECT_TOPICS.get(s["id"], [])

        with cols[i % 3]:
            wrong_badge = f'<span class="wrong-tag">要復習 {stats["wrong"]}</span>' if stats["wrong"] > 0 else ""
            st.markdown(f"""
            <div class="subject-card">
                <div><span class="subject-tag">{s['short']}</span>{wrong_badge}</div>
                <div style="font-size:15px;font-weight:500;color:#e0e0f0;margin:8px 0 12px;">{s['name']}</div>
                <div class="progress-outer"><div class="progress-inner {bar_color}" style="width:{pct}%"></div></div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#7070a0;">
                    <span>正解 {stats['correct']}</span>
                    <span>要復習 {stats['wrong']}</span>
                    <span style="color:#a594ff;font-family:'DM Mono',monospace;">{stats['rate']}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 出題範囲の内訳（expander でポップアップ風に表示）
            if topics:
                with st.expander(f"📋 出題範囲（{len(topics)}分野）を見る"):
                    rows_html = ""
                    for title, detail in topics:
                        rows_html += f"""
                        <div style="display:flex;gap:10px;padding:7px 0;
                            border-bottom:1px solid rgba(255,255,255,0.05);align-items:flex-start;">
                            <span style="min-width:8px;margin-top:6px;width:8px;height:8px;
                                border-radius:50%;background:#7c6af5;flex-shrink:0;display:inline-block;"></span>
                            <div>
                                <div style="font-size:13px;color:#d0d0f0;font-weight:500;">{title}</div>
                                <div style="font-size:11px;color:#6060a0;margin-top:2px;line-height:1.5;">{detail}</div>
                            </div>
                        </div>"""
                    st.markdown(f'<div style="padding:4px 0;">{rows_html}</div>', unsafe_allow_html=True)

            if st.button(f"▶ {s['short']} を始める", key=f"start_{s['id']}", use_container_width=True):
                start_quiz(s["id"], "all", questions, progress)
                st.rerun()



    render_footer()
