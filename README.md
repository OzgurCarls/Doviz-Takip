# 💱 Döviz & Altın Takip Aracı

Python ile gerçek zamanlı döviz ve altın fiyatlarını çeken, alarmlayan ve görselleştiren bir araç.

## Özellikler

- 🌐 Doviz.com'dan gerçek zamanlı veri çekme (BeautifulSoup)
- ⏰ Her 5 dakikada otomatik veri güncelleme (schedule)
- 📁 Geçmiş verileri CSV'ye kaydetme (zaman serisi oluşturma)
- 🔴 Fiyat alarm sistemi (üst/alt eşik tanımlama)
- 📊 Dolar ve Altın fiyat grafikleri (matplotlib)

## Takip Edilen Varlıklar

- Gram Altın
- Dolar
- Euro
- Sterlin
- Bitcoin
- Gram Gümüş
- Brent Petrol
- BIST 100

## Kullanılan Teknolojiler

- Python
- requests
- BeautifulSoup4
- pandas
- matplotlib
- schedule

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

Veri toplamak için:
```bash
python main.py
```

Grafik oluşturmak için:
```bash
python grafik.py
```

## Alarm Ayarlama

`main.py` içindeki `ALARMLAR` sözlüğünü düzenle:

```python
ALARMLAR = {
    "DOLAR": {"ust": 48.0, "alt": 46.0},
    "GRAM ALTIN": {"ust": 6200.0, "alt": 6000.0},
}
```