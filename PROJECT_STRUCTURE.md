# Struktura Projekta - Backup Daddy

## 📁 Pregled Direktorija

```
Backup/
├── core/                      # Osnovna backup logika
│   ├── __init__.py
│   ├── backup_engine.py       # Backup engine (kopiranje, kompresija)
│   ├── job_manager.py         # Upravljanje job-ovima
│   └── scheduler.py           # Automatsko planiranje
│
├── gui/                       # Grafičko sučelje
│   ├── __init__.py
│   ├── main_window.py         # Glavni prozor (dashboard)
│   ├── job_editor.py          # Editor za job-ove (wizard)
│   └── settings_window.py     # Postavke aplikacije
│
├── utils/                     # Pomoćne funkcije
│   ├── __init__.py
│   ├── i18n.py               # Višejezična podrška
│   ├── theme_manager.py      # Dark/Light mode
│   ├── config.py             # Konfiguracija
│   └── logger.py             # Logovanje
│
├── locales/                   # Prijevodi
│   ├── hr.json               # Hrvatski
│   └── en.json               # English
│
├── data/                      # Podaci aplikacije (auto-kreirano)
│   ├── .gitkeep
│   ├── config.json           # Postavke (auto-kreirano)
│   ├── jobs.json             # Job konfiguracije (auto-kreirano)
│   └── logs/                 # Log datoteke (auto-kreirano)
│
├── main.py                    # Entry point aplikacije
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore file
│
├── README.md                  # Pregled projekta
├── INSTALL.md                # Instalacijske upute
├── USAGE.md                  # Upute za korištenje
├── FEATURES.md               # Lista značajki
├── PROJECT_STRUCTURE.md      # Ovaj file
│
├── test_installation.py      # Test skripta
├── quick_start.bat           # Brzo pokretanje (CMD)
└── quick_start.ps1           # Brzo pokretanje (PowerShell)
```

## 📄 Opis Ključnih Datoteka

### Core Moduli

#### `core/backup_engine.py`
- **BackupEngine**: Glavna klasa za backup operacije
- **BackupProgress**: Praćenje napretka backup-a
- Funkcionalnosti:
  - Kopiranje datoteka
  - ZIP kompresija
  - Filtriranje datoteka
  - Checksum validacija (SHA-256)
  - Progress tracking

#### `core/job_manager.py`
- **BackupJob**: Model za backup job
- **JobManager**: Upravljanje svim job-ovima
- Funkcionalnosti:
  - CRUD operacije
  - JSON persistence
  - Job validacija
  - Status tracking

#### `core/scheduler.py`
- **BackupScheduler**: Automatsko planiranje
- Funkcionalnosti:
  - Dnevno/Tjedno/Mjesečno planiranje
  - Interval-based scheduling
  - Background execution
  - Job callbacks

### GUI Moduli

#### `gui/main_window.py`
- **MainWindow**: Glavni prozor aplikacije
- **DashboardCard**: Statistika kartice
- **JobRow**: Red u tablici job-ova
- Funkcionalnosti:
  - Dashboard sa statistikama
  - Lista job-ova
  - Menu bar
  - Job akcije (run, edit, delete)

#### `gui/job_editor.py`
- **JobEditorWindow**: Wizard za kreiranje/uređivanje job-ova
- 4 koraka:
  1. Osnovne postavke
  2. Raspored
  3. Filteri
  4. Napredne opcije
- Validacija unosa

#### `gui/settings_window.py`
- **SettingsWindow**: Postavke aplikacije
- Sekcije:
  - Općenito (jezik, tema)
  - Obavijesti
  - Pokretanje

### Utils Moduli

#### `utils/i18n.py`
- **I18n**: Višejezična podrška
- Funkcionalnosti:
  - Učitavanje prijevoda iz JSON-a
  - Dot notation pristup (`dashboard.title`)
  - Dinamička promjena jezika
  - Globalna `t()` funkcija

#### `utils/theme_manager.py`
- **ThemeManager**: Upravljanje temama
- Funkcionalnosti:
  - Dark/Light/System mode
  - Preddefinirane boje
  - Status boje
  - Dinamička promjena

#### `utils/config.py`
- **Config**: Konfiguracija aplikacije
- Funkcionalnosti:
  - JSON persistence
  - Default vrijednosti
  - Get/Set operacije
  - Auto-save

#### `utils/logger.py`
- **BackupLogger**: Logovanje
- Funkcionalnosti:
  - Rotating file handler (10 MB)
  - Console output
  - Različiti nivoi (DEBUG, INFO, WARNING, ERROR)
  - Timestamp tracking

### Locale Files

#### `locales/hr.json` & `locales/en.json`
- Struktura:
  ```json
  {
    "app_title": "...",
    "dashboard": { ... },
    "job_editor": { ... },
    "settings": { ... },
    "common": { ... }
  }
  ```

## 🔄 Data Flow

### 1. Pokretanje Aplikacije

```
main.py
  ↓
run_gui_mode() ili run_service_mode()
  ↓
Inicijalizacija komponenti:
  - I18n (prijevodi)
  - ThemeManager (tema)
  - Config (postavke)
  - Logger (logovanje)
  - JobManager (job-ovi)
  - Scheduler (planiranje)
```

