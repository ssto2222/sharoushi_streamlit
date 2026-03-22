from datetime import datetime

APP_NAME     = "社労士 Study"
CURRENT_YEAR = datetime.now().year
COPYRIGHT    = f"© {CURRENT_YEAR} {APP_NAME}. All rights reserved."
MODEL_NAME   = "claude-haiku-4-5-20251001"
SESSION_EXPIRE_SEC = 60 * 60 * 24  # 24時間

SUBJECTS = [
    {"id": "roki",    "name": "労働基準法",             "short": "労基"},
    {"id": "roan",    "name": "労働安全衛生法",           "short": "労安"},
    {"id": "rosai",   "name": "労働者災害補償保険法",      "short": "労災"},
    {"id": "koyo",    "name": "雇用保険法",               "short": "雇用"},
    {"id": "choshu",  "name": "労働保険徴収法",           "short": "徴収"},
    {"id": "kenpo",   "name": "健康保険法",               "short": "健保"},
    {"id": "kokunen", "name": "国民年金法",               "short": "国年"},
    {"id": "konen",   "name": "厚生年金保険法",           "short": "厚年"},
    {"id": "shaichi", "name": "社会保険一般常識",          "short": "社一"},
]
SUBJECT_MAP = {s["id"]: s for s in SUBJECTS}

# キャッシュキー
CACHE_Q  = "_cache_questions"
CACHE_P  = "_cache_progress"
CACHE_AD = "_cache_ads"
