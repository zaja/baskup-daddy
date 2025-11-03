# Backup Daddy 💾

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)

**Tvoj pouzdani pomoćnik za automatsko backup-iranje podataka na Windows operativnom sistemu**

[Značajke](#-značajke) • [Instalacija](#-instalacija) • [Korištenje](#-korištenje) • [Dokumentacija](#-dokumentacija) • [Roadmap](#-roadmap)

</div>

---

## 🎯 Značajke

### 🎨 Korisničko Sučelje
- **Moderan GUI** sa CustomTkinter frameworkom
- **Dark/Light Mode** podrška sa sistemskom integracijom
- **Responsive dizajn** prilagođen različitim rezolucijama
- **Intuitivni dashboard** sa real-time statistikama
- **Wizard-style editor** za jednostavno kreiranje job-ova

### 🌍 Internacionalizacija
- **Višejezična podrška**: Hrvatski i English (lako proširivo)
- **Dinamička promjena jezika** bez restarta
- **Lokalizirani datumi i vremena**

### 📋 Upravljanje Job-ovima
- **CRUD operacije** (Create, Read, Update, Delete)
- **Više izvora** po jednom job-u
- **Različite vrste backup-a**:
  - 🔵 **Potpuni (Full)** - Kopira sve datoteke
  - 🟢 **Inkrementalni** - Samo promijenjene datoteke
  - 🟡 **Diferencijalni** - Promjene od zadnjeg potpunog backup-a
- **Omogući/Onemogući** job-ove bez brisanja
- **Import/Export** konfiguracija (JSON)

### ⏰ Automatsko Planiranje
- **Ručno pokretanje** - Pokreni kada želiš
- **Dnevni backup** - Svaki dan u određeno vrijeme
- **Tjedno backup** - Određeni dan u tjednu
- **Mjesečni backup** - Određeni dan u mjesecu
- **Interval-based** - Svakih X minuta/sati/dana
- **Background scheduler** - Radi u pozadini bez GUI-a

### 🔍 Napredni Filteri
- **Include/Exclude ekstenzije** - Odaberi koje tipove datoteka backup-irati
- **Filtriranje po veličini** - Min/Max veličina u MB
- **Exclude patterns** - Wildcard podrška za kompleksne filtere
- **Pametno filtriranje** - Automatski preskoči sistemske i temp datoteke

### 💾 Backup Funkcionalnosti
- **ZIP kompresija** - Uštedi 30-50% prostora
- **SHA-256 checksum** - Validacija integriteta
- **Metadata tracking** - Detaljan zapis svakog backup-a
- **Real-time progress**:
  - Ukupni napredak (%)
  - Trenutna datoteka
  - Brzina prijenosa (MB/s)
  - Preostalo vrijeme (ETA)
- **Error handling** - Detaljno logovanje grešaka

### 📊 Monitoring i Logovanje
- **Rotating log files** - Automatsko čišćenje (10 MB limit)
- **Različiti log nivoi** - DEBUG, INFO, WARNING, ERROR
- **Timestamp tracking** - Precizno praćenje svih operacija
- **Console i file logging** - Fleksibilno logovanje

### 🔧 Dual-Mode Aplikacija
- **GUI Mode** - Puno grafičko sučelje za interakciju
- **Service Mode** - Background scheduler bez GUI-a
- **NSSM kompatibilnost** - Instalacija kao Windows servis
- **Automatsko pokretanje** - Start sa Windows sistemom

---

## 🚀 Brza Instalacija

### Preduvjeti
- Python 3.8 ili noviji
- Windows 10/11
- pip (Python package manager)

### Metoda 1: Quick Start (Preporučeno)

**PowerShell:**
```powershell
.\quick_start.ps1
```

**CMD:**
```cmd
quick_start.bat
```

### Metoda 2: Ručna Instalacija

```bash
# 1. Kreiraj virtualno okruženje
python -m venv venv

# 2. Aktiviraj virtualno okruženje
# PowerShell:
.\venv\Scripts\Activate.ps1
# CMD:
.\venv\Scripts\activate.bat

# 3. Instaliraj dependencies
pip install -r requirements.txt

# 4. Testiraj instalaciju
python test_installation.py

# 5. Pokreni aplikaciju
python main.py
```

---

## 💻 Korištenje

### GUI Mod (Grafičko Sučelje)

```bash
python main.py
```

**Prvo pokretanje:**
1. Klikni **"+ New Job"**
2. Konfiguriraj job kroz 4 koraka:
   - **Basic**: Naziv, izvori, odredište, vrsta backup-a
   - **Schedule**: Kada se izvršava
   - **Filters**: Koje datoteke uključiti/isključiti
   - **Advanced**: Kompresija i druge opcije
3. Spremi job
4. Klikni **▶** za pokretanje ili čekaj automatsko izvršavanje

### Service Mod (Pozadinski Scheduler)

```bash
python main.py --service
```

Scheduler će automatski izvršavati planirane job-ove u pozadini.

### Instalacija kao Windows Servis

```powershell
# Preuzmi NSSM: https://nssm.cc/download
# Otvori PowerShell kao Administrator:

.\nssm.exe install BackupService "C:\path\to\venv\Scripts\python.exe" "C:\path\to\main.py --service"
.\nssm.exe start BackupService
```

Detaljne upute: [INSTALL.md](INSTALL.md)

---

## 📚 Dokumentacija

| Dokument | Opis |
|----------|------|
| [INSTALL.md](INSTALL.md) | Detaljne instalacijske upute |
| [USAGE.md](USAGE.md) | Upute za korištenje i best practices |
| [FEATURES.md](FEATURES.md) | Potpuna lista značajki i roadmap |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Arhitektura i struktura projekta |

---

## 📁 Struktura Projekta

```
Backup/
├── core/                      # Osnovna backup logika
│   ├── backup_engine.py       # Backup engine
│   ├── job_manager.py         # Upravljanje job-ovima
│   └── scheduler.py           # Automatsko planiranje
│
├── gui/                       # Grafičko sučelje
│   ├── main_window.py         # Glavni prozor
│   ├── job_editor.py          # Editor za job-ove
│   └── settings_window.py     # Postavke
│
├── utils/                     # Pomoćne funkcije
│   ├── i18n.py               # Višejezična podrška
│   ├── theme_manager.py      # Dark/Light mode
│   ├── config.py             # Konfiguracija
│   └── logger.py             # Logovanje
│
├── locales/                   # Prijevodi
│   ├── hr.json               # Hrvatski
│   └── en.json               # English
│
├── data/                      # Podaci (auto-kreirano)
│   ├── config.json           # Postavke
│   ├── jobs.json             # Job konfiguracije
│   └── logs/                 # Log datoteke
│
└── main.py                    # Entry point
```

---

## 🎨 Screenshots

### Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 JOBS     │ ⏱️ ACTIVE   │ 💾 STORAGE                      │
│    15       │    2        │   245 GB                         │
│ 12 ✓ 3 ⚠️   │ Running     │   Used                           │
└─────────────────────────────────────────────────────────────┘

📋 BACKUP JOBS                                    [+ New Job]
┌─────────────────────────────────────────────────────────────┐
│ Name          │ Status │ Last Run │ Next │ Actions          │
├─────────────────────────────────────────────────────────────┤
│ 📁 Documents  │ ✓ OK   │ 10:30   │ 22:00│ ▶️ ✏️ 🗑️          │
│ 💼 Work Files │ ⚠️ Warn│ 09:15   │ 18:00│ ▶️ ✏️ 🗑️          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗺️ Roadmap

### ✅ v1.0 (Trenutno)
- [x] Osnovni backup engine
- [x] GUI sa dark/light mode
- [x] Višejezična podrška
- [x] Automatsko planiranje
- [x] ZIP kompresija
- [x] Filtriranje datoteka
- [x] Logovanje i monitoring

### 🚧 v1.5 (Q1 2025)
- [ ] VSS (Volume Shadow Copy) podrška
- [ ] Email notifikacije
- [ ] Restore UI sa file browserom
- [ ] System tray integracija
- [ ] Pause/Resume funkcionalnost

### 🔮 v2.0 (Q2 2025)
- [ ] Cloud integracija (Google Drive, OneDrive, Backblaze B2)
- [ ] AES šifriranje backup-a
- [ ] FTP/SFTP podrška
- [ ] Dashboard grafikoni i statistike
- [ ] REST API za automaciju

### 🌟 v3.0 (Q4 2025)
- [ ] Plugin sistem
- [ ] Centralizirano upravljanje (više računala)
- [ ] Mobile app (Android/iOS)
- [ ] AI-powered smart scheduling

Potpuni roadmap: [FEATURES.md](FEATURES.md)

---

## 🤝 Contributing

Doprinosi su dobrodošli! Za doprinos projektu:

1. Fork repository
2. Kreiraj feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit promjene (`git commit -m 'Add some AmazingFeature'`)
4. Push na branch (`git push origin feature/AmazingFeature`)
5. Otvori Pull Request

---

## 📝 Licenca

Ovaj projekt je licenciran pod MIT licencom - vidi [LICENSE](LICENSE) file za detalje.

---

## 🙏 Acknowledgments

- **CustomTkinter** - Moderan GUI framework
- **Python Schedule** - Jednostavno planiranje
- **Python Community** - Za odličnu dokumentaciju i podršku

---

## 📞 Podrška

Imaš pitanje ili problem?

- 📖 Provjeri [dokumentaciju](USAGE.md)
- 🐛 Otvori [issue](https://github.com/yourusername/backup-manager/issues)
- 💬 Kontaktiraj developera

---

<div align="center">

**Napravljeno s ❤️ za Windows korisnike**

⭐ Ako ti se sviđa projekt, daj mu zvjezdicu!

</div>
