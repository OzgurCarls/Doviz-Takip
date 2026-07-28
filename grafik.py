import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("doviz_gecmis.csv")

# ham_fiyat sütunundan fiyatı yeniden hesapla (güvenilir kaynak)
def ham_fiyat_temizle(deger):
    try:
        return float(str(deger).replace("$", "").replace(".", "").replace(",", ".").strip())
    except:
        return None

df["fiyat_temiz"] = df["ham_fiyat"].apply(ham_fiyat_temizle)
df["datetime"] = pd.to_datetime(df["tarih"] + " " + df["saat"])

dolar = df[df["isim"] == "DOLAR"].copy()
altin = df[df["isim"] == "GRAM ALTIN"].copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(dolar["datetime"], dolar["fiyat_temiz"], color="green", marker="o")
ax1.set_title("Dolar (TL)")
ax1.set_xlabel("Saat")
ax1.set_ylabel("Fiyat")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(True)
ax1.set_ylim(46, 49) 


ax2.plot(altin["datetime"], altin["fiyat_temiz"], color="gold", marker="o")
ax2.set_title("Gram Altın (TL)")
ax2.set_xlabel("Saat")
ax2.tick_params(axis="x", rotation=45)
ax2.grid(True)

plt.tight_layout()
plt.savefig("doviz_grafik.png")
print("✅ Grafik kaydedildi.")
plt.show()