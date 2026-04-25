"""
Universal Weather Clock
Copyright (c) 2026 大杉一実 (ohsugi kazumi)
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests

# 地域 -> 都市の階層構造リスト
LOCATIONS = {
    "北海道": {
        "札幌市": {"lat": 43.0642, "lon": 141.3469},
        "旭川市": {"lat": 43.7703, "lon": 142.3649},
        "函館市": {"lat": 41.7688, "lon": 140.7290},
        "釧路市": {"lat": 42.9848, "lon": 144.3820},
        "稚内市": {"lat": 45.4016, "lon": 141.6738},
    },
    "東北": {
        "青森市": {"lat": 40.8222, "lon": 140.7474},
        "秋田市": {"lat": 39.7186, "lon": 140.1024},
        "盛岡市": {"lat": 39.7036, "lon": 141.1527},
        "仙台市": {"lat": 38.2682, "lon": 140.8694},
        "山形市": {"lat": 38.2404, "lon": 140.3636},
        "福島市": {"lat": 37.7608, "lon": 140.4748},
    },
    "関東甲信": {
        "東京都": {"lat": 35.6895, "lon": 139.6917},
        "横浜市": {"lat": 35.4437, "lon": 139.6380},
        "さいたま市": {"lat": 35.8617, "lon": 139.6455},
        "千葉市": {"lat": 35.6074, "lon": 140.1265},
        "水戸市": {"lat": 36.3418, "lon": 140.4468},
        "宇都宮市": {"lat": 36.5658, "lon": 139.8836},
        "前橋市": {"lat": 36.3895, "lon": 139.0634},
        "甲府市": {"lat": 35.6635, "lon": 138.5684},
        "長野市": {"lat": 36.6485, "lon": 138.1940},
    },
    "北陸": {
        "新潟市": {"lat": 37.9026, "lon": 139.0232},
        "富山市": {"lat": 36.6953, "lon": 137.2113},
        "金沢市": {"lat": 36.5944, "lon": 136.6256},
        "福井市": {"lat": 36.0652, "lon": 136.2218},
    },
    "東海": {
        "静岡市": {"lat": 34.9756, "lon": 138.3828},
        "名古屋市": {"lat": 35.1815, "lon": 136.9064},
        "岐阜市": {"lat": 35.4232, "lon": 136.7608},
        "津市":   {"lat": 34.7303, "lon": 136.5086},
    },
    "近畿": {
        "大阪市": {"lat": 34.6937, "lon": 135.5023},
        "京都市": {"lat": 35.0116, "lon": 135.7681},
        "神戸市": {"lat": 34.6913, "lon": 135.1830},
        "奈良市": {"lat": 34.6851, "lon": 135.8050},
        "和歌山市": {"lat": 34.2261, "lon": 135.1675},
        "大津市": {"lat": 35.0045, "lon": 135.8686},
    },
    "中国": {
        "広島市": {"lat": 34.3853, "lon": 132.4553},
        "岡山市": {"lat": 34.6553, "lon": 133.9195},
        "鳥取市": {"lat": 35.5011, "lon": 134.2351},
        "松江市": {"lat": 35.4681, "lon": 133.0485},
        "山口市": {"lat": 34.1860, "lon": 131.4706},
    },
    "四国": {
        "高松市": {"lat": 34.3401, "lon": 134.0434},
        "徳島市": {"lat": 34.0658, "lon": 134.5593},
        "松山市": {"lat": 33.8416, "lon": 132.7657},
        "高知市": {"lat": 33.5597, "lon": 133.5311},
    },
    "九州": {
        "福岡市": {"lat": 33.5902, "lon": 130.4017},
        "佐賀市": {"lat": 33.2494, "lon": 130.2989},
        "長崎市": {"lat": 32.7503, "lon": 129.8779},
        "熊本市": {"lat": 32.7898, "lon": 130.7417},
        "大分市": {"lat": 33.2382, "lon": 131.6126},
        "宮崎市": {"lat": 31.9111, "lon": 131.4239},
        "鹿児島市": {"lat": 31.5966, "lon": 130.5571},
    },
    "沖縄": {
        "那覇市": {"lat": 26.2124, "lon": 127.6809},
        "名護市": {"lat": 26.5914, "lon": 127.9774},
        "久米島町": {"lat": 26.3395, "lon": 126.8044},
        "宮古島市": {"lat": 24.8055, "lon": 125.2810},
        "石垣市": {"lat": 24.3448, "lon": 124.1572},
    },
}


def get_current_location_by_ip():
    """
    IPアドレスから現在地の位置情報を取得する。
    取得に失敗した場合は、デフォルトとして東京都(新宿)の情報を返す。
    """
    try:
        response = requests.get("http://ip-api.com/json/?lang=ja", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["city"], data["lat"], data["lon"]
    except Exception:
        pass

    # フォールバック地点（新宿）
    return "東京都(新宿)", 35.6895, 139.6917


def get_location_by_zipcode(zipcode):
    """
    HeartRails Geo APIを使用して郵便番号から住所・緯度・経度を取得する。
    郵便番号はハイフンあり・なし両方に対応（例: 160-0022 または 1600022）。
    取得成功時は (city_name, lat, lon) を返す。
    失敗時は None を返す。
    """
    # ハイフンを除去して7桁に統一
    zipcode_clean = zipcode.replace("-", "").strip()

    if len(zipcode_clean) != 7 or not zipcode_clean.isdigit():
        messagebox.showerror("入力エラー", "郵便番号は7桁の数字で入力してください。\n例: 1600022 または 160-0022")
        return None

    try:
        url = f"https://geoapi.heartrails.com/api/json?method=searchByPostal&postal={zipcode_clean}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        locations = data.get("response", {}).get("location")
        if not locations:
            messagebox.showerror("取得エラー", f"郵便番号 {zipcode} に対応する住所が見つかりませんでした。")
            return None

        # 先頭の結果を使用
        loc = locations[0]
        prefecture = loc.get("prefecture", "")
        city = loc.get("city", "")
        town = loc.get("town", "")
        lat = float(loc.get("y"))  # HeartRails は緯度を "y" で返す
        lon = float(loc.get("x"))  # HeartRails は経度を "x" で返す
        city_name = f"{prefecture}{city}{town}"

        return city_name, lat, lon

    except Exception as e:
        messagebox.showerror("通信エラー", f"HeartRails Geo APIへの接続に失敗しました。\n{e}")
        return None


def on_zipcode_search():
    """
    郵便番号入力欄の内容を取得し、位置情報を検索して天気を更新する。
    """
    zipcode = zipcode_entry.get().strip()
    if not zipcode:
        messagebox.showwarning("入力なし", "郵便番号を入力してください。")
        return

    weather_label.config(text="住所を検索中...")
    status_label.config(text="")
    root.update_idletasks()

    result = get_location_by_zipcode(zipcode)
    if result:
        city_name, lat, lon = result
        get_weather(city_name, lat, lon)


def get_weather(city_name, lat, lon):
    """
    Open-Meteo APIを使用して指定された座標の天気を取得し、GUIを更新する。
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true&timezone=Asia%2FTokyo"
        )
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

