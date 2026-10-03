# Universal Weather Clock

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B%20(tested%203.13)-blue.svg)

シンプルで視認性の高い天気予報・地震情報付きデスクトップ時計アプリケーション。IPアドレスから自動的に現在地を特定し、リアルタイムで気象情報と最新地震情報を表示します。

## 特徴

- 📍 **自動位置情報取得**: IPアドレスから現在地を自動判定
- 🌤️ **リアルタイム天気表示**: Open-Meteo APIで30分間隔に更新
- 🕐 **正確な時刻表示**: 1秒単位で更新される24時間時計
- 🗾 **全国10地域・49都市対応**: 地域→都市の階層メニューで切り替え可能
- 📮 **郵便番号検索**: HeartRails Geo APIで郵便番号から住所・緯度経度を自動変換
- 🔴 **最新地震情報表示**: P2P地震情報APIで最新5件を10分間隔に更新
- 🛡️ **フォールバック機能**: ネットワーク障害時も東京の天気を表示
- 🎨 **シンプルなUI**: 黒背景に見やすい色分けされたテキスト

## 必要な環境

- Python 3.10以上（動作確認・推奨バージョンは **Python 3.13**）
- tkinter（通常Pythonに同梱）
- requests ライブラリ

## インストール

### リポジトリのクローン
```bash
git clone https://github.com/YOUR_USERNAME/universal-weather-clock.git
cd universal-weather-clock
```

### 仮想環境の作成（推奨）
```bash
# Windows（Python Install Manager）
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3.13 -m venv .venv
source .venv/bin/activate
```

### 依存ライブラリのインストール

依存パッケージは、用途に応じて2つのファイルに分けています。

| ファイル | 対象 | 内容 |
|----------|------|------|
| `requirements.txt` | アプリを実行する方 | requests とその依存パッケージ |
| `requirements-dev.txt` | 開発・exe化を行う方 | `requirements.txt` の内容 + 開発用ツール |

#### アプリを実行する場合

```bash
pip install -r requirements.txt
```

#### 開発・exe化を行う場合

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` は先頭で `requirements.txt` を読み込んでいるため、実行用のパッケージも一緒にインストールされます。追加される開発用ツールは以下のとおりです。

| ツール | 用途 |
|--------|------|
| [Nuitka](https://nuitka.net/) | exeファイルの作成 |
| [zstandard](https://pypi.org/project/zstandard/) | Nuitka（onefile形式）での圧縮 |
| [pip-audit](https://pypi.org/project/pip-audit/) | 依存パッケージの脆弱性チェック |

## 使い方

### 基本的な起動
```bash
python clock.py
```

ウィンドウが起動し、現在地の天気と時刻が表示されます。

### 位置の手動変更

#### 階層メニューから選択

メニューバーの「地点変更」から地域を選ぶと、その地域の都市一覧がサブメニューで展開されます。

| 地域 | 収録都市（例） |
|------|--------------|
| 北海道 | 札幌市、旭川市、函館市、釧路市、稚内市 |
| 東北 | 青森市、秋田市、盛岡市、仙台市、山形市、福島市 |
| 関東甲信 | 東京都、横浜市、さいたま市、千葉市、水戸市 他 |
| 北陸 | 新潟市、富山市、金沢市、福井市 |
| 東海 | 静岡市、名古屋市、岐阜市、津市 |
| 近畿 | 大阪市、京都市、神戸市、奈良市、和歌山市、大津市 |
| 中国 | 広島市、岡山市、鳥取市、松江市、山口市 |
| 四国 | 高松市、徳島市、松山市、高知市 |
| 九州 | 福岡市、佐賀市、長崎市、熊本市、大分市、宮崎市、鹿児島市 |
| 沖縄 | 那覇市、名護市、久米島町、宮古島市、石垣市 |

#### 郵便番号検索

画面下部の郵便番号入力欄に7桁の郵便番号を入力して「検索」ボタンを押すか、Enterキーを押してください。ハイフンあり・なし両方に対応しています。

```
例: 1600022 または 160-0022
```

住所・緯度・経度が自動取得され、その地点の天気が即座に表示されます。

#### 現在地の再取得

「地点変更」→「現在地を自動再取得」を選ぶと、IP判定を再実行して現在地を更新します。

## exeファイルの作成（Windows）

[Nuitka](https://nuitka.net/) を使用して、単体で動作するexeファイルを作成できます。

### 事前準備

開発用ツールをインストールしておきます。

```powershell
pip install -r requirements-dev.txt
```

Python 3.13 では Nuitka の MinGW64 が使用できないため、**Visual Studio Build Tools**（C++ によるデスクトップ開発）が必要です。

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

### ビルド

```powershell
# 実行用パッケージの脆弱性チェック（問題がないことを確認してからビルドする）
pip-audit -r requirements.txt

