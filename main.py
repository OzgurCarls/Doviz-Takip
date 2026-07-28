import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import schedule
import time

def doviz_verisi_cek():
    url = "https://www.doviz.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    veriler = []
    kutular = soup.find_all("div", class_="item")
    
    for kutu in kutular:
        try:
            isim = kutu.find("span", class_="name").text.strip()
            fiyat_str = kutu.find("span", class_="value").text.strip()
            fiyat_temiz = fiyat_str.replace("$", "").replace(".", "").replace(",", ".").strip()
            try:
                fiyat = float(fiyat_temiz)
            except:
                fiyat = None

            veriler.append({
                "isim": isim,
                "fiyat": fiyat,
                "ham_fiyat": fiyat_str,
                "tarih": datetime.now().strftime("%Y-%m-%d"),
                "saat": datetime.now().strftime("%H:%M:%S")
            })
        except:
            continue
    
    return pd.DataFrame(veriler)


def csv_ye_kaydet(df, dosya="doviz_gecmis.csv"):
    if os.path.exists(dosya):
        mevcut = pd.read_csv(dosya)
        df = pd.concat([mevcut, df], ignore_index=True)
    df.to_csv(dosya, index=False)

    # Alarm eşikleri — istediğin değerleri gir
ALARMLAR = {
    "DOLAR": {"ust": 47.0, "alt": 46.0},      
    "GRAM ALTIN": {"ust": 6130.0, "alt": 6000.0},  
    "EURO": {"ust": 55.0, "alt": 52.0},
}

def alarm_kontrol(df):
    """Fiyatlar alarm eşiklerini geçti mi kontrol eder."""
    for _, satir in df.iterrows():
        isim = satir["isim"]
        fiyat = satir["fiyat"]
        
        if isim in ALARMLAR and fiyat is not None:
            esikler = ALARMLAR[isim]
            
            if fiyat > esikler["ust"]:
                print(f"🔴 ALARM! {isim} {fiyat} → ÜST EŞİĞİ ({esikler['ust']}) AŞTI!")
            elif fiyat < esikler["alt"]:
                print(f"🟢 ALARM! {isim} {fiyat} → ALT EŞİĞİ ({esikler['alt']}) ALTINA DÜŞTÜ!")


def veri_cek_ve_kaydet():
    """Zamanlayıcının her tetiklenişinde çağrılan fonksiyon."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Veri çekiliyor...")
    df = doviz_verisi_cek()
    csv_ye_kaydet(df)
    
    # Anlık özet
    for _, satir in df.iterrows():
        print(f"  {satir['isim']:<15} {satir['ham_fiyat']}")
    
    # Yeni eklenen kısım:
    alarm_kontrol(df)
    
    print("✅ Kaydedildi.")


# İlk çalıştırma hemen olsun
veri_cek_ve_kaydet()

# Sonraki çalıştırmalar her 5 dakikada bir
schedule.every(5).minutes.do(veri_cek_ve_kaydet)

print("\n⏰ Zamanlayıcı başladı — her 5 dakikada veri çekilecek.")
print("Durdurmak için Ctrl+C\n")

# Sürekli çalış
while True:
    schedule.run_pending()
    time.sleep(1)