"""
Test script to verify installation and basic functionality.
"""
import sys
from pathlib import Path

print("=" * 60)
print("Backup Daddy - Installation Test")
print("=" * 60)
print()

# Test 1: Python version
print("1. Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
    sys.exit(1)

# Test 2: Required modules
print("\n2. Checking required modules...")
required_modules = [
    "customtkinter",
    "PIL",
    "schedule",
    "dotenv",
    "psutil",
    "py7zr",
    "cryptography"
]

missing_modules = []
for module in required_modules:
    try:
        if module == "PIL":
            __import__("PIL")
        elif module == "dotenv":
            __import__("dotenv")
        else:
            __import__(module)
        print(f"   ✓ {module}")
    except ImportError:
        print(f"   ✗ {module} (MISSING)")
        missing_modules.append(module)

if missing_modules:
    print(f"\n   Missing modules: {', '.join(missing_modules)}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Project structure
print("\n3. Checking project structure...")
required_dirs = [
    "core",
    "gui",
    "utils",
    "locales",
    "data"
]

required_files = [
    "main.py",
    "requirements.txt",
    "README.md",
    "locales/hr.json",
    "locales/en.json",
    "core/backup_engine.py",
    "core/job_manager.py",
    "core/scheduler.py",
    "gui/main_window.py",
    "gui/job_editor.py",
    "gui/settings_window.py",
    "utils/i18n.py",
    "utils/theme_manager.py",
    "utils/config.py",
    "utils/logger.py"
]

project_root = Path(__file__).parent

for dir_name in required_dirs:
    dir_path = project_root / dir_name
    if dir_path.exists():
        print(f"   ✓ {dir_name}/")
    else:
        print(f"   ✗ {dir_name}/ (MISSING)")

for file_name in required_files:
    file_path = project_root / file_name
    if file_path.exists():
        print(f"   ✓ {file_name}")
    else:
        print(f"   ✗ {file_name} (MISSING)")

# Test 4: Import application modules
print("\n4. Testing application imports...")
try:
    from utils.i18n import get_i18n, t
    print("   ✓ i18n module")
    
    from utils.theme_manager import get_theme_manager
    print("   ✓ theme_manager module")
    
    from utils.config import get_config
    print("   ✓ config module")
    
    from utils.logger import get_logger
    print("   ✓ logger module")
    
    from core.job_manager import get_job_manager, BackupJob
    print("   ✓ job_manager module")
    
    from core.backup_engine import BackupEngine
    print("   ✓ backup_engine module")
    
    from core.scheduler import BackupScheduler
    print("   ✓ scheduler module")
    
except Exception as e:
    print(f"   ✗ Import error: {str(e)}")
    sys.exit(1)

# Test 5: Initialize core components
print("\n5. Testing core components initialization...")
try:
    i18n = get_i18n()
    print(f"   ✓ i18n initialized (language: {i18n.current_language})")
    
    theme_manager = get_theme_manager()
    print(f"   ✓ theme_manager initialized (theme: {theme_manager.current_theme})")
    
    config = get_config()
    print(f"   ✓ config initialized")
    
    logger = get_logger()
    print(f"   ✓ logger initialized")
    
    job_manager = get_job_manager()
    print(f"   ✓ job_manager initialized (jobs: {len(job_manager.get_all_jobs())})")
    
except Exception as e:
    print(f"   ✗ Initialization error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test translations
print("\n6. Testing translations...")
try:
    test_keys = [
        "app_title",
        "dashboard.title",
        "job_editor.job_name",
        "common.save"
    ]
    
    for key in test_keys:
        value = t(key)
        if value and value != key:
            print(f"   ✓ {key} = '{value}'")
        else:
            print(f"   ⚠ {key} (not found)")
            
except Exception as e:
    print(f"   ✗ Translation error: {str(e)}")

# Test 7: Test job creation
print("\n7. Testing job creation...")
try:
    test_job = BackupJob(
        name="Test Job",
        description="Test backup job",
        source_paths=["C:\\Test"],
        destination_path="C:\\Backup",
        backup_type="full"
    )
    
    job_dict = test_job.to_dict()
    restored_job = BackupJob.from_dict(job_dict)
    
    if restored_job.name == test_job.name:
        print(f"   ✓ Job serialization works")
    else:
        print(f"   ✗ Job serialization failed")
        
except Exception as e:
    print(f"   ✗ Job creation error: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("Installation Test Complete!")
print("=" * 60)
print("\nYou can now run the application:")
print("  GUI mode:     python main.py")
print("  Service mode: python main.py --service")
print("\nFor more information, see:")
print("  - INSTALL.md (Installation guide)")
print("  - USAGE.md (User guide)")
print("  - README.md (Project overview)")
print()
