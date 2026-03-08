# reports/report_generator.py

CURRENCY_FLAGS = {
    "USD": ":us:",
    "JPY": ":jp:",
    "PHP": ":flag-ph:"
}

# 前回比フォーマット
def format_diff(value):
    if value > 0:
        return f"+{value:.2f}"
    elif value < 0:
        return f"{value:.2f}"
    else:
        return "±0.00"

def generate_report(rate_data, jpy_to_php, prev_rates=None, prev_updated_at=None):
    from datetime import datetime
    today = datetime.now().strftime("%Y/%m/%d")
    date_header = f"----{today}-----\n"

    php_to_jpy = 1 / jpy_to_php

    # 前回比計算（差分）
    if prev_rates:
        jpy_diff = rate_data["rates"]["JPY"] - prev_rates["JPY"]
        php_diff = rate_data["rates"]["PHP"] - prev_rates["PHP"]
        jpy_to_php_prev = prev_rates["PHP"] / prev_rates["JPY"]
        jpy_to_php_diff = jpy_to_php - jpy_to_php_prev
        php_to_jpy_prev = 1 / jpy_to_php_prev
        php_to_jpy_diff = php_to_jpy - php_to_jpy_prev
    else:
        jpy_diff = php_diff = jpy_to_php_diff = php_to_jpy_diff = 0

    report_lines = [
        date_header.strip(),
        f"基準通貨: {rate_data['base']}{CURRENCY_FLAGS.get(rate_data['base'], '')}",
        f"USD → JPY: {rate_data['rates']['JPY']} ({format_diff(jpy_diff)})",
        f"USD → PHP: {rate_data['rates']['PHP']} ({format_diff(php_diff)})",
        "",
        f"1 JPY{CURRENCY_FLAGS.get('JPY','')} = {jpy_to_php:.2f} PHP ({format_diff(jpy_to_php_diff)})",
        f"1 PHP{CURRENCY_FLAGS.get('PHP','')} = {php_to_jpy:.2f} JPY ({format_diff(php_to_jpy_diff)})"
    ]

    # 前回更新日を追記
    if prev_updated_at:
        report_lines.append(f"\n※前回レート更新日: {prev_updated_at}")

    return "\n".join(report_lines)