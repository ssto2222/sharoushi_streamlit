"""
page_quiz.py - 問題出題・解答・結果ページ
"""
import html as _html
import streamlit as st
import streamlit.components.v1 as components
from .constants import SUBJECT_MAP
from .db import (
    load_progress, save_progress_item,
    save_session_item, clear_session,
)
from .utils import render_footer


def render_quiz(questions, progress):
    # 次の問題へ進んだ直後のみ先頭までスクロール
    if st.session_state.pop("scroll_to_top", False):
        components.html(
            "<script>"
            "(function(){"
            "var attempts=0;"
            "function tryScroll(){"
            "try{"
            "var el=window.parent.document.getElementById('quiz-content-top');"
            "if(el){el.scrollIntoView({behavior:'smooth',block:'start'});return;}"
            "}catch(e){return;}"
            "if(++attempts<20)setTimeout(tryScroll,100);"
            "}"
            "setTimeout(tryScroll,100);"
            "})();"
            "</script>",
            height=1,
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

    # 戻るボタン
    if st.button("← 戻る", key="back_btn"):
        save_session_item(st.session_state.quiz_session_key, idx, total, st.session_state.quiz_score)
        st.session_state.page              = "home"
        st.session_state.session_confirmed = False
        st.rerun()

    st.markdown('<div id="quiz-content-top"></div>', unsafe_allow_html=True)

    q      = qs[idx]
    q_subj = SUBJECT_MAP.get(q["subject"], {"name": ""})
    labels_ja = ["ア", "イ", "ウ", "エ", "オ"]

    # 問題番号 + 科目バッジ + プログレスバー
    bar_pct = round((idx + 1) / total * 100)
    st.markdown(f"""
    <div class="quiz-meta-row">
        <span class="quiz-meta-num">問題 {idx + 1} / {total}</span>
        <span class="subject-pill">{q_subj['name']}</span>
    </div>
    <div class="progress-outer"><div class="progress-inner" style="width:{bar_pct}%"></div></div>
    """, unsafe_allow_html=True)
    st.write("")

    is_fill_blank = "___" in q["question"]

    _blank_html = (
        '<span style="display:inline-block;min-width:80px;border-bottom:2px solid #a594ff;'
        'color:#a594ff;font-weight:700;text-align:center;padding:0 6px;margin:0 2px;">'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
    )
    display_q = q["question"].replace("___", _blank_html) if is_fill_blank else q["question"]

    # 問題文カード
    st.markdown(f"""
    <div class="question-card">
        <div class="question-text">{display_q}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered:
        # temp_selection 初期化
        if f"temp_sel_{idx}" not in st.session_state:
            st.session_state[f"temp_sel_{idx}"] = None

        temp = st.session_state[f"temp_sel_{idx}"]

        # 選択肢ボタンのスタイル
        st.markdown("""<style>
/* 選択肢ボタン共通（テキスト折り返し・左揃え） */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: #1e1e38 !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
    border-left: none !important;
    border-radius: 0 12px 12px 0 !important;
    color: #e4e4f4 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 15px !important;
    padding: 13px 16px !important;
    line-height: 1.7 !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 52px !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: rgba(124,106,245,0.14) !important;
    border-color: rgba(124,106,245,0.7) !important;
    color: #e8e8f8 !important;
}
/* バッジ列とボタン列の隙間をゼロに */
div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    padding: 0 !important;
}
</style>""", unsafe_allow_html=True)

        for i, opt in enumerate(q["options"]):
            is_selected = (temp == i)
            escaped_opt = _html.escape(opt)
            if is_selected:
                # 選択済み → 紫枠カード（HTMLレンダリング）
                st.markdown(f"""
                <div style="background:rgba(124,106,245,0.12);border:1.5px solid #7c6af5;
                    border-radius:12px;padding:13px 18px;margin:5px 0;
                    display:flex;align-items:flex-start;gap:12px;
                    font-size:15px;color:#e4e4f4;line-height:1.7;">
                    <span style="background:rgba(124,106,245,0.35);color:#c8b8ff;
                        display:inline-flex;align-items:center;justify-content:center;
                        min-width:28px;height:28px;border-radius:6px;
                        font-size:13px;font-weight:700;flex-shrink:0;margin-top:2px;">{labels_ja[i]}</span>
                    <span style="flex:1;">{escaped_opt}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # 未選択 → バッジ(HTML) + ボタン(st.button) をcolumnsで横並び
                st.markdown('<div style="margin:2.5px 0;">', unsafe_allow_html=True)
                col_badge, col_btn = st.columns([0.08, 0.92])
                with col_badge:
                    st.markdown(f"""
                    <div style="background:#1e1e38;
                        border:1px solid rgba(255,255,255,0.22);border-right:none;
                        border-radius:12px 0 0 12px;min-height:52px;height:100%;
                        display:flex;align-items:flex-start;justify-content:center;
                        padding:15px 0 0 0;">
                        <span style="background:rgba(255,255,255,0.1);color:#d0d0e8;
                            display:inline-flex;align-items:center;justify-content:center;
                            width:28px;height:28px;border-radius:6px;
                            font-size:13px;font-weight:700;">{labels_ja[i]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.button(opt, key=f"opt_{idx}_{i}", use_container_width=True):
                        st.session_state[f"temp_sel_{idx}"] = i
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        # 解答を確認するボタン
        if temp is not None:
            if st.button("解答を確認する", key=f"answer_{idx}", use_container_width=True):
                choice     = temp
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
            st.markdown("""
            <div style="background:#1a1a2e;border:1px solid rgba(255,255,255,0.06);border-radius:12px;
                padding:14px;text-align:center;color:#4a4a6a;font-size:14px;margin-top:4px;cursor:default;">
                解答を確認する
            </div>
            """, unsafe_allow_html=True)

    else:
        selected      = st.session_state.selected_option
        is_correct    = (selected == q["answer"])
        just_answered = st.session_state.pop("just_answered", False)

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
                border-radius:12px;padding:14px 18px;margin:8px 0;font-size:14px;color:#c0c0e0;line-height:1.8;">
                {answered_q}
            </div>
            """, unsafe_allow_html=True)

        # 選択肢（回答後：色付きカード）
        for i, opt in enumerate(q["options"]):
            if i == q["answer"] and i == selected:
                # 正解を選んだ場合
                card_cls  = "option-card-correct"
                lbl_cls   = "option-label-correct"
                marker    = " ✓"
            elif i == q["answer"]:
                # 正解（選んでいない場合でも緑表示）
                card_cls  = "option-card-correct"
                lbl_cls   = "option-label-correct"
                marker    = " ✓"
            elif i == selected and not is_correct:
                # 誤答を選んだ
                card_cls  = "option-card-wrong"
                lbl_cls   = "option-label-wrong"
                marker    = " ✗"
            else:
                card_cls  = "option-card"
                lbl_cls   = "option-label"
                marker    = ""
            st.markdown(f"""
            <div class="{card_cls}">
                <span class="{lbl_cls}">{labels_ja[i]}</span>
                <span>{opt}{marker}</span>
            </div>
            """, unsafe_allow_html=True)

        # 結果バナー
        if is_correct:
            st.markdown('<div id="explanation-anchor" class="result-correct">✓ 正解</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div id="explanation-anchor" class="result-wrong">✗ 不正解</div>', unsafe_allow_html=True)

        # 解説
        st.markdown(f"""
        <div class="explanation-box">
            <div class="explanation-label">解説</div>
            {q['explanation']}
        </div>
        """, unsafe_allow_html=True)

        if just_answered:
            components.html(
                "<script>setTimeout(function(){"
                "try{"
                "var el=window.parent.document.getElementById('explanation-anchor');"
                "if(el)el.scrollIntoView({behavior:'smooth',block:'start'});"
                "}catch(e){}"
                "},400);</script>",
                height=1,
            )

        st.write("")
        next_label = "次の問題 →" if idx + 1 < total else "結果を見る"
        if st.button(next_label, key=f"next_{idx}", use_container_width=True):
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
