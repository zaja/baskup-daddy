# Značajke - Backup Daddy

## ✅ Implementirane Značajke (v1.0)

### 🎨 Korisničko Sučelje

- **Moderan GUI** sa CustomTkinter
- **Dark/Light Mode** podrška
- **Višejezično sučelje** (Hrvatski, English)
- **Responsive dizajn** sa prilagodljivim layoutom
- **Dashboard** sa statistikama i pregledom
- **Wizard-style editor** za kreiranje job-ova

### 📋 Upravljanje Job-ovima

- **CRUD operacije** (Create, Read, Update, Delete)
- **Više izvora** po job-u
- **Različite vrste backup-a**:
  - Potpuni (Full)
  - Inkrementalni (Incremental)
  - Diferencijalni (Differential)
- **Omogući/Onemogući** job-ove
- **JSON konfiguracija** za lako dijeljenje

### ⏰ Planiranje

- **Ručno pokretanje**
- **Dnevni backup** (određeno vrijeme)
- **Tjedno backup** (određeni dan i vrijeme)
- **Mjesečni backup** (određeni dan u mjesecu)
- **Interval-based** (svakih X minuta/sati/dana)
- **Automatski scheduler** u pozadini

### 🔍 Filtriranje

- **Include/Exclude ekstenzije**
- **Filtriranje po veličini** (min/max MB)
- **Exclude patterns** (wildcard podrška)
- **Pametno filtriranje** sistema i temp datoteka

### 💾 Backup Funkcionalnosti

- **ZIP kompresija** za uštedu prostora
- **Checksum validacija** (SHA-256)
- **Metadata tracking** za svaki backup
- **Progress tracking** sa real-time podacima:
  - Ukupni napredak (%)
  - Trenutna datoteka
  - Brzina prijenosa
  - Preostalo vrijeme
- **Error handling** sa detaljnim logovima

### 📊 Monitoring i Logovanje

- **Rotating log files** (automatsko čišćenje)
- **Različiti log nivoi** (DEBUG, INFO, WARNING, ERROR)
- **Timestamp tracking** za sve operacije
- **Error reporting** sa stack trace-ovima
- **Console i file logging**

### ⚙️ Konfiguracija

- **Globalne postavke** (jezik, tema, notifikacije)
- **Per-job konfiguracija**
- **Persistent storage** (JSON)
- **Import/Export** konfiguracija

### 🔧 Servis Mod

- **Dual-mode aplikacija** (GUI + Service)
- **Background scheduler** bez GUI-a
- **NSSM kompatibilnost** za Windows servis
- **Automatsko pokretanje** sa sistemom

## 🚧 Planirane Značajke (v2.0)

### 🔐 Sigurnost

- [ ] **AES šifriranje** backup-a
- [ ] **Password zaštita** arhiva
- [ ] **Secure deletion** starih backup-a
- [ ] **Access control** za job-ove

### 📸 Napredni Backup

- [ ] **VSS (Volume Shadow Copy)** podrška
- [ ] **Otvorene datoteke** backup
- [ ] **Delta kopiranje** (samo promijenjeni dijelovi)
- [ ] **Deduplication** za uštedu prostora
- [ ] **Bandwidth throttling** (ograničenje brzine)
- [ ] **Pause/Resume** funkcionalnost

### 🌐 Cloud Integracija

- [ ] **Google Drive** backup
- [ ] **OneDrive** backup
- [ ] **Backblaze B2** backup
- [ ] **Dropbox** backup
- [ ] **Custom S3** kompatibilni servisi

### 📡 Mrežne Funkcionalnosti

- [ ] **FTP/SFTP** podrška
- [ ] **WebDAV** podrška
- [ ] **Network share** optimizacije
- [ ] **Remote backup** na drugi računar

### 📧 Notifikacije

- [ ] **Email obavijesti** (SMTP)
- [ ] **Desktop notifikacije**
- [ ] **Sound alerts**
- [ ] **Webhook integracija**
- [ ] **Slack/Discord** notifikacije

### 📈 Izvještavanje

- [ ] **Dashboard grafikoni** (korištenje prostora, trendovi)
- [ ] **Backup statistike** (uspješnost, brzina)
- [ ] **Storage analytics** (najveće datoteke, duplikati)
- [ ] **PDF izvještaji** (dnevni, tjedno, mjesečni)
- [ ] **Email izvještaji**

