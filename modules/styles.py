"""
styles.py - カスタムCSS一元管理
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
.stApp { background-color: #0e0e16; }
section[data-testid="stSidebar"] { background-color: #12121c !important; border-right: 1px solid rgba(255,255,255,0.07); }
section[data-testid="stSidebar"] * { color: #c8c8d8 !important; }
[data-testid="metric-container"] { background: #1a1a28; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px !important; }
[data-testid="metric-container"] label { color: #7070a0 !important; font-size: 11px !important; letter-spacing: 1px; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e0e0f0 !important; font-family: 'DM Mono', monospace !important; }
.stButton > button { background: #7c6af5 !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 500 !important; padding: 10px 24px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #9580ff !important; transform: translateY(-1px) !important; }
.question-card { background: #16162a; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px 32px; margin-bottom: 20px; }
.question-number { font-family: 'DM Mono', monospace; font-size: 11px; color: #6060a0; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; }
.question-text { font-size: 17px; line-height: 1.9; color: #e8e8f8; font-weight: 400; }
.correct-box { background: rgba(46,204,113,0.1); border: 1px solid rgba(46,204,113,0.4); border-radius: 10px; padding: 16px 20px; color: #2ecc71; font-weight: 500; margin: 12px 0; }
.wrong-box { background: rgba(231,76,60,0.1); border: 1px solid rgba(231,76,60,0.4); border-radius: 10px; padding: 16px 20px; color: #e74c3c; font-weight: 500; margin: 12px 0; }
.explanation-box { background: #1a1a2e; border: 1px solid rgba(255,255,255,0.06); border-left: 3px solid #7c6af5; border-radius: 0 10px 10px 0; padding: 18px 20px; color: #a0a0c8; font-size: 14px; line-height: 1.9; margin-top: 14px; }
.explanation-label { font-family: 'DM Mono', monospace; font-size: 10px; color: #7c6af5; letter-spacing: 2px; margin-bottom: 8px; }
.progress-outer { background: #1e1e30; border-radius: 4px; height: 6px; margin: 6px 0 10px; overflow: hidden; }
.progress-inner { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #7c6af5, #a594ff); transition: width 0.4s ease; }
.progress-inner-green { background: linear-gradient(90deg, #27ae60, #2ecc71); }
.subject-card { background: #16162a; border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 20px; margin-bottom: 10px; cursor: pointer; transition: border-color 0.2s; }
.subject-card:hover { border-color: #7c6af5; }
.subject-tag { display: inline-block; background: rgba(124,106,245,0.15); color: #a594ff; font-size: 10px; font-family: 'DM Mono', monospace; padding: 3px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 10px; }
.wrong-tag { display: inline-block; background: rgba(231,76,60,0.1); color: #e74c3c; font-size: 10px; font-family: 'DM Mono', monospace; padding: 3px 10px; border-radius: 20px; margin-left: 8px; }
.stRadio > div { gap: 8px !important; }
.stRadio > div > label { background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; padding: 14px 18px !important; width: 100% !important; color: #c8c8e8 !important; transition: all 0.15s !important; font-size: 14px !important; line-height: 1.6 !important; }
.stRadio > div > label:hover { border-color: #7c6af5 !important; background: rgba(124,106,245,0.08) !important; }
.option-card { background: #1a1a2e; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px 18px; margin: 5px 0; font-size: 14px; color: #c8c8e8; line-height: 1.6; display: flex; align-items: flex-start; gap: 12px; }
.option-card:hover { border-color: #7c6af5; background: rgba(124,106,245,0.06); }
.option-card-selected { background: rgba(124,106,245,0.12); border: 1.5px solid #7c6af5; border-radius: 12px; padding: 14px 18px; margin: 5px 0; font-size: 14px; color: #c8c8e8; line-height: 1.6; display: flex; align-items: flex-start; gap: 12px; }
.option-card-correct { background: rgba(46,204,113,0.08); border: 1.5px solid #2ecc71; border-radius: 12px; padding: 14px 18px; margin: 5px 0; font-size: 14px; color: #2ecc71; line-height: 1.6; display: flex; align-items: flex-start; gap: 12px; }
.option-card-wrong { background: rgba(231,76,60,0.08); border: 1.5px solid #e74c3c; border-radius: 12px; padding: 14px 18px; margin: 5px 0; font-size: 14px; color: #e74c3c; line-height: 1.6; display: flex; align-items: flex-start; gap: 12px; }
.option-label { display: inline-flex; align-items: center; justify-content: center; min-width: 28px; height: 28px; background: rgba(255,255,255,0.07); border-radius: 6px; font-size: 13px; font-weight: 600; flex-shrink: 0; margin-top: 1px; }
.option-label-correct { display: inline-flex; align-items: center; justify-content: center; min-width: 28px; height: 28px; background: rgba(46,204,113,0.2); color: #2ecc71; border-radius: 6px; font-size: 13px; font-weight: 600; flex-shrink: 0; margin-top: 1px; }
.option-label-wrong { display: inline-flex; align-items: center; justify-content: center; min-width: 28px; height: 28px; background: rgba(231,76,60,0.2); color: #e74c3c; border-radius: 6px; font-size: 13px; font-weight: 600; flex-shrink: 0; margin-top: 1px; }
.result-correct { background: rgba(46,204,113,0.12); border: 1.5px solid #2ecc71; border-radius: 12px; padding: 16px; text-align: center; color: #2ecc71; font-size: 17px; font-weight: 700; margin: 14px 0; }
.result-wrong { background: rgba(231,76,60,0.12); border: 1.5px solid #e74c3c; border-radius: 12px; padding: 16px; text-align: center; color: #e74c3c; font-size: 17px; font-weight: 700; margin: 14px 0; }
.quiz-meta-row { display: flex; align-items: center; justify-content: space-between; margin: 10px 0 6px; }
.quiz-meta-num { font-size: 14px; color: #9090b8; font-family: 'Noto Sans JP', sans-serif; }
.subject-pill { display: inline-block; background: rgba(46,204,113,0.15); color: #2ecc71; border: 1px solid rgba(46,204,113,0.3); font-size: 12px; padding: 4px 12px; border-radius: 20px; font-weight: 500; }
.confirm-btn-wrap { margin: 12px 0; }
div[data-testid="stButton"].option-btn > button { background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.08) !important; color: #c8c8e8 !important; text-align: left !important; justify-content: flex-start !important; border-radius: 12px !important; padding: 14px 18px !important; font-size: 14px !important; line-height: 1.6 !important; }
div[data-testid="stButton"].option-btn > button:hover { border-color: #7c6af5 !important; background: rgba(124,106,245,0.08) !important; }
h1 { color: #e8e8f8 !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2, h3 { color: #d0d0e8 !important; font-weight: 500 !important; }
p, li { color: #9090b8 !important; }
hr { border-color: rgba(255,255,255,0.07) !important; }
.log-box { background: #0e0e16; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 14px; font-family: 'DM Mono', monospace; font-size: 12px; color: #7070a0; max-height: 300px; overflow-y: auto; }
.ad-section-label { font-size: 10px; color: #5050a0; font-family: 'DM Mono', monospace; letter-spacing: 2px; margin-bottom: 10px; text-align: right; }
.ad-card { display: flex; align-items: center; gap: 16px; background: linear-gradient(135deg, #16162a 0%, #1a1828 100%); border: 1px solid rgba(245,197,66,0.25); border-radius: 14px; padding: 16px 20px; margin-bottom: 10px; text-decoration: none; transition: border-color 0.2s, transform 0.15s; }
.ad-card:hover { border-color: rgba(245,197,66,0.6); transform: translateY(-2px); }
.ad-card-img { width: 72px; height: 72px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }
.ad-card-img-placeholder { width: 72px; height: 72px; border-radius: 8px; flex-shrink: 0; background: rgba(124,106,245,0.15); display: flex; align-items: center; justify-content: center; font-size: 28px; }
.ad-card-body { flex: 1; min-width: 0; }
.ad-card-title { font-size: 14px; font-weight: 600; color: #e8e8f0; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ad-card-desc { font-size: 12px; color: #8080a8; line-height: 1.6; }
.ad-card-badge { font-size: 10px; font-family: 'DM Mono', monospace; background: rgba(245,197,66,0.15); color: #f5c542; padding: 2px 8px; border-radius: 4px; flex-shrink: 0; }
.footer { text-align: center; padding: 32px 0 16px; color: #3a3a5a; font-size: 11px; font-family: 'DM Mono', monospace; }
.footer a { color: #5050a0; text-decoration: none; }
.footer a:hover { color: #a594ff; }
.role-badge-admin { display:inline-block; background:rgba(124,106,245,0.2); color:#a594ff; font-size:10px; font-family:'DM Mono',monospace; padding:2px 8px; border-radius:4px; letter-spacing:1px; }
.role-badge-user { display:inline-block; background:rgba(46,204,113,0.15); color:#2ecc71; font-size:10px; font-family:'DM Mono',monospace; padding:2px 8px; border-radius:4px; letter-spacing:1px; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