# exeファイルの作成
python -m nuitka `
  --mode=onefile `
  --windows-console-mode=disable `
  --enable-plugin=tk-inter `
  --msvc=latest `
  --output-dir=build `
  --output-filename=UniversalWeatherClock.exe `
  --onefile-tempdir-spec="{CACHE_DIR}/UniversalWeatherClock/{VERSION}" `
  --product-name="Universal Weather Clock" `
  --file-version=1.2.0 `
  --product-version=1.2.0 `
  --assume-yes-for-downloads `
  --remove-output `
  clock.py
```

`build\UniversalWeatherClock.exe` が作成されます。

> ⚠️ `--file-version` / `--product-version` はリリースごとに必ず更新してください。展開先フォルダがバージョンごとに分かれているため、更新しないと古いファイルが使われる場合があります。

## 動作仕様

### 天気更新のタイミング
- **初回**: アプリケーション起動時
- **定期更新**: 30分ごと（1,800,000ミリ秒）
- **手動更新**: メニューまたは郵便番号検索で位置を変更した時点で即座に更新

### 使用API

| API | 用途 | タイムアウト |
|-----|------|----------|
| [ip-api.com](https://ip-api.com/) | 現在地の位置情報取得 | 5秒 |
| [Open-Meteo](https://open-meteo.com/) | 天気情報取得 | 10秒 |
| [HeartRails Geo API](https://geoapi.heartrails.com/) | 郵便番号→住所・緯度経度変換 | 10秒 |
| [P2P地震情報 API](https://www.p2pquake.net/develop/api_v2_client_api/) | 最新地震情報取得 | 10秒 |

いずれもAPIキー不要で利用できます。

### 天気コード対応表（WMO 4677 / Open-Meteo準拠）

Open-MeteoはWMO（世界気象機関）の天気コードに準拠しています。v1.0.1より全コードに対応しました。

| コード | 天気 |
|--------|------|
| 0 | 快晴 |
| 1 | 晴れ |
| 2 | 曇時々晴 |
| 3 | 曇り |
| 45 | 霧 |
| 48 | 着氷性の霧 |
| 51 | 小雨（霧雨） |
| 53 | 霧雨 |
| 55 | 強い霧雨 |
| 56 | 着氷性の霧雨（弱） |
| 57 | 着氷性の霧雨（強） |
| 61 | 小雨 |
| 63 | 雨 |
| 65 | 大雨 |
| 66 | 着氷性の雨（弱） |
| 67 | 着氷性の雨（強） |
| 71 | 小雪 |
| 73 | 雪 |
| 75 | 大雪 |
| 77 | 霰（みぞれ） |
| 80 | にわか雨（弱） |
| 81 | にわか雨 |
| 82 | にわか雨（強） |
| 85 | にわか雪（弱） |
| 86 | にわか雪（強） |
| 95 | 雷雨 |
| 96 | 雷雨と小さな雹 |
| 99 | 雷雨と大きな雹 |

未知のコードが返された場合は `不明(コード:XX)` と表示されます。

### エラーハンドリング

| 状況 | 動作 |
|------|------|
| IP取得失敗 | 東京都(新宿)の天気を表示 |
| 天気データ取得失敗 | 「データ取得エラー」を表示 |
| ネットワーク障害 | ステータスに「更新失敗」と表示 |
| 郵便番号が不正（7桁以外） | エラーダイアログで通知 |
| 郵便番号が未登録 | エラーダイアログで通知 |
| HeartRails API接続失敗 | エラーダイアログで通知（通信エラー） |
| 郵便番号APIの応答データが不正 | エラーダイアログで通知（取得エラー） |
| 地震情報取得失敗 | 「地震情報取得エラー」を表示 |

## 出力例

```
2026/04/25(土)
14:32:45

東京都新宿区西新宿: 晴れ 22℃
情報更新: 14:32 (自動取得)

── 最新地震情報 ──
2026/06/08 13:45  千葉県東方沖  M3.2
2026/06/08 10:12  茨城県南部  M2.8
2026/06/07 22:30  福島県沖  M4.1
2026/06/07 18:55  岩手県沿岸北部  M3.5
2026/06/07 09:03  長野県中部  M2.5
```

## ソースコード構成

```python
get_current_location_by_ip()          # IP -> 位置情報変換
get_location_by_zipcode(zipcode)       # 郵便番号 -> 住所・緯度経度変換
on_zipcode_search()                    # 郵便番号検索ボタンのイベントハンドラ
get_weather(city_name, lat, lon)       # 天気情報取得 & 表示更新
get_earthquake_info()                  # 地震情報取得 & 表示更新（10分ごと）
update_clock()                         # 時計の1秒ごと更新
setup_initial_location()               # 初期化処理
```

## カスタマイズ例

### 都市の追加

`LOCATIONS`辞書の該当地域に座標を追加してください：

```python
LOCATIONS = {
    "関東甲信": {
        # ... 既存の都市 ...
        "新しい都市": {"lat": 緯度, "lon": 経度},
    }
}
```

### 地域の追加

新しい地域キーを追加するだけでサブメニューに自動反映されます：

```python
LOCATIONS = {
    # ... 既存の地域 ...
    "海外": {
        "ニューヨーク": {"lat": 40.7128, "lon": -74.0060},
        "ロンドン":     {"lat": 51.5074, "lon": -0.1278},
    }
}
```

### デフォルト位置の変更

`get_current_location_by_ip()`関数のフォールバック部分を修正：

```python
# フォールバック地点を変更
return "大阪市", 34.6937, 135.5023
```

### 更新間隔・表示件数の変更

ファイル先頭の定数を修正してください（間隔はミリ秒単位）：

```python
CLOCK_INTERVAL_MS = 1000  # 時計：1秒
WEATHER_INTERVAL_MS = 30 * 60 * 1000  # 天気：30分
QUAKE_INTERVAL_MS = 10 * 60 * 1000  # 地震情報：10分
QUAKE_DISPLAY_LIMIT = 5  # 地震情報の表示件数
```

## 日本語対応

このアプリケーションは日本語環境を前提としています。フォントは`MS Gothic`を使用していますが、環境に応じて変更可能です：

```python
clock_label = tk.Label(root, font=("ヒラギノ角ゴ Pro", 36, "bold"), ...)
```

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 著作権

Copyright (c) 2026 大杉一実 (ohsugi kazumi)

## 既知の制限事項

- Windows/macOS/Linuxで動作確認済み（GUIはplatform依存）
- ネットワーク接続が必須（初回の位置情報取得時）
- 位置情報精度はISP単位のため、正確性は保証されません
- 郵便番号検索はHeartRails Geo APIのカバー範囲（日本国内）に限定されます

## トラブルシューティング

### tkinterが見つからないエラー
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (Homebrew)
brew install python-tk@3.13
```

### ネットワークエラーが頻発する場合

タイムアウト値を増やしてください：

```python
response = requests.get(..., timeout=15)  # 15秒に延長
```

### exe作成時に「cannot locate suitable C compiler」と表示される

Python 3.13 では MinGW64 が使用できません。「[exeファイルの作成（Windows）](#exeファイルの作成windows)」の事前準備に従って Visual Studio Build Tools をインストールし、`--msvc=latest` を指定してください。

## 貢献

バグ報告や機能提案はIssuesセクションにお願いします。

## 更新履歴

### v1.2.0 (2026-10-03)
- 開発・動作確認環境を Python 3.11 から **Python 3.13** へ移行（ソースコードの変更なし。動作環境は引き続き Python 3.10以上）
- 依存パッケージを更新し、実行用の `requirements.txt` と開発用の `requirements-dev.txt` に分割
- urllib3 を 2.8.0 に更新（2.7.0 の既知の脆弱性 PYSEC-2026-4175 / 4176 / 4177 に対応）
- 脆弱性チェックツール [pip-audit](https://pypi.org/project/pip-audit/) を開発環境に導入
- Nuitka によるexeファイル作成手順を追加（Python 3.13 対応のため MSVC を使用）

### v1.1.3 (2026-10-01)
- コード品質の改善（静的解析ツール [Ruff](https://docs.astral.sh/ruff/) の全ルールに準拠）
- `except Exception` による一括捕捉をやめ、想定する例外（通信エラー・データ解析エラーなど）のみを捕捉するよう変更
- 郵便番号検索で、通信エラーと応答データの解析エラーを別のメッセージで通知するよう改善
- 地震情報の時刻に日本時間（JST）のタイムゾーンを付与
- 更新間隔・郵便番号の桁数・地震情報の表示件数を定数化
- 天気更新タイマーIDの管理を `global` 文から辞書 `timer_state` に変更
- 全関数に型ヒントを追加（これに伴い動作環境を Python 3.10以上に変更）

### v1.1.2 (2026-06-15)
- 天気更新タイマーの重複蓄積バグを修正
- 地点を手動変更するたびに古いタイマーが残存し、数時間後に表示が元の場所に戻ってしまう問題を解消
- `root.after()` のIDを `weather_timer_id` で管理し、新規タイマーセット前に `root.after_cancel()` で旧タイマーをキャンセルする方式に変更

### v1.1.1 (2026-06-08)
- 地震情報の重複表示を修正（同一地震が複数レコードで返される場合に除去）
- APIの取得件数を limit=5 → limit=10 に変更（重複除去後に5件を確保するため）

### v1.1.0 (2026-06-08)
- 最新地震情報の表示機能を追加（P2P地震情報API使用）
- 地震情報は新しい順に最大5件を表示、10分ごとに自動更新

### v1.0.1 (2026-04-27)
- WMO天気コードの対応を10種類から29種類に拡充（WMO 4677 / Open-Meteo準拠）
- 未知の天気コードを受信した場合にコード番号を表示するよう改善

### v1.0.0 (2026-04-25)
- 初回リリース
- IPアドレスによる自動位置情報取得
- Open-Meteo APIによる天気表示（30分自動更新）
- 全国10地域・49都市の階層メニューによる手動切り替え
- 郵便番号検索機能（HeartRails Geo API使用）

---

**最終更新**: 2026年10月
