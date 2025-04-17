# 🔹 SRO:SH – Server Hub

A lightweight, efficient background service for **Silkroad Online private server administrators**.\
Part of the **SRO:Server Browser System**, SRO:SH enables private servers to sync metadata with a centralized hub and optionally interface with SQL databases for remote account creation.

> ⚙️ Designed to run on low-end hardware (e.g., alongside server software on minimal systems)\
> 🌐 Seamlessly integrates with the SRO:SB ecosystem for server discoverability

---

## 📖 Overview

SRO:SH (Server Hub) is a companion service for SilkSilkroad Online private servers. It:

- Reads server details from simple `.ini` configuration files
- Periodically sends server metadata (e.g., player count, ping, settings) to the SRO:SB hub
- Supports SQL database integration for remote account management
- Ensures minimal resource usage, making it ideal for running alongside server software

This service empowers server administrators to make their servers discoverable to players through the **SRO:SB Server Browser** while maintaining full control over their server’s configuration.

---

## 🌟 Features

- **Lightweight**: Runs efficiently with minimal CPU and memory usage
- **Configurable**: Reads server settings from `config.ini` and SQL credentials from `special_config.ini`
- **Asynchronous Communication**: Uses TCP and JSON payloads for reliable, non-blocking hub communication
- **SQL Integration**: Connects to SQL Server databases (via `pyodbc`) for account management
- **Modular Design**: Easily extendable for custom message types and integrations
- **Colorful Logging**: Provides clear, color-coded terminal output for debugging

---

## 🛠️ Technical Details

- **Language**: Python 3.10+ with `asyncio` for non-blocking I/O
- **Dependencies**: `aiohttp`, `requests`, `ping3`, `pyodbc`
- **Communication**: TCP-based JSON messaging with the SRO:SB hub
- **Database**: Supports SQL Server via ODBC (configurable via `special_config.ini`)
- **Platform**: Windows, Linux, or any system with Python support

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- SQL Server ODBC driver (e.g., ODBC Driver 17 for SQL Server)
- Git (optional, for cloning the repository)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kantrveysel/sro-server-hub.git
   cd sro-server-hub
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**:

   - Copy `src/config.ini.example` to `src/config.ini` and update with your server details.

   - Copy `src/special_config.ini.example` to `src/special_config.ini` and add your SQL credentials.

   - Example `config.ini`:

     ```ini
     [HUB]
     port=8888
     
     [settings]
     server_name=MyServer
     max_players=1000
     
     [info]
     name=MySROServer
     version=1.0
     ```

   - Example `special_config.ini`:

     ```ini
     [SQL]
     driver=SQL Server
     database=SRO_VT_ACCOUNT
     host=localhost
     uuid=sa
     pwd=your_password
     ```

4. **Run the Service**:

   ```bash
   cd src
   python main.py
   ```

---

## 🚀 Usage

- **Starting the Service**: Run `python main.py` from the `src` directory. The service will connect to the SRO:SB hub and start syncing server metadata.
- **Monitoring**: Check the color-coded terminal output or `logs/server_hub.log` for status updates and errors.
- **Extending**: Add custom message handlers in `src/core/hub_client.py` to support new hub interactions (e.g., custom player events).

For detailed usage, refer to the **SRO:Server Browser System documentation**.

---

## 🧪 Status

SRO:SH is fully functional for core features:

- Hub communication and metadata syncing
- SQL integration for account management
- Modular message handling

Future enhancements include:

- Advanced message types for player interactions
- GUI-based configuration tool
- Enhanced security for SQL credentials

---

## 🤝 Contributing

Contributions are welcome! You can help with:

- Bug fixes and performance improvements
- New message types for hub communication
- Documentation and localization
- Testing on diverse server setups

Please read the **SRO:SB Contributing Guide** for details.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🙌 Acknowledgments

- Built as part of the **SRO:Server Browser System**
- Made with ❤️ for the Silkroad Online private server community
- Special thanks to all contributors and testers!

---

# 🇹🇷 SRO:SH – Sunucu Merkezi

**Silkroad Online özel sunucu yöneticileri** için hafif ve verimli bir arka plan servisi.\
**SRO:Sunucu Tarayıcı Sistemi**’nin bir parçası olan SRO:SH, özel sunucuların merkezi bir hub ile meta veri senkronizasyonu yapmasını sağlar ve isteğe bağlı olarak SQL veritabanlarıyla uzaktan hesap yönetimi için entegrasyon sunar.

> ⚙️ Düşük donanımlı sistemlerde (örneğin, sunucu yazılımıyla birlikte minimal sistemlerde) çalışacak şekilde tasarlandı\
> 🌐 Sunucu keşfedilebilirliği için SRO:SB ekosistemiyle sorunsuz entegrasyon

---

## 📖 Genel Bakış

SRO:SH (Sunucu Merkezi), Silkroad Online özel sunucuları için bir yardımcı servistir. Şunları yapar:

