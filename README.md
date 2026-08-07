# Murciélago 🦇

**Murciélago**, saf Python ile yazılmış bir subnet hesaplayıcı ve ağ tarayıcısıdır.
CIDR notasyonundan ağ bilgilerini hesaplar ve bir alt ağdaki canlı hostları üç farklı yöntemle keşfeder.

> `murciélago` İspanyolca "yarasa" demektir — tıpkı yankı (echo) ile etrafını tarayan bir yarasa gibi.

---

## Özellikler

- **Subnet hesaplama** — network, broadcast, subnet mask, host aralığı ve host sayısı (`/31` ve `/32` özel durumları RFC 3021'e uygun).
- **Üç tarama yöntemi:**

  | Yöntem | Açıklama | Root gerekir mi? |
  |--------|----------|:----------------:|
  | `subprocess` | Sistem `ping` komutunu çağırır, çok-thread'li (ThreadPoolExecutor) | Hayır |
  | `icmp` | Ham (raw) socket ile elle üretilen ICMP echo paketleri | Evet |
  | `arp` | Scapy ile L2 seviyesinde ARP taraması (MAC adresleri) | Evet |

- **Platform bağımsız** `ping` çağrısı (macOS / Linux / Windows için doğru bayraklar).
- **Ayarlanabilir eşzamanlılık** — `max_workers` ve `timeout` parametreleri.

---

## Gereksinimler

- Python 3.8+
- [scapy](https://scapy.net/) (yalnızca `arp` taraması için)

```bash
pip install scapy
```

---

## Kullanım

```bash
python main.py --cidr <CIDR> [--scan <yöntem>]
```

| Argüman | Zorunlu | Açıklama |
|---------|:-------:|----------|
| `--cidr` | Evet | CIDR notasyonu, örn. `192.168.1.0/24` |
| `--scan` | Hayır | Tarama yöntemi: `subprocess`, `icmp` veya `arp` |

### Örnekler

Sadece subnet bilgisini hesapla:
```bash
python main.py --cidr 192.168.1.0/24
```

Subprocess ping ile tarama (root gerekmez):
```bash
python main.py --cidr 192.168.1.0/28 --scan subprocess
```

Ham ICMP veya ARP taraması (root/sudo gerekir):
```bash
sudo python main.py --cidr 192.168.1.0/28 --scan icmp
sudo python main.py --cidr 192.168.1.0/28 --scan arp
```

> `icmp` ve `arp` yöntemleri ham socket kullandığı için root yetkisi ister.
> Yetki yoksa program anlaşılır bir hata mesajı verip çıkar.

---

## Proje Yapısı

| Dosya | Görev |
|-------|-------|
| `main.py` | CLI arayüzü (argparse) |
| `subnet_calc.py` | CIDR / IP hesaplamaları (saf fonksiyonlar) |
| `ping_sweep.py` | Subprocess ve ICMP tabanlı host taraması |
| `icmp_ping.py` | ICMP paketi üretimi, checksum ve yanıt yakalama |
| `arp_scan.py` | Scapy ile ARP taraması |
| `benchmark.py` | Eşzamanlılık (worker sayısı) performans testi |

---

## Benchmark

### Eşzamanlılık Testi — 2026-08-08

Yerel bir `/28` alt ağı, `subprocess` tabanlı ping ile 200 ms sabit timeout kullanılarak tarandı.
Worker sayısı artırıldıkça tarama süresi yaklaşık 25 worker'a kadar belirgin şekilde düştü.

| Workers | Scan Time | Hosts Found |
|:-------:|:---------:|:-----------:|
| 1 | 15.826 s | 1 |
| 5 | 3.651 s | 2 |
| 10 | 2.440 s | 2 |
| 25 | **1.223 s** | 2 |
| 50 | 1.235 s | 2 |

**Bulgu:** Worker sayısını 1'den 25'e çıkarmak tarama süresini yaklaşık %92.3 azalttı (~12.9x hızlanma).
25'ten 50'ye çıkmak ek bir fayda sağlamadı, hatta çok az (~%1) daha yavaştı. Bu test ortamında performans
yaklaşık 25 eşzamanlı worker civarında platoya ulaştı.

> **Not:** Bu sonuçlar ortama bağımlıdır ve evrensel bir "optimal worker sayısı" olarak yorumlanmamalıdır.
> Test bir `/28` alt ağı ve 200 ms timeout ile yapılmıştır; daha büyük alt ağlar ve farklı ağ koşulları
> farklı sonuçlar üretebilir.

Testi kendin çalıştırmak için:
```bash
python benchmark.py
```

---

## Yasal Uyarı

Bu araç yalnızca sahibi olduğun veya taramak için açık izne sahip olduğun ağlarda kullanılmalıdır.
İzinsiz ağ taraması birçok ülkede yasa dışıdır. Sorumluluk kullanıcıya aittir.
