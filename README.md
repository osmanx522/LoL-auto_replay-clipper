# LoL Auto-Replay Clipper

League of Legends oynarken ekranı arka planda sürekli kaydeden, öldüğünde veya kill aldığında son saniyeleri otomatik olarak `.mp4` klibe dönüştüren bir Python aracı.

Oyun verisi Riot'un resmi **Live Client Data API**'sinden okunur. Bu API maç sırasında bilgisayarda yerel olarak çalışır (`https://127.0.0.1:2999`). Oyunun belleğine erişilmez, oyuna müdahale edilmez.

## Özellikler

- Ölüm ve kill anlarını otomatik algılama
- RAM'de sürekli güncellenen döngüsel video tamponu (ring buffer)
- Olaydan önceki ve sonraki saniyeleri içeren klipler
- Kareler RAM'de JPEG olarak sıkıştırılarak tutulur, bu sayede bellek kullanımı düşük kalır
- Ekran yakalama ve API dinleme ayrı thread'lerde çalışır, birbirini bekletmez
- Ctrl+C ile güvenli kapatma

## Gereksinimler

- Windows
- Python 3.10 veya üzeri
- League of Legends (oyun **Kenarlıksız** veya **Pencere** modunda olmalı, tam ekranda görüntü siyah çıkabilir)

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install requests urllib3 mss opencv-python numpy
```

## Kullanım

```bash
python main.py
```

1. Programı çalıştır, ardından bir maça (veya Practice Tool'a) gir.
2. Öldüğünde veya kill aldığında klip otomatik olarak `klipler/` klasörüne kaydedilir.
3. Kapatmak için terminalde `Ctrl+C`'ye bas.

Klip adları şu formattadır:

```
LOL[death]-26_11_2026_153012_482913.mp4
LOL[kill]-26_11_2026_153145_120934.mp4
```

## Ayarlar

Tüm ayarlar `config.py` dosyasındadır.

| Ayar | Açıklama | Varsayılan |
|---|---|---|
| `FPS` | Saniyedeki kare sayısı | `30` |
| `SECOND` | Klibin toplam uzunluğu (saniye) | `20` |
| `AFTER_EVENT_SECOND` | Olaydan sonra kayda devam edilen süre (saniye) | `3` |
| `RESOLUTION` | Klip çözünürlüğü (genişlik, yükseklik) | `(1280, 800)` |
| `JPEG_QUALITY` | RAM'deki karelerin sıkıştırma kalitesi (0-100) | `70` |

Varsayılan ayarlarla bir klip olaydan önceki 17 saniyeyi ve sonraki 3 saniyeyi içerir.

## Proje Yapısı

```
main.py      Programın giriş noktası. Tamponu ve thread'leri oluşturur, Ctrl+C'yi bekler.
config.py    Tüm ayarlar.
lol_api.py   Live Client Data API'ye bağlanır, ölüm ve kill olaylarını algılar.
capture.py   Ekranı yakalar, küçültür, sıkıştırır ve tampona ekler.
buffer.py    Thread-safe döngüsel tampon (deque + Lock).
video.py     Tampondaki kareleri .mp4 dosyasına yazar.
```

## Nasıl Çalışır

```
[capture thread]  ekranı yakala -> küçült -> JPEG'e sıkıştır -> tampona ekle   (FPS kez/saniye)
[api thread]      API'yi sorgula -> skorları karşılaştır -> olay varsa callback'i çağır   (2 kez/saniye)
[kayıt thread]    AFTER_EVENT_SECOND bekle -> tamponun kopyasını al -> .mp4 olarak kaydet
```

Tampon `collections.deque(maxlen=...)` ile kurulmuştur. Dolduğunda en eski kare otomatik olarak silinir. Böylece RAM'de her zaman sadece son `SECOND` saniye tutulur.

## Bilinen Sınırlamalar

- Kliplerde ses yoktur (OpenCV `VideoWriter` ses desteklemez).
- Sadece ana monitör kaydedilir.
- API yalnızca aktif bir maç sırasında çalışır. İzleyici modu desteklenmez.

## Yol Haritası

- [ ] Rakip takımın aldığı Ejder ve Baron'u algılama
- [ ] Kayıt thread'lerinin güvenli kapatılması
- [ ] Grafik arayüz
- [ ] Highlight özelliği