- Basit `.ini` yapılandırma dosyalarından sunucu detaylarını okur
- Sunucu meta verilerini (örneğin, oyuncu sayısı, ping, ayarlar) periyodik olarak SRO:SB hub’ına gönderir
- Uzaktan hesap yönetimi için SQL veritabanı entegrasyonu sağlar
- Minimum kaynak kullanımıyla sunucu yazılımıyla birlikte çalışır

Bu servis, sunucu yöneticilerinin sunucularını **SRO:SB Sunucu Tarayıcı** aracılığıyla oyunculara görünür hale getirmesini sağlar ve sunucu yapılandırması üzerinde tam kontrol sunar.

---

## 🌟 Özellikler

- **Hafif**: Minimum CPU ve bellek kullanımıyla çalışır
- **Yapılandırılabilir**: Sunucu ayarlarını `config.ini` ve SQL kimlik bilgilerini `special_config.ini`’den okur
- **Asenkron İletişim**: Güvenilir, bloklamayan hub iletişimi için TCP ve JSON paketleri kullanır
- **SQL Entegrasyonu**: Hesap yönetimi için SQL Server veritabanlarına bağlanır (`pyodbc` ile)
- **Modüler Tasarım**: Özel mesaj türleri ve entegrasyonlar için kolayca genişletilebilir
- **Renkli Loglama**: Hata ayıklama için net, renk kodlu terminal çıktıları sunar

---

## 🛠️ Teknik Detaylar

- **Dil**: Python 3.10+ ve `asyncio` ile bloklamayan I/O
- **Bağımlılıklar**: `aiohttp`, `requests`, `ping3`, `pyodbc`
- **İletişim**: SRO:SB hub’ı ile TCP tabanlı JSON mesajlaşma
- **Veritabanı**: ODBC üzerinden SQL Server desteği (`special_config.ini` ile yapılandırılabilir)
- **Platform**: Windows, Linux veya Python destekleyen herhangi bir sistem

---

## 📦 Kurulum

### Gereksinimler

- Python 3.10 veya üstü
- SQL Server ODBC sürücüsü (örneğin, ODBC Driver 17 for SQL Server)
- Git (opsiyonel, depoyu klonlamak için)

### Adımlar

1. **Depoyu Klonlayın**:

   ```bash
   git clone https://github.com/kantrveysel/sro-server-hub.git
   cd sro-server-hub
   ```

2. **Bağımlılıkları Yükleyin**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ayarları Yapılandırın**:

   - `src/config.ini.example` dosyasını `src/config.ini` olarak kopyalayın ve sunucu detaylarınızı güncelleyin.

   - `src/special_config.ini.example` dosyasını `src/special_config.ini` olarak kopyalayın ve SQL kimlik bilgilerinizi ekleyin.

   - Örnek `config.ini`:

     ```ini
     [HUB]
     port=8888
     
     [settings]
     server_name=MyServer
     max_players=1000
     
     [info]
     name=MySROServer
     version=1.0
     ```

   - Örnek `special_config.ini`:

     ```ini
     [SQL]
     driver=SQL Server
     database=SRO_VT_ACCOUNT
     host=localhost
     uuid=sa
     pwd=your_password
     ```

4. **Servisi Çalıştırın**:

   ```bash
   cd src
   python main.py
   ```

---

## 🚀 Kullanım

- **Servisi Başlatma**: `src` dizininden `python main.py` komutunu çalıştırın. Servis, SRO:SB hub’ına bağlanacak ve sunucu meta verilerini senkronize etmeye başlayacak.
- **İzleme**: Durum güncellemeleri ve hatalar için renk kodlu terminal çıktılarını veya `logs/server_hub.log` dosyasını kontrol edin.
- **Genişletme**: Yeni hub etkileşimleri (örneğin, özel oyuncu etkinlikleri) için `src/core/hub_client.py`’ye özel mesaj işleyiciler ekleyin.

Ayrıntılı kullanım için **SRO:Sunucu Tarayıcı Sistemi dokümantasyonuna** bakın.

---

## 🧪 Geliştirme Durumu

SRO:SH, temel özellikleriyle tamamen işlevseldir:

- Hub iletişimi ve meta veri senkronizasyonu
- Hesap yönetimi için SQL entegrasyonu
- Modüler mesaj işleme

Gelecekteki geliştirmeler:

- Oyuncu etkileşimleri için gelişmiş mesaj türleri
- Grafik arayüz tabanlı yapılandırma aracı
- SQL kimlik bilgileri için gelişmiş güvenlik

---

## 🤝 Katkı Sağlayın

Katkılarınızı bekliyoruz! Şu alanlarda yardımcı olabilirsiniz:

- Hata düzeltmeleri ve performans iyileştirmeleri
- Hub iletişimi için yeni mesaj türleri
- Dokümantasyon ve çeviri
- Farklı sunucu kurulumlarında testler

Detaylar için **SRO:SB Katkı Rehberi**’ni okuyun.

---

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

---

## 🙌 Teşekkürler

- **SRO:Sunucu Tarayıcı Sistemi**’nin bir parçası olarak geliştirildi
- Silkroad Online özel sunucu topluluğu için ❤️ ile yapıldı
- Tüm katkıda bulunanlara ve test edenlere özel teşekkürler!