### 🔄 Vraćanje Podataka

- [ ] **File browser** za backup arhive
- [ ] **Point-in-time recovery**
- [ ] **Selective restore** (odabir datoteka)
- [ ] **Restore preview** (pregled prije vraćanja)
- [ ] **Batch restore** (više verzija odjednom)

### 🗂️ Verzioniranje

- [ ] **Automatsko verzioniranje**
- [ ] **Retention policies** (čuvaj X verzija)
- [ ] **Grandfather-Father-Son** rotacija
- [ ] **Smart cleanup** (obriši najstarije)
- [ ] **Version comparison** (usporedi verzije)

### 🖥️ System Tray

- [ ] **Minimize to tray**
- [ ] **Tray ikona** sa statusom
- [ ] **Quick actions** iz tray-a
- [ ] **Progress u tray ikoni**

### 🔌 Ekstenzibilnost

- [ ] **Plugin sistem**
- [ ] **Pre/Post backup skripte**
- [ ] **Custom hooks**
- [ ] **REST API** za automaciju
- [ ] **CLI interface** za napredne korisnike

### 🏢 Enterprise Funkcionalnosti

- [ ] **Centralizirano upravljanje** (više računala)
- [ ] **Role-based access control**
- [ ] **Audit logging**
- [ ] **Compliance izvještaji**
- [ ] **Active Directory integracija**

### 🎯 Korisničko Iskustvo

- [ ] **Drag & drop** za dodavanje izvora
- [ ] **Quick setup wizard** za početnike
- [ ] **Templates** za česte scenarije
- [ ] **Backup profiles** (Work, Personal, etc.)
- [ ] **Dark/Light/Custom themes**
- [ ] **Keyboard shortcuts**

### 🧪 Testiranje i Validacija

- [ ] **Dry-run mode** (test bez izvršavanja)
- [ ] **Backup verification** (automatska provjera)
- [ ] **Test restore** (provjera integriteta)
- [ ] **Integrity checks** (periodične provjere)

## 🎁 Bonus Funkcionalnosti

### 📱 Mobile App (Budućnost)

- [ ] Android/iOS app za monitoring
- [ ] Push notifikacije
- [ ] Remote trigger backup-a
- [ ] View backup status

### 🤖 AI/ML Funkcionalnosti

- [ ] **Smart scheduling** (optimalno vrijeme za backup)
- [ ] **Predictive storage** (procjena potrebnog prostora)
- [ ] **Anomaly detection** (neobične promjene)
- [ ] **Auto-categorization** (automatsko grupiranje)

### 🔗 Integracije

- [ ] **Git integration** (backup repozitorija)
- [ ] **Database backup** (MySQL, PostgreSQL, MongoDB)
- [ ] **Docker volumes** backup
- [ ] **VM backup** (Hyper-V, VirtualBox)

## 📊 Performanse

### Trenutne Performanse

- **Brzina kopiranja**: Ovisi o disku (~100-500 MB/s)
- **Kompresija**: ~30-50% smanjenje veličine
- **CPU korištenje**: Nisko (5-15% tijekom backup-a)
- **RAM korištenje**: ~50-100 MB

### Planirane Optimizacije

- [ ] **Multithreading** za paralelno kopiranje
- [ ] **Async I/O** za bolje performanse
- [ ] **Incremental compression** (brža kompresija)
- [ ] **Memory-mapped files** za velike datoteke
- [ ] **Buffer optimization** za mrežne backup-e

## 🐛 Poznati Problemi

- Backup otvorenih datoteka nije podržan (dolazi VSS)
- Nema GUI progress za servis mod
- Email notifikacije nisu implementirane
- Restore funkcionalnost je osnovna

## 💡 Prijedlozi Dobrodošli

Imate ideju za novu značajku? Otvori issue ili pošalji pull request!

## 📅 Roadmap

- **v1.0** (Trenutno): Osnovne funkcionalnosti ✅
- **v1.5** (Q1 2025): VSS, Email notifikacije, Restore UI
- **v2.0** (Q2 2025): Cloud integracija, Šifriranje
- **v2.5** (Q3 2025): REST API, Plugin sistem
- **v3.0** (Q4 2025): Enterprise funkcionalnosti
