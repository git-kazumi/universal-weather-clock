# Universal Weather Clock

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

シンプルで視認性の高い天気予報付きデスクトップ時計アプリケーション。IPアドレスから自動的に現在地を特定し、リアルタイムで気象情報を表示します。

## 特徴

- 📍 **自動位置情報取得**: IPアドレスから現在地を自動判定
- 🌤️ **リアルタイム天気表示**: Open-Meteo APIで30分間隔に更新
- 🕐 **正確な時刻表示**: 1秒単位で更新される24時間時計
- 🗾 **日本全主要都市対応**: 手動で位置を切り替え可能
- 🛡️ **フォールバック機能**: ネットワーク障害時も東京の天気を表示
- 🎨 **シンプルなUI**: 黒背景に見やすい色分けされたテキスト

## 必要な環境

- Python 3.7以上
- tkinter（通常Pythonに同梱）
- requests ライブラリ

## インストール

### リポジトリのクローン
```bash
git clone https://github.com/YOUR_USERNAME/universal-weather-clock.git
cd universal-weather-clock
```

### 依存ライブラリのインストール
```bash
pip install requests
```

## 使い方

### 基本的な起動
```bash
python clock.py
```

ウィンドウが起動し、現在地の天気と時刻が表示されます。

### 位置の手動変更

メニューバーの「地点変更」から以下の操作が可能です：

- **都市選択**: リストから日本全主要都市を選択
  - 札幌市、仙台市、さいたま市、千葉市、東京都、横浜市、相模原市、名古屋市、大阪市、広島市、福岡市
- **現在地を自動再取得**: IP判定を再実行して現在地を更新

## 動作仕様

### 天気更新のタイミング
- **初回**: アプリケーション起動時
- **定期更新**: 30分ごと（1,800,000ミリ秒）
- **手動更新**: メニューから位置を変更した時点で即座に更新

### 使用API

| API | 用途 | タイムアウト |
|-----|------|----------|
| [ip-api.com](https://ip-api.com/) | 位置情報取得 | 5秒 |
| [Open-Meteo](https://open-meteo.com/) | 天気情報取得 | 10秒 |

どちらもAPIキーが不要で、安定性が高いサービスです。

### エラーハンドリング

| 状況 | 動作 |
|------|------|
| IP取得失敗 | 東京都(新宿)の天気を表示 |
| 天気データ取得失敗 | 「データ取得エラー」を表示 |
| ネットワーク障害 | ステータスに「更新失敗」と表示 |

## 出力例

```
2026/04/11(金)
14:32:45

相模原市: 晴れ 18℃
情報更新: 14:32 (自動取得)
```

## ソースコード構成

```python
get_current_location_by_ip()      # IP→位置情報変換
get_weather(city_name, lat, lon)  # 天気情報取得＆表示更新
update_clock()                     # 時計の1秒ごと更新
setup_initial_location()           # 初期化処理
```

## カスタマイズ例

### 都市の追加

`LOCATIONS`辞書に座標を追加してください：

```python
LOCATIONS = {
    "地方選択": {
        # ... 既存の都市 ...
        "新しい都市": {"lat": 緯度, "lon": 経度},
    }
}
```

### デフォルト位置の変更

`get_current_location_by_ip()`関数のフォールバック部分を修正：

```python
# フォールバック地点を変更
return "大阪市", 34.6937, 135.5023
```

### 更新間隔の変更

`get_weather()`関数の以下の行を修正（ミリ秒単位）：

```python
root.after(1800000, ...)  # デフォルト30分
root.after(600000, ...)   # 10分に変更
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
- Open-Meteoの天気コード対応は基本的な気象条件に限定しています

## トラブルシューティング

### tkinterが見つからないエラー
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (Homebrew)
brew install python-tk@3.11
```

### ネットワークエラーが頻発する場合

タイムアウト値を増やしてください：

```python
response = requests.get(..., timeout=15)  # 15秒に延長
```

## 貢献

バグ報告や機能提案はIssuesセクションにお願いします。

---

**最終更新**: 2026年4月
