from pathlib import Path
import json
from datetime import datetime
from services.exchange_service import get_exchange_rates, calculate_jpy_to_php
from reports.report_generator import generate_report
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# =========================
# 設定読み込み
# =========================
from config import EXCHANGE_API_KEY, BASE_CURRENCY, TARGET_CURRENCIES, SLACK_BOT_TOKEN, SLACK_CHANNEL

# =========================
# 保存先パス
# =========================
REPORT_DIR = Path("reports")
PREV_RATE_FILE = Path("prev_rates/prev_rates.json")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PREV_RATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# =========================
# 前回レート読み込み
# =========================
prev_rates = None
prev_updated_at = None
if PREV_RATE_FILE.exists():
    try:
        with PREV_RATE_FILE.open("r", encoding="utf-8") as f:
            prev_data = json.load(f)
            prev_rates = prev_data.get("rates")
            prev_updated_at = prev_data.get("updated_at")
    except Exception as e:
        print(f"前回レート読み込みエラー: {e}")

# =========================
# 今日のレート取得
# =========================
rate_data = get_exchange_rates(base=BASE_CURRENCY, targets=TARGET_CURRENCIES, api_key=EXCHANGE_API_KEY)
jpy_to_php = calculate_jpy_to_php(rate_data)

# =========================
# レポート作成
# =========================
today_str = datetime.now().strftime("%Y-%m-%d")
report_text = generate_report(rate_data, jpy_to_php, prev_rates=prev_rates, prev_updated_at=prev_updated_at)

# =========================
# ローカル保存
# =========================
report_file_path = REPORT_DIR / f"daily_report_{today_str}.txt"
with report_file_path.open("w", encoding="utf-8") as f:
    f.write(report_text)

# 今日のレートを prev_rates.json に保存
prev_data_to_save = {
    "updated_at": today_str,
    "rates": rate_data["rates"]
}
with PREV_RATE_FILE.open("w", encoding="utf-8") as f:
    json.dump(prev_data_to_save, f, ensure_ascii=False, indent=2)

print(report_text)
print(f"レポートを {report_file_path} に保存しました。")

# =========================
# Slack通知
# =========================
if SLACK_BOT_TOKEN and SLACK_CHANNEL:
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=report_text
        )
        print("Slack通知送信成功！")
    except SlackApiError as e:
        print(f"Slack通知失敗: {e.response['error']}")
else:
    print("Slack情報が設定されていないため通知は送信されません。")