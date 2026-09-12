# ページ契約

`ine/index.html` は部品の見本である。同じ骨格を守る必要はない。クラス名は使ってよい。色・飾り・フォントは旅ごとに新しくする。

必須セクションは必ず必須でなくてもいいし、順序や構成も都度変更していい。ただし AI とすぐわかるようなデザインは避けること。

## よく使う部品

旅に合わせて採る・捨てる・並べ替える。全部載せなくてよい。

1. 見出し（縦書きキッカー、題、泊数などの副題、目次へ戻る）
2. 導入文とスタンプ
3. 挿絵（`{slug}/images/`）
4. 往復の交通（空路・鉄道・車など、その旅の主経路）
5. 地図 + 日フィルタ + 凡例
6. 日程（日ごと。時刻・題・一言）
7. 注意
8. 心得
9. 出典・目安時刻の注記

## データ

地図や日程を置くときの形。置かない旅ならこの塊ごと不要。ページ内スクリプトで持つ。

```js
const places = {
  key: { name: "表示名", lat: 35.0, lng: 135.0, sub: "短い役割" }
};

const days = [
  {
    id: 1,
    label: "一日　…",
    stay: "宿泊地または帰着",
    color: "#3a5366",
    bounds: [[south, west], [north, east]],
    gmaps: "https://www.google.com/maps/dir/地点A/地点B",
    items: [
      { time: "07:00〜10:30", title: "移動や滞在の題", place: "key", note: "補足" }
    ]
  }
];
```

`routes` は `[[lat, lng], ...]`。必ずスクリプトで取得した実ルートを入れる。

```bash
python3 .cursor/skills/create-itinerary/scripts/fetch-route.py \
  --from-name "大阪国際空港" --to-name "京都駅"
```

座標が分かっているとき:

```bash
python3 .cursor/skills/create-itinerary/scripts/fetch-route.py \
  --from 135.4382,34.7855 --to 135.7588,34.9858
```

標準出力は Leaflet 用の `[[lat,lng],...]`。複数区間は区間ごとに呼ぶ。Nominatim は 1 秒以上空ける。

## 地図

地図を置くとき:

- ライブラリ: Leaflet 1.9.x（unpkg）
- 国内タイル: `https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png`  
  帰属: 国土地理院
- 国外タイル: Carto Positron または OSM（帰属を残す）
- 初期表示は全日。日ボタンで線とピンを切り替える
- 日程行クリックで `flyTo` とポップアップ
- ピンは数字や一字。角はテーマに合わせる（伊根の矩形を必須にしない）

## 目次カード

`index.html` の既存 `.trip` と同じ格子。中身だけ足す。

```html
<a class="trip" href="{slug}/">
  <div>
    <h2>題</h2>
    <p>一文の要約。</p>
    <div class="stamps">
      <span class="stamp">泊数</span>
      <span class="stamp">経路</span>
    </div>
  </div>
  <div class="trip-art">
    <img src="{slug}/images/a.png" alt="" width="640" height="360" />
    <img src="{slug}/images/b.png" alt="" width="640" height="360" />
  </div>
</a>
```

`README.md` の表:

```
| [題]({slug}/) | `{slug}/` |
```
