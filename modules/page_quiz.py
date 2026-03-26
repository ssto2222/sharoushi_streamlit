"""
page_quiz.py - 問題出題・解答・結果ページ
"""
import streamlit as st
import streamlit.components.v1 as components
from .constants import SUBJECT_MAP
from .db import (
    load_progress, save_progress_item,
    save_session_item, clear_session,
)
from .utils import render_footer


def render_quiz(questions, progress):
    # 次の問題へ進んだ直後のみ先頭にスクロール
    if st.session_state.pop("scroll_to_top", False):
        components.html(
            "<script>window.parent.document.querySelector('section.main').scrollTo(0,0);</script>",
            height=0,
        )

    qs    = st.session_state.quiz_questions
    total = len(qs)

    # 続きから再開の確認
    if st.session_state.get("quiz_saved_session") and not st.session_state.get("session_confirmed"):
        saved = st.session_state.quiz_saved_session
        st.info(f"前回の続きがあります（{saved['index']}/{saved['total']}問）。再開しますか？")
        col_a, col_b = st.columns(2)
        if col_a.button("▶ 続きから再開"):
            st.session_state.quiz_index        = saved["index"]
            st.session_state.quiz_score        = saved["score"]
            st.session_state.session_confirmed = True
            st.rerun()
        if col_b.button("最初からやり直す"):
            clear_session(st.session_state.quiz_session_key)
            st.session_state.session_confirmed = True
            st.rerun()
        st.stop()

    if not st.session_state.get("session_confirmed"):
        st.session_state.session_confirmed = True

    idx       = st.session_state.quiz_index
    subj_info = SUBJECT_MAP.get(st.session_state.quiz_subject, {"name": "全科目", "short": "--"})

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
    labels = ["A", "B", "C", "D", "E"]

    is_fill_blank = "___" in q["question"]

    _blank_html = (
        '<span style="display:inline-block;min-width:80px;border-bottom:2px solid #a594ff;'
        'color:#a594ff;font-weight:700;text-align:center;padding:0 6px;margin:0 2px;">'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
    )
    display_q = q["question"].replace("___", _blank_html) if is_fill_blank else q["question"]

    q_type_label = "穴埋め" if is_fill_blank else "選択"
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">
            Q {str(idx + 1).zfill(2)} -- {q_subj['name']}
            <span style="font-size:10px;background:rgba(165,148,255,0.15);color:#a594ff;
                border-radius:4px;padding:2px 7px;margin-left:8px;font-family:'DM Mono',monospace;">
                {q_type_label}
            </span>
        </div>
        <div class="question-text">{display_q}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered:
        choice = st.radio(
            "選択してください",
            options=list(range(len(q["options"]))),
            format_func=lambda i: f"{labels[i]}  {q['options'][i]}",
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
            st.session_state.just_answered   = True
            st.rerun()

    else:
        selected   = st.session_state.selected_option
        is_correct = (selected == q["answer"])

        # 穴埋め問題は問題文に選んだ答えを埋めて再表示
        if is_fill_blank:
            fill_color = "#2ecc71" if is_correct else "#e74c3c"
            filled_html = (
                f'<span style="display:inline-block;min-width:80px;border-bottom:2px solid {fill_color};'
                f'color:{fill_color};font-weight:700;text-align:center;padding:0 6px;margin:0 2px;">'
                f'{q["options"][selected]}</span>'
            )
            answered_q = q["question"].replace("___", filled_html)
            st.markdown(f"""
            <div style="background:#1a1a2e;border:1px solid rgba(255,255,255,0.08);
                border-radius:10px;padding:14px 18px;margin:8px 0;font-size:14px;color:#c0c0e0;line-height:1.8;">
                {answered_q}
            </div>
            """, unsafe_allow_html=True)

        for i, opt in enumerate(q["options"]):
            if i == q["answer"]:
                icon = "OK"
            elif i == selected and not is_correct:
                icon = "NG"
            else:
                icon = "  "
            st.markdown(f"""
            <div style="background:#1a1a2e;border:1px solid rgba(255,255,255,0.08);
                border-radius:10px;padding:12px 18px;margin:6px 0;font-size:14px;color:#c0c0e0;">
                {icon} {labels[i]}  {opt}
            </div>
            """, unsafe_allow_html=True)

        if is_correct:
            st.markdown('<div class="correct-box">正解！</div>', unsafe_allow_html=True)
        else:
            correct_text = q["options"][q["answer"]]
            st.markdown(f'<div class="wrong-box">不正解  正解：{labels[q["answer"]]}  {correct_text}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="explanation-box">
            <div class="explanation-label">EXPLANATION</div>
            {q['explanation']}
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        next_label    = "次の問題 →" if idx + 1 < total else "結果を見る"
        just_answered = st.session_state.get("just_answered", False)
        if just_answered:
            st.session_state.just_answered = False
        if st.button(next_label, key=f"next_{idx}", disabled=just_answered):
            if idx + 1 >= total:
                clear_session(st.session_state.quiz_session_key)
                st.session_state.page = "result"
            else:
                st.session_state.quiz_index     += 1
                st.session_state.answered        = False
                st.session_state.selected_option = None
                st.session_state.scroll_to_top   = True
            st.rerun()


def render_result(questions, progress):
    from .page_dashboard import start_quiz
    from .utils import get_wrong_questions

    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    pct   = round(score / total * 100) if total > 0 else 0
    icon  = "🎯" if pct >= 70 else "📚" if pct >= 50 else "💪"

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

    render_footer()


def render_wrong_review(questions, progress):
    from .page_dashboard import start_quiz
    from .utils import get_wrong_questions, render_ads
    from .db import cache_invalidate

    wrong_qs = get_wrong_questions(questions, progress)
    st.markdown("# 間違えた問題")
    st.caption(f"要復習の問題が **{len(wrong_qs)}** 件あります")
    st.write("")

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
        from .constants import SUBJECT_MAP as SM
        for q in wrong_qs:
            s  = SM.get(q["subject"], {"short": "--"})
            wc = progress.get(q["id"], {}).get("wrong_count", 0)
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
                    <span style="flex:1;font-size:13px;color:#a0a0c8;">{q['question'][:60]}...</span>
                    <span style="font-size:11px;font-family:'DM Mono',monospace;color:#e74c3c;">x{wc}</span>
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

    render_footer()
