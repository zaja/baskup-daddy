# Upute za Korištenje - Backup Daddy

## Pregled Sučelja

### Dashboard (Glavna Stranica)

Dashboard prikazuje:
- **Statistike**: Broj job-ova, aktivni backup-i, iskorištena pohrana
- **Nedavne aktivnosti**: Povijest izvršavanja
- **Lista job-ova**: Svi konfigurirani backup job-ovi

## Kreiranje Backup Job-a

### Korak 1: Osnovne Postavke

1. Klikni **"+ New Job"**
2. Unesi:
   - **Naziv job-a**: Opisno ime (npr. "Documents Backup")
   - **Opis**: Opcioni detaljan opis
   - **Izvorni folderi**: Klikni "Add Source" i odaberi foldere za backup
   - **Odredište**: Gdje će se čuvati backup (lokalni disk, eksterni disk, mrežni disk)
   - **Vrsta backupa**:
     - **Potpuni (Full)**: Kopira sve datoteke svaki put
     - **Inkrementalni**: Kopira samo promijenjene datoteke od zadnjeg backup-a
     - **Diferencijalni**: Kopira promijenjene datoteke od zadnjeg potpunog backup-a

### Korak 2: Raspored

Odaberi kada će se backup izvršavati:

- **Manual**: Samo ručno pokretanje
- **Daily**: Svaki dan u određeno vrijeme (npr. 22:00)
- **Weekly**: Jednom tjedno (odaberi dan i vrijeme)
- **Monthly**: Jednom mjesečno (odaberi dan u mjesecu i vrijeme)

### Korak 3: Filteri

Definiraj koje datoteke uključiti/isključiti:

- **Include Extensions**: Samo određene ekstenzije (npr. `pdf,docx,xlsx`)
- **Exclude Extensions**: Isključi ekstenzije (npr. `tmp,log,cache`)
- **Min/Max Size**: Filtriraj po veličini datoteka (u MB)

### Korak 4: Napredne Opcije

- **Compression**: Kompresija u ZIP format (preporučeno - štedi prostor)
- **Encryption**: Šifriranje (dolazi uskoro)
- **Job Enabled**: Da li je job aktivan

## Izvršavanje Backup-a

### Ručno Pokretanje

1. Na dashboard-u, pronađi job
2. Klikni **▶ (Play)** gumb
3. Backup će se pokrenuti odmah

### Automatsko Izvršavanje

- Job-ovi sa definiranim rasporedom izvršavaju se automatski
- Scheduler mora biti pokrenut (automatski u GUI modu)
- Za pozadinski rad bez GUI-a: `python main.py --service`

## Praćenje Napretka

Tijekom backup-a prikazuje se:
- Ukupni napredak (%)
- Trenutna datoteka
- Brzina prijenosa (MB/s)
- Preostalo vrijeme
- Lista obrađenih datoteka

Opcije:
- **Pause**: Privremeno zaustavi backup
- **Stop**: Potpuno prekini backup
- **Minimize**: Minimiziraj prozor (backup nastavlja u pozadini)

## Vraćanje Podataka (Restore)

### Pregled Povijesti

1. Odaberi job
2. Klikni **"View"** ili idi na **View → History**
3. Prikazuju se sve verzije backup-a sa:
   - Datum i vrijeme
   - Veličina
   - Broj datoteka
   - Status (uspješno/neuspješno)

### Vraćanje Datoteka

1. Odaberi verziju backup-a
2. Klikni **"Restore"**
3. Pregledaj datoteke u backup-u
4. Odaberi datoteke za vraćanje
5. Odaberi odredište:
   - **Original Location**: Vrati na izvorno mjesto
   - **Custom Location**: Odaberi drugo mjesto
6. Odaberi akciju ako datoteka postoji:
   - **Ask**: Pitaj za svaku datoteku
   - **Overwrite**: Prepiši postojeću
   - **Keep Both**: Zadrži obje verzije
   - **Skip**: Preskoči