### 2. Kreiranje Job-a

```
User klikne "New Job"
  ↓
JobEditorWindow otvoren
  ↓
User unosi podatke kroz 4 koraka
  ↓
Validacija unosa
  ↓
BackupJob kreiran
  ↓
JobManager.create_job()
  ↓
Spremanje u jobs.json
  ↓
Scheduler.refresh_schedules()
```

### 3. Izvršavanje Backup-a

```
Scheduler ili Manual trigger
  ↓
BackupScheduler._execute_backup_job()
  ↓
Job status → "running"
  ↓
BackupEngine.perform_backup()
  ├─ Kalkulacija veličine
  ├─ Filtriranje datoteka
  ├─ Kopiranje/Kompresija
  ├─ Progress tracking
  └─ Checksum validacija
  ↓
Spremanje metadata
  ↓
Job status → "completed" ili "failed"
  ↓
Callback notifikacije
```

## 🎯 Design Patterns

### Singleton Pattern
- `get_i18n()` - Globalna i18n instanca
- `get_theme_manager()` - Globalna theme instanca
- `get_config()` - Globalna config instanca
- `get_logger()` - Globalna logger instanca
- `get_job_manager()` - Globalna job manager instanca

### Observer Pattern
- Scheduler callbacks:
  - `on_job_start`
  - `on_job_complete`
  - `on_job_error`

### Strategy Pattern
- Backup types: Full, Incremental, Differential
- Schedule types: Manual, Daily, Weekly, Monthly, Interval

### Factory Pattern
- `BackupJob.from_dict()` - Kreiranje job-a iz dictionary-a

## 🔌 Extensibility Points

### 1. Dodavanje Novog Jezika

```python
# 1. Kreiraj locales/de.json
# 2. Dodaj u i18n.py:
def get_available_languages(self):
    return {
        "hr": "Hrvatski",
        "en": "English",
        "de": "Deutsch"  # Novo
    }
```

### 2. Dodavanje Nove Vrste Backup-a

```python
# U backup_engine.py:
def perform_backup(self, ..., backup_type="full"):
    if backup_type == "full":
        # ...
    elif backup_type == "incremental":
        # ...
    elif backup_type == "custom":  # Novo
        # Implementacija
```

### 3. Dodavanje Novog Filtera

```python
# U backup_engine.py:
def _should_include_file(self, file_path, filters):
    # Postojeći filteri
    # ...
    
    # Novi filter
    if filters.get("custom_filter"):
        # Implementacija
```

### 4. Dodavanje Nove Notifikacije

```python
# Kreiraj utils/notifier.py
class Notifier:
    def send_email(self, ...):
        pass
    
    def send_slack(self, ...):  # Novo
        pass
```

## 📊 Dependencies

### Production
- **customtkinter**: Moderan GUI framework
- **Pillow**: Image processing (za CustomTkinter)
- **schedule**: Job scheduling
- **python-dotenv**: Environment variables
- **psutil**: System utilities
- **py7zr**: 7z compression (za budućnost)
- **cryptography**: Šifriranje (za budućnost)

### Development (Opciono)
- **pytest**: Unit testing
- **black**: Code formatting
- **pylint**: Code linting
- **mypy**: Type checking

## 🧪 Testing Strategy

### Unit Tests (Planirano)
```
tests/
├── test_backup_engine.py
├── test_job_manager.py
├── test_scheduler.py
├── test_i18n.py
└── test_config.py
```

### Integration Tests (Planirano)
```
tests/integration/
├── test_full_backup.py
├── test_incremental_backup.py
└── test_scheduler_execution.py
```

## 📈 Performance Considerations

### Memory Usage
- Job manager: ~1 MB po 100 job-ova
- Logger: ~10 MB max (rotating)
- Config: ~1 KB
- GUI: ~50-100 MB

### Disk Usage
- Aplikacija: ~5 MB
- Dependencies: ~100 MB
- Logs: ~10 MB (rotating)
- Backups: Ovisi o podacima

### CPU Usage
- Idle: ~0-1%
- Backup: ~5-15%
- Compression: ~20-40%

## 🔒 Security Considerations

### Trenutno
- Config i jobs spremljeni u plain text JSON
- Nema šifriranja backup-a
- Nema autentifikacije

### Planirano (v2.0)
- AES šifriranje backup-a
- Password zaštita konfiguracije
- Secure storage za credentials
- Access control

## 🚀 Deployment

### Standalone Executable (Planirano)
```bash
# PyInstaller
pyinstaller --onefile --windowed main.py
```

### Windows Installer (Planirano)
```bash
# Inno Setup ili NSIS
```

## 📝 Coding Standards

- **PEP 8** style guide
- **Type hints** gdje je moguće
- **Docstrings** za sve javne funkcije
- **Comments** za kompleksnu logiku
- **Error handling** sa try/except
- **Logging** umjesto print statements

## 🤝 Contributing

Za doprinos projektu:
1. Fork repository
2. Kreiraj feature branch
3. Commit promjene
4. Push na branch
5. Otvori Pull Request

## 📞 Support

Za pitanja i probleme:
- Provjeri dokumentaciju
- Provjeri log datoteke
- Otvori issue na projektu
