# Changelog

Sve značajne promjene u projektu bit će dokumentirane u ovom file-u.

Format baziran na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt slijedi [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-03

### 🎉 Inicijalni Release

#### Added
- **Core Backup Engine**
  - Potpuni (Full) backup
  - Inkrementalni backup
  - Diferencijalni backup
  - ZIP kompresija
  - SHA-256 checksum validacija
  - Real-time progress tracking
  - Error handling i recovery

- **Job Manager**
  - CRUD operacije za job-ove
  - JSON persistence
  - Više izvora po job-u
  - Omogući/Onemogući job-ove
  - Job status tracking

- **Scheduler**
  - Ručno pokretanje
  - Dnevno planiranje
  - Tjedno planiranje
  - Mjesečno planiranje
  - Interval-based planiranje
  - Background execution
  - Job callbacks

- **GUI (Grafičko Sučelje)**
  - Moderan dashboard sa statistikama
  - Lista job-ova sa akcijama
  - Wizard-style job editor (4 koraka)
  - Settings prozor
  - Dark/Light mode podrška
  - Responsive dizajn

- **Internacionalizacija**
  - Hrvatski jezik
  - English jezik
  - Dinamička promjena jezika
  - JSON-based prijevodi

- **Filtriranje**
  - Include/Exclude ekstenzije
  - Min/Max veličina datoteka
  - Exclude patterns

- **Monitoring i Logovanje**
  - Rotating log files (10 MB limit)
  - Console i file logging
  - Različiti log nivoi (DEBUG, INFO, WARNING, ERROR)
  - Timestamp tracking

- **Konfiguracija**
  - Globalne postavke
  - Per-job konfiguracija
  - JSON persistence
  - Default vrijednosti

- **Dual-Mode**
  - GUI mode za interakciju
  - Service mode za background scheduler
  - NSSM kompatibilnost

- **Dokumentacija**
  - README.md - Pregled projekta
  - INSTALL.md - Instalacijske upute
  - USAGE.md - Upute za korištenje
  - FEATURES.md - Lista značajki i roadmap
  - PROJECT_STRUCTURE.md - Arhitektura projekta
  - CHANGELOG.md - Povijest promjena

- **Pomoćne Skripte**
  - test_installation.py - Test skripta
  - quick_start.bat - Brzo pokretanje (CMD)
  - quick_start.ps1 - Brzo pokretanje (PowerShell)

#### Technical Details
- Python 3.8+ kompatibilnost
- CustomTkinter za GUI
- Schedule library za planiranje
- Pillow za image processing
- psutil za system utilities
- py7zr za 7z compression (priprema)
- cryptography za encryption (priprema)

#### Known Issues
- Backup otvorenih datoteka nije podržan (VSS dolazi u v1.5)
- Email notifikacije nisu implementirane (dolazi u v1.5)
- Restore funkcionalnost je osnovna (poboljšanje u v1.5)
- System tray integracija nije implementirana (dolazi u v1.5)

---

## [Unreleased]

### Planned for v1.5 (Q1 2025)
- VSS (Volume Shadow Copy) podrška
- Email notifikacije (SMTP)
- Napredni Restore UI sa file browserom
- System tray integracija
- Pause/Resume funkcionalnost
- Desktop notifikacije
- Sound alerts

### Planned for v2.0 (Q2 2025)
- Cloud integracija (Google Drive, OneDrive, Backblaze B2)
- AES šifriranje backup-a
- FTP/SFTP podrška
- Dashboard grafikoni i statistike
- REST API za automaciju
- Webhook integracija

### Planned for v2.5 (Q3 2025)
- Plugin sistem
- Pre/Post backup skripte
- Custom hooks
- CLI interface
- Bandwidth throttling
- Delta kopiranje

### Planned for v3.0 (Q4 2025)
- Centralizirano upravljanje (više računala)
- Role-based access control
- Active Directory integracija
- Mobile app (Android/iOS)
- AI-powered smart scheduling

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-11-03 | Inicijalni release sa osnovnim funkcionalnostima |

---

## Upgrade Guide

### From 0.x to 1.0.0
Ovo je prvi stabilni release, nema upgrade procedure.

---

## Breaking Changes

Nema breaking changes u ovoj verziji.

---

## Deprecations

Nema deprecation-a u ovoj verziji.

---

## Contributors

- Glavni Developer - Inicijalni razvoj

---

## Support

Za pitanja o promjenama ili upgrade-u:
- Provjeri [dokumentaciju](README.md)
- Otvori [issue](https://github.com/yourusername/backup-manager/issues)
- Kontaktiraj support