# 地域 -> 都市の階層サブメニューを構築
for region, cities in LOCATIONS.items():
    sub_menu = tk.Menu(loc_menu, tearoff=0)
    for city, coords in cities.items():
        sub_menu.add_command(
            label=city,
            command=lambda c=city, la=coords["lat"], lo=coords["lon"]: get_weather(
                c, la, lo
            ),
        )
    loc_menu.add_cascade(label=region, menu=sub_menu)

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

# --- 郵便番号入力エリア ---
zipcode_frame = tk.Frame(root, bg="black")
zipcode_frame.pack(pady=(0, 8))

tk.Label(
    zipcode_frame, text="郵便番号:", font=("MS Gothic", 11), fg="gray", bg="black"
).pack(side=tk.LEFT, padx=(0, 4))

zipcode_entry = tk.Entry(
    zipcode_frame, font=("MS Gothic", 13), width=10,
    bg="#1a1a1a", fg="white", insertbackground="white",
    relief=tk.FLAT, bd=2
)
zipcode_entry.pack(side=tk.LEFT, padx=(0, 6))
# Enterキーでも検索できるようにバインド
zipcode_entry.bind("<Return>", lambda event: on_zipcode_search())

tk.Button(
    zipcode_frame, text="検索", font=("MS Gothic", 11),
    bg="#333333", fg="white", activebackground="#555555", activeforeground="white",
    relief=tk.FLAT, padx=8, pady=2,
    command=on_zipcode_search
).pack(side=tk.LEFT)

# --- プログラム実行 ---
if __name__ == "__main__":
    update_clock()
    setup_initial_location()
    root.mainloop()
