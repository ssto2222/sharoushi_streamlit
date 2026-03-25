"""
page_admin.py - admin専用ページ
- 問題生成・追加
- 広告管理
"""
import json
import streamlit as st
from .constants import SUBJECTS, SUBJECT_MAP, MODEL_NAME
from .db import (
    load_questions, save_questions,
    delete_questions_by_subject, delete_all_questions,
    load_ads, save_ad, delete_ad,
)
from .utils import render_ads, render_footer


# ── 問題生成・追加

def render_generate():
    st.markdown("# 問題を生成・追加")
    st.write("")

    with st.expander("🔑 Anthropic API キー設定", expanded=not bool(st.session_state.api_key)):
        api_key = st.text_input("API キー", value=st.session_state.api_key, type="password", placeholder="sk-ant-...")
        if st.button("保存"):
            st.session_state.api_key = api_key
            st.success("保存しました！")

    st.divider()
    st.markdown("### AI で問題を自動生成")
    st.caption(f"科目を選択して「生成開始」を押すと、各科目10問を自動生成します。（モデル: `{MODEL_NAME}`）")

    selected = st.multiselect(
        "生成する科目を選択",
        options=[s["id"] for s in SUBJECTS],
        format_func=lambda x: f"{SUBJECT_MAP[x]['short']} - {SUBJECT_MAP[x]['name']}",
        default=[],
    )

    if st.button("🚀 選択科目を生成開始", disabled=not (selected and st.session_state.api_key)):
        try:
            import anthropic
        except ImportError:
            st.error("anthropic パッケージがインストールされていません。")
            st.stop()

        log_area = st.empty()
        logs     = []

        def log(msg, ok=True):
            logs.append(("OK " if ok else "NG ") + msg)
            log_area.markdown(
                '<div class="log-box">' + "<br>".join(logs[-30:]) + "</div>",
                unsafe_allow_html=True,
            )

        try:
            client = anthropic.Anthropic(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"APIクライアントの初期化に失敗: {repr(e)}")
            st.stop()

        qs = load_questions()
        for sid in selected:
            subj      = SUBJECT_MAP[sid]
            existing  = [q for q in qs if q["subject"] == sid]
            start_idx = len(existing) + 1
            log(f"{subj['name']} の問題を生成中...")

            prompt = (
                f"社会保険労務士試験の「{subj['name']}」に関する5択問題を10問作成してください。\n"
                f"必ずJSON配列のみ返してください（前後の説明文・```マークは不要）。\n"
                f'[{{"id":"{sid}_{str(start_idx).zfill(3)}","subject":"{sid}",'
                f'"question":"問題文","options":["A","B","C","D","E"],'
                f'"answer":0,"explanation":"解説文"}}]\n\n'
                f"ルール: answer=0〜4の整数 / 法令条文に基づく内容 / 本試験レベル / "
                f"ID={sid}_{str(start_idx).zfill(3)}〜{sid}_{str(start_idx+9).zfill(3)} / 10問ちょうど"
            )

            try:
                msg      = client.messages.create(model=MODEL_NAME, max_tokens=4096, messages=[{"role": "user", "content": prompt}])
                raw_text = msg.content[0].text.strip()

                if "```" in raw_text:
                    for part in raw_text.split("```"):
                        part = part.strip()
                        if part.startswith("json"):
                            part = part[4:].strip()
                        if part.startswith("["):
                            raw_text = part
                            break

                s_i = raw_text.find("[")
                e_i = raw_text.rfind("]")
                if s_i == -1 or e_i == -1:
                    raise ValueError(f"JSON [ ] が見つかりません: {raw_text[:200]}")
                raw_text = raw_text[s_i:e_i + 1]

                new_qs       = json.loads(raw_text)
                existing_ids = {q["id"] for q in qs}
                valid_added  = []
                for q in new_qs:
                    if q["id"] in existing_ids:
                        continue
                    required = {"id", "subject", "question", "options", "answer", "explanation"}
                    if not required.issubset(q.keys()):
                        log(f"  {q.get('id','?')} フィールド不足 (スキップ)", ok=False)
                        continue
                    if not isinstance(q["options"], list) or len(q["options"]) != 5:
                        log(f"  {q.get('id','?')} 選択肢が5個でない (スキップ)", ok=False)
                        continue
                    if not isinstance(q["answer"], int) or not (0 <= q["answer"] <= 4):
                        log(f"  {q.get('id','?')} answer が不正 (スキップ)", ok=False)
                        continue
                    valid_added.append(q)

                if valid_added:
                    save_questions(valid_added)
                    qs.extend(valid_added)
                log(f"{subj['name']}: {len(valid_added)}問追加（合計 {len([q for q in qs if q['subject']==sid])}問）")

            except json.JSONDecodeError as e:
                log(f"{subj['name']}: JSONパースエラー - {repr(e)}", ok=False)
            except Exception as e:
                log(f"{subj['name']}: エラー - {repr(e)}", ok=False)

        log("完了！")
        st.success("問題の生成が完了しました！")

    st.divider()
    st.markdown("### JSON で問題を追加")
    st.caption("**穴埋め問題**は `question` フィールドに `___` を含めることで自動判定されます。")
    sample_json = json.dumps([
        {
            "id": "roki_custom_001", "subject": "roki",
            "question": "問題文（通常の選択問題）",
            "options": ["選択肢A", "選択肢B", "選択肢C", "選択肢D", "選択肢E"],
            "answer": 0, "explanation": "解説文",
        },
        {
            "id": "roki_custom_002", "subject": "roki",
            "question": "穴埋め問題の例：労働時間が___時間を超える場合は1時間以上の休憩が必要である。",
            "options": ["8", "6", "10", "7", "9"],
            "answer": 0, "explanation": "___に入る語句を選ぶ穴埋め形式です。",
        },
    ], ensure_ascii=False, indent=2)

    with st.expander("📋 JSON フォーマットを確認", expanded=False):
        st.markdown("以下のフォーマットに従って JSON を作成してください。")
        st.code(sample_json, language="json")
        st.caption("subject は次のいずれか: " + "、".join(f"`{s['id']}`" for s in SUBJECTS))
        st.caption("answer は 0〜4 の整数（0 = 選択肢A、4 = 選択肢E）")

    overwrite_mode = st.checkbox("既存IDの問題を上書きする（同じIDがあれば置き換え）", value=False)

    def _validate_and_import_questions(new_qs, overwrite=False):
        if not isinstance(new_qs, list):
            st.error("JSON はオブジェクトの配列（ `[{...}, ...]` ）である必要があります。")
            return
        qs           = load_questions()
        existing_ids = {q["id"] for q in qs}
        valid_qs     = []
        errors       = []
        skipped_dup  = 0
        overwritten  = 0
        valid_subject_ids = {s["id"] for s in SUBJECTS}

        for q in new_qs:
            qid = q.get("id", "?")
            required = {"id", "subject", "question", "options", "answer", "explanation"}
            if not required.issubset(q.keys()):
                missing = required - q.keys()
                errors.append(f"`{qid}`: 必須フィールド不足 — {', '.join(missing)}")
                continue
            if q["subject"] not in valid_subject_ids:
                errors.append(f"`{qid}`: 無効な subject `{q['subject']}`")
                continue
            if not isinstance(q["options"], list) or len(q["options"]) != 5:
                errors.append(f"`{qid}`: options は5個のリストである必要があります")
                continue
            if not isinstance(q["answer"], int) or not (0 <= q["answer"] <= 4):
                errors.append(f"`{qid}`: answer は 0〜4 の整数である必要があります（現在: `{q['answer']}`）")
                continue
            if qid in existing_ids:
                if overwrite:
                    overwritten += 1
                    valid_qs.append(q)
                else:
                    skipped_dup += 1
            else:
                valid_qs.append(q)

        new_only = len(valid_qs) - overwritten
        if valid_qs:
            save_questions(valid_qs)
            msg = []
            if new_only:
                msg.append(f"{new_only} 問を新規追加")
            if overwritten:
                msg.append(f"{overwritten} 問を上書き")
            st.success(f"✅ {'、'.join(msg)}しました！")
        if skipped_dup:
            st.info(f"⏭️ {skipped_dup} 問は既存IDと重複しているためスキップしました。")
        if errors:
            with st.expander(f"⚠️ {len(errors)} 件のエラー（スキップ）", expanded=True):
                for e in errors:
                    st.markdown(f"- {e}")
        if valid_qs:
            st.rerun()

    tab_file, tab_text = st.tabs(["📁 ファイルアップロード", "📝 テキスト貼り付け"])

    with tab_file:
        uploaded_file = st.file_uploader("JSON ファイルをアップロード", type=["json"], label_visibility="collapsed")
        if uploaded_file is not None:
            st.caption(f"ファイル名: `{uploaded_file.name}`　サイズ: {uploaded_file.size:,} bytes")
            if st.button("📥 ファイルからインポート", use_container_width=True):
                try:
                    raw = uploaded_file.read().decode("utf-8")
                    new_qs = json.loads(raw)
                    _validate_and_import_questions(new_qs, overwrite=overwrite_mode)
                except json.JSONDecodeError as e:
                    st.error(f"JSON のパースに失敗しました: {e}")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

    with tab_text:
        json_input = st.text_area("JSON を貼り付け", placeholder=sample_json, height=200, label_visibility="collapsed")
        if st.button("📥 テキストからインポート", use_container_width=True):
            if not json_input.strip():
                st.warning("JSON を入力してください。")
            else:
                try:
                    new_qs = json.loads(json_input)
                    _validate_and_import_questions(new_qs, overwrite=overwrite_mode)
                except json.JSONDecodeError as e:
                    st.error(f"JSON のパースに失敗しました: {e}")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

    st.divider()
    st.markdown("### 問題を削除")
    st.caption("削除した問題は元に戻せません。操作前にデータをエクスポートすることをお勧めします。")

    del_tab_subj, del_tab_all = st.tabs(["📚 科目ごとに削除", "🗑️ 全問題を削除"])

    with del_tab_subj:
        del_subject = st.selectbox(
            "削除する科目",
            options=[s["id"] for s in SUBJECTS],
            format_func=lambda x: f"{SUBJECT_MAP[x]['short']} - {SUBJECT_MAP[x]['name']}",
            key="del_subject_select",
        )
        qs_preview = load_questions()
        del_count = len([q for q in qs_preview if q["subject"] == del_subject])
        st.caption(f"現在 {del_count} 問登録されています。")

        if st.session_state.get("confirm_del_subj") == del_subject:
            st.warning(f"⚠️ 本当に **{SUBJECT_MAP[del_subject]['name']}** の {del_count} 問を削除しますか？")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("はい、削除する", type="primary", use_container_width=True):
                    n = delete_questions_by_subject(del_subject)
                    st.session_state.pop("confirm_del_subj", None)
                    st.success(f"🗑️ {SUBJECT_MAP[del_subject]['name']} の {n} 問を削除しました。")
                    st.rerun()
            with col_no:
                if st.button("キャンセル", use_container_width=True):
                    st.session_state.pop("confirm_del_subj", None)
                    st.rerun()
        else:
            if st.button(f"🗑️ {SUBJECT_MAP[del_subject]['name']} の問題を削除", disabled=del_count == 0):
                st.session_state["confirm_del_subj"] = del_subject
                st.rerun()

    with del_tab_all:
        all_count = len(load_questions())
        st.caption(f"現在 全科目合計 {all_count} 問登録されています。")

        if st.session_state.get("confirm_del_all"):
            st.warning(f"⚠️ 本当に **全 {all_count} 問**を削除しますか？この操作は取り消せません。")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("はい、全て削除する", type="primary", use_container_width=True, key="del_all_yes"):
                    n = delete_all_questions()
                    st.session_state.pop("confirm_del_all", None)
                    st.success(f"🗑️ 全 {n} 問を削除しました。")
                    st.rerun()
            with col_no:
                if st.button("キャンセル", use_container_width=True, key="del_all_no"):
                    st.session_state.pop("confirm_del_all", None)
                    st.rerun()
        else:
            if st.button("🗑️ 全問題を削除", disabled=all_count == 0):
                st.session_state["confirm_del_all"] = True
                st.rerun()

    st.divider()
    st.markdown("### 現在の問題数")
    qs   = load_questions()
    cols = st.columns(3)
    for i, s in enumerate(SUBJECTS):
        count = len([q for q in qs if q["subject"] == s["id"]])
        cols[i % 3].markdown(f"""
        <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
            border-radius:10px;padding:14px;margin:4px 0;">
            <div style="font-size:11px;color:#6060a0;font-family:'DM Mono',monospace;">{s['short']}</div>
            <div style="font-size:20px;font-weight:700;color:#a594ff;font-family:'DM Mono',monospace;">
                {count}<span style="font-size:12px;color:#5050a0;">問</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_footer()


# ── 広告管理

def render_ads_management():
    st.markdown("# 広告管理")
    st.caption("弱点復習ページに表示するおすすめ教材を管理します")
    st.write("")

    ads = load_ads(active_only=False)

    if ads:
        st.markdown("### 現在の広告")
        for ad in ads:
            status_color = "#2ecc71" if ad.get("is_active") else "#7070a0"
            status_label = "公開中" if ad.get("is_active") else "非公開"
            col_info, col_actions = st.columns([5, 2])
            with col_info:
                img_tag = (
                    f'<img src="{ad["image_url"]}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;margin-right:12px;vertical-align:middle;">'
                    if ad.get("image_url") else ""
                )
                st.markdown(f"""
                <div style="background:#16162a;border:1px solid rgba(255,255,255,0.07);
                    border-radius:10px;padding:14px 18px;display:flex;align-items:center;">
                    {img_tag}
                    <div style="flex:1;">
                        <div style="font-size:13px;font-weight:600;color:#e0e0f0;">{ad.get("title","")}</div>
                        <div style="font-size:11px;color:#6060a0;margin-top:2px;">
                            表示順: {ad.get("sort_order",0)}　|　
                            <span style="color:{status_color};">● {status_label}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_actions:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("編集", key=f"edit_{ad['id']}"):
                        st.session_state.ad_edit_id = ad["id"]
                        st.rerun()
                with c2:
                    if st.button("削除", key=f"del_{ad['id']}"):
                        if delete_ad(ad["id"]):
                            st.success("削除しました")
                            st.rerun()
        st.divider()
    else:
        st.info("広告はまだありません。下のフォームから追加してください。")
        st.write("")

    edit_id   = st.session_state.get("ad_edit_id")
    edit_ad   = next((a for a in ads if a["id"] == edit_id), {}) if edit_id else {}
    st.markdown("### 広告を編集" if edit_id else "### 広告を追加")

    with st.form("ad_form", clear_on_submit=True):
        title       = st.text_input("タイトル *", value=edit_ad.get("title", ""), placeholder="例: ユーキャン 社労士 通信講座")
        description = st.text_area("説明文", value=edit_ad.get("description", ""), height=80)
        link_url    = st.text_input("リンクURL *", value=edit_ad.get("link_url", ""), placeholder="https://example.com/affiliate?id=xxx")
        image_url   = st.text_input("画像URL（空欄の場合は絵文字）", value=edit_ad.get("image_url", ""))
        col_e, col_o, col_a = st.columns([2, 2, 2])
        with col_e:
            emoji = st.text_input("絵文字", value=edit_ad.get("emoji", "📖"), max_chars=2)
        with col_o:
            sort_order = st.number_input("表示順", value=int(edit_ad.get("sort_order", len(ads) + 1)), min_value=1, max_value=999)
        with col_a:
            st.write("")
            is_active = st.checkbox("公開する", value=edit_ad.get("is_active", True))

        col_s, col_c = st.columns([3, 1])
        with col_s:
            submitted = st.form_submit_button("保存" if edit_id else "追加", use_container_width=True)
        with col_c:
            cancelled = st.form_submit_button("キャンセル", use_container_width=True)

        if submitted:
            if not title or not link_url:
                st.error("タイトルとリンクURLは必須です。")
            else:
                ad_data = {
                    "title": title, "description": description,
                    "link_url": link_url, "image_url": image_url,
                    "emoji": emoji or "📖", "sort_order": sort_order,
                    "is_active": is_active,
                }
                if edit_id:
                    ad_data["id"] = edit_id
                if save_ad(ad_data):
                    st.success("保存しました！")
                    st.session_state.ad_edit_id = None
                    st.rerun()

        if cancelled:
            st.session_state.ad_edit_id = None
            st.rerun()

    if ads:
        st.divider()
        st.markdown("### プレビュー")
        render_ads()

    render_footer()
