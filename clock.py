"""
Universal Weather Clock
Copyright (c) 2026 大杉一実 (ohsugi kazumi)
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

import tkinter as tk
from datetime import datetime
import requests

# 手動選択用の主要都市リスト（IP取得失敗時や出張時用）
LOCATIONS = {
    "地方選択": {
        "札幌市": {"lat": 43.0642, "lon": 141.3469},
        "仙台市": {"lat": 38.2682, "lon": 140.8694},
        "さいたま市": {"lat": 35.8617, "lon": 139.6455},
        "千葉市": {"lat": 35.6074, "lon": 140.1265},
        "東京都": {"lat": 35.6895, "lon": 139.6917},
        "横浜市": {"lat": 35.4437, "lon": 139.6380},
        "相模原市": {"lat": 35.5751, "lon": 139.3711},
        "名古屋市": {"lat": 35.1815, "lon": 136.9064},
        "大阪市": {"lat": 34.6937, "lon": 135.5023},
        "広島市": {"lat": 34.3853, "lon": 132.4553},
        "福岡市": {"lat": 33.5902, "lon": 130.4017},
    }
}


def get_current_location_by_ip():
    """
    IPアドレスから現在地の位置情報を取得する。
    取得に失敗した場合は、デフォルトとして東京都(新宿)の情報を返す。
    """
    try:
        # 外部APIを使用してIPアドレスから位置情報を取得
        response = requests.get("http://ip-api.com/json/?lang=ja", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["city"], data["lat"], data["lon"]
    except Exception:
        pass
    
    # フォールバック地点（新宿）
    return "東京都(新宿)", 35.6895, 139.6917


def get_weather(city_name, lat, lon):
    """
    Open-Meteo APIを使用して指定された座標の天気を取得し、GUIを更新する。
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=Asia%2FTokyo"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp = data["current_weather"]["temperature"]
        weather_code = data["current_weather"]["weathercode"]

        # WMO Weather interpretation codes のマッピング
        weather_map = {
            0: "晴れ",
            1: "晴時々曇",
            2: "曇時々晴",
            3: "曇り",
            45: "霧",
            48: "霧",
            51: "小雨",
            61: "雨",
            71: "雪",
            95: "雷雨",
        }
        weather_text = weather_map.get(weather_code, "不明")

        # 表示ラベルの更新
        weather_label.config(text=f"{city_name}: {weather_text} {temp}℃")
        status_label.config(
            text=f"情報更新: {datetime.now().strftime('%H:%M')} (自動取得)"
        )

        # 30分（1,800,000ミリ秒）後に再更新をスケジュール
        root.after(1800000, lambda: get_weather(city_name, lat, lon))

    except Exception:
        weather_label.config(text="データ取得エラー")
        status_label.config(text="更新失敗")


def update_clock():
    """
    1秒ごとに現在時刻を取得し、時計表示を更新する。
    """
    now = datetime.now()
    weeks = ["月", "火", "水", "木", "金", "土", "日"]
    day_of_week = weeks[now.weekday()]
    date_str = now.strftime(f"%Y/%m/%d({day_of_week})")
    time_str = now.strftime("%H:%M:%S")
    
    clock_label.config(text=f"{date_str}\n{time_str}")
    clock_label.after(1000, update_clock)


def setup_initial_location():
    """
    アプリケーション起動時に現在地を特定し、初期表示を行う。
    """
    weather_label.config(text="現在地を取得中...")
    city, lat, lon = get_current_location_by_ip()
    get_weather(city, lat, lon)


# --- GUI構成の初期化 ---
root = tk.Tk()
root.title("Universal Weather Clock")
root.configure(bg="black")

# メニューバーの設定
menubar = tk.Menu(root)
root.config(menu=menubar)
loc_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="地点変更", menu=loc_menu)

# 都市リストをメニューに追加
for city, coords in LOCATIONS["地方選択"].items():
    loc_menu.add_command(
        label=city,
        command=lambda c=city, la=coords["lat"], lo=coords["lon"]: get_weather(
            c, la, lo
        ),
    )

# 現在地再取得オプション
loc_menu.add_separator()
loc_menu.add_command(
    label="現在地を自動再取得", command=setup_initial_location
)

# ウィジェットの作成と配置
clock_label = tk.Label(
    root, font=("MS Gothic", 36, "bold"), fg="cyan", bg="black", padx=20, pady=10
)
clock_label.pack()

weather_label = tk.Label(root, font=("MS Gothic", 20), fg="white", bg="black")
weather_label.pack()

status_label = tk.Label(root, font=("MS Gothic", 10), fg="gray", bg="black", pady=5)
status_label.pack()

# --- プログラム実行 ---
if __name__ == "__main__":
    update_clock()
    setup_initial_location()
    root.mainloop()