7. Klikni **"Restore"**

## Upravljanje Job-ovima

### Uređivanje Job-a

1. Klikni **✏ (Edit)** gumb na job-u
2. Izmijeni postavke
3. Spremi promjene

### Brisanje Job-a

1. Klikni **🗑 (Delete)** gumb
2. Potvrdi brisanje
3. **Napomena**: Postojeći backup-i NEĆE biti obrisani

### Omogući/Onemogući Job

1. Uredi job
2. Promijeni "Job Enabled" opciju
3. Onemogućeni job-ovi se neće automatski izvršavati

## Postavke Aplikacije

### Jezik

Promijeni jezik sučelja:
- Hrvatski
- English

### Tema

Odaberi izgled:
- **Light**: Svijetla tema
- **Dark**: Tamna tema (preporučeno)
- **System**: Prati sistemske postavke

### Obavijesti

- **Email Notifications**: Primi email nakon završetka backup-a
- **Sound Notifications**: Zvučna obavijest

### Pokretanje

- **Start with Windows**: Automatski pokreni sa sistemom
- **Start Minimized**: Pokreni minimizirano u system tray

## Logovi i Dijagnostika

### Pregled Logova

Logovi se čuvaju u: `data/logs/backup_YYYYMMDD.log`

Sadrže:
- Vrijeme svake operacije
- Uspješna izvršavanja
- Greške i upozorenja
- Detalje o datotekama

### Čitanje Logova

```
2024-11-03 10:30:12 - BackupApp - INFO - Starting backup job: Documents
2024-11-03 10:30:15 - BackupApp - INFO - Processed 150 files (1.2 GB)
2024-11-03 10:35:45 - BackupApp - INFO - Backup completed successfully
```

## Best Practices

### 1. Redoviti Backup-i

- Postavi automatski raspored
- Kritični podaci: dnevno
- Ostali podaci: tjedno

### 2. 3-2-1 Pravilo

- **3** kopije podataka
- **2** različita medija (lokalni + eksterni disk)
- **1** off-site kopija (cloud, drugi lokacija)

### 3. Testiranje Restore-a

- Povremeno testiraj vraćanje podataka
- Provjeri integritet backup-a

### 4. Praćenje Prostora

- Redovito provjeri iskorištenu pohranu
- Postavi politiku čišćenja starih backup-a

### 5. Šifriranje Osjetljivih Podataka

- Koristi šifriranje za osjetljive podatke
- Čuvaj lozinke na sigurnom mjestu

## Česta Pitanja (FAQ)

### Koliko prostora trebam?

- Potpuni backup: Jednako kao izvorni podaci
- Inkrementalni: Samo promjene (mnogo manje)
- Sa kompresijom: ~30-50% manje

### Mogu li backup-irati na mrežni disk?

Da, odaberi mrežnu lokaciju kao odredište (npr. `\\server\backup`).

### Što ako je računalo ugašeno u vrijeme backup-a?

Backup će se izvršiti pri sljedećem pokretanju ako je scheduler aktivan.

### Mogu li backup-irati otvorene datoteke?

Trenutno ne. VSS (Volume Shadow Copy) podrška dolazi u budućoj verziji.

### Kako obrisati stare backup-e?

Ručno obriši foldere/arhive u odredišnom direktoriju. Automatsko čišćenje dolazi uskoro.

## Napredne Funkcionalnosti

### Pokretanje kao Servis

Za automatski rad u pozadini bez GUI-a:

```bash
python main.py --service
```

Ili instaliraj kao Windows servis sa NSSM (vidi INSTALL.md).

### Backup na Cloud

Dolazi uskoro:
- Google Drive
- Backblaze B2
- OneDrive

### FTP/SFTP Podrška

Dolazi uskoro - backup na remote servere.

## Podrška

Za dodatnu pomoć:
- Provjeri log datoteke
- Kontaktiraj support
- Otvori issue na projektu
