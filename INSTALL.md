# Instalacijske Upute - Backup Daddy

## Preduvjeti

- Python 3.8 ili noviji
- Windows 10/11
- pip (Python package manager)

## Instalacija

### 1. Kloniraj/preuzmi projekt

```bash
cd C:\Users\Zaja\Desktop\Backup
```

### 2. Kreiraj virtualno okruženje (preporučeno)

```bash
python -m venv venv
```

### 3. Aktiviraj virtualno okruženje

```bash
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
.\venv\Scripts\activate.bat
```

### 4. Instaliraj dependencies

```bash
pip install -r requirements.txt
```

## Pokretanje

### GUI Mod (Grafičko sučelje)

```bash
python main.py
```

### Servis Mod (Pozadinski scheduler)

```bash
python main.py --service
```

## Instalacija kao Windows Servis (Opciono)

### Korištenje NSSM (Non-Sucking Service Manager)

1. Preuzmi NSSM: https://nssm.cc/download
2. Ekstraktuj i kopiraj `nssm.exe` u projekt folder
3. Otvori PowerShell kao Administrator:

```powershell
# Instaliraj servis
.\nssm.exe install BackupDaddyService "C:\Users\Zaja\Desktop\Backup\venv\Scripts\python.exe" "C:\Users\Zaja\Desktop\Backup\main.py --service"

# Postavi radni direktorij
.\nssm.exe set BackupDaddyService AppDirectory "C:\Users\Zaja\Desktop\Backup"

# Postavi opis
.\nssm.exe set BackupDaddyService Description "Backup Daddy Service"

# Pokreni servis
.\nssm.exe start BackupDaddyService
```

### Upravljanje servisom

```powershell
# Status
.\nssm.exe status BackupDaddyService

# Zaustavi
.\nssm.exe stop BackupDaddyService

# Restart
.\nssm.exe restart BackupDaddyService

# Ukloni servis
.\nssm.exe remove BackupDaddyService confirm
```

## Konfiguracija

Aplikacija automatski kreira `data/` direktorij sa sljedećim datotekama:

- `config.json` - Postavke aplikacije
- `jobs.json` - Backup job konfiguracije
- `logs/` - Log datoteke

## Prva Upotreba

1. Pokreni aplikaciju: `python main.py`
2. Klikni "New Job" za kreiranje prvog backup job-a
3. Konfiguriraj:
   - Naziv i opis job-a
   - Izvorni folderi (što želiš backup-irati)
   - Odredišni folder (gdje će se čuvati backup)
   - Raspored izvršavanja
   - Filtere (opciono)
4. Spremi job
5. Klikni ▶ za ručno pokretanje ili čekaj automatsko izvršavanje

## Postavke

Pristup postavkama: **File → Settings**

- **Jezik**: Hrvatski / English
- **Tema**: Svijetla / Tamna / Sistemska
- **Obavijesti**: Email i zvučne notifikacije
- **Pokretanje**: Automatsko pokretanje sa Windowsima

## Troubleshooting

### Problem: ModuleNotFoundError

**Rješenje**: Provjeri da li je virtualno okruženje aktivirano i da su svi paketi instalirani:

```bash
pip install -r requirements.txt
```

### Problem: Permission Denied pri backup-u

**Rješenje**: Pokreni aplikaciju kao Administrator ili provjeri dozvole za izvorne i odredišne foldere.

### Problem: Servis se ne pokreće

**Rješenje**: Provjeri log datoteke u `data/logs/` direktoriju za detalje o grešci.

## Deinstalacija

1. Zaustavi servis (ako je instaliran):
   ```powershell
   .\nssm.exe stop BackupDaddyService
   .\nssm.exe remove BackupDaddyService confirm
   ```

2. Obriši projekt folder

## Podrška

Za pitanja i probleme, kontaktiraj developera ili otvori issue na projektu.
