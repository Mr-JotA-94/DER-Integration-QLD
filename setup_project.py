"""
Project Setup Script
====================

Run this after cloning the repository to download required data files
and verify the project structure.

This script:
1. Creates necessary directories
2. Downloads AEMO data (if you provide the URL)
3. Downloads postcode coordinates
4. Downloads postcode boundary GeoJSON
5. Verifies all dependencies are installed

Usage:
    python setup_project.py
"""

import os
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
OUTPUTS = PROJECT_ROOT / 'outputs'

print("="*60)
print("  DER INTEGRATION QUEENSLAND - PROJECT SETUP")
print("="*60)
print()

# ============================================================================
# 1. CREATE DIRECTORY STRUCTURE
# ============================================================================

print("1. Creating directory structure...")

directories = [
    DATA_RAW,
    DATA_PROCESSED,
    OUTPUTS / 'figures',
    OUTPUTS / 'dashboards',
    PROJECT_ROOT / 'notebooks',
    PROJECT_ROOT / 'src',
    PROJECT_ROOT / 'docs'
]

for directory in directories:
    directory.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ {directory.relative_to(PROJECT_ROOT)}")

print()

# ============================================================================
# 2. DOWNLOAD POSTCODE COORDINATES
# ============================================================================

print("2. Downloading Australian postcode coordinates...")

coords_url = "https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.csv"
coords_path = DATA_RAW / 'au_postcode_coords.csv'

if coords_path.exists():
    print(f"   ⚠ File already exists: {coords_path.name}")
else:
    try:
        print(f"   Downloading from: matthewproctor/australianpostcodes")
        response = requests.get(coords_url, timeout=30)
        response.raise_for_status()
        
        with open(coords_path, 'wb') as f:
            f.write(response.content)
        
        print(f"   ✓ Downloaded: {coords_path.name} ({len(response.content)/1024:.1f} KB)")
    except Exception as e:
        print(f"   ✗ Download failed: {e}")
        print(f"   → Manual download: {coords_url}")

print()

# ============================================================================
# 3. DOWNLOAD POSTCODE BOUNDARIES GEOJSON
# ============================================================================

print("3. Downloading Australian postcode boundaries...")

geojson_url = "https://raw.githubusercontent.com/Offbeatmammal/AU_Postcode_Map/main/POA_2021_AUST_GDA2020_15percent.json"
geojson_path = DATA_RAW / 'au_postcode_boundaries.geojson'

if geojson_path.exists():
    print(f"   ⚠ File already exists: {geojson_path.name}")
else:
    try:
        print(f"   Downloading from: Offbeatmammal/AU_Postcode_Map (~15MB)")
        print(f"   This may take a minute...")
        response = requests.get(geojson_url, timeout=120)
        response.raise_for_status()
        
        with open(geojson_path, 'wb') as f:
            f.write(response.content)
        
        print(f"   ✓ Downloaded: {geojson_path.name} ({len(response.content)/1024/1024:.1f} MB)")
    except Exception as e:
        print(f"   ✗ Download failed: {e}")
        print(f"   → Manual download: {geojson_url}")

print()

# ============================================================================
# 4. AEMO DATA INSTRUCTIONS
# ============================================================================

print("4. AEMO DER Register data (manual download required)...")
print()

# Check if any AEMO file already exists
import glob
aemo_patterns = [
    str(DATA_RAW / 'aemo_der_register*.csv'),
    str(DATA_RAW / 'DER_Register*.csv'),
    str(DATA_RAW / 'aemo_der_register*.xlsx'),
    str(DATA_RAW / 'DER_Register*.xlsx')
]

aemo_files = []
for pattern in aemo_patterns:
    aemo_files.extend(glob.glob(pattern))

if aemo_files:
    print(f"   ✓ AEMO data found: {os.path.basename(aemo_files[0])}")
    print(f"   Location: {aemo_files[0]}")
else:
    print("   ⚠ AEMO DER Register not found. Please download manually:")
    print()
    print("   1. Visit: https://www.aemo.com.au/energy-systems/electricity/")
    print("      der-register/data-der/data-downloads")
    print()
    print("   2. Download the latest 'DER Register' file (CSV or Excel)")
    print()
    print("   3. Save it to data/raw/ folder")
    print("      Filename can be:")
    print("      - aemo_der_register_raw.csv (preferred)")
    print("      - DER_Register_<date>.xlsx (will work)")
    print("      - Any file matching: DER_Register*.csv or *.xlsx")
    print()
    print("   Note: If you download .xlsx, the notebooks will handle it automatically")
    print("         (requires 'openpyxl' package)")

print()

# ============================================================================
# 5. VERIFY PYTHON DEPENDENCIES
# ============================================================================

print("5. Verifying Python dependencies...")

required_packages = [
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'plotly',
    'requests',
    'jupyter'
]

missing = []

for package in required_packages:
    try:
        __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} (missing)")
        missing.append(package)

if missing:
    print()
    print(f"   ⚠ Missing packages: {', '.join(missing)}")
    print()
    print("   Install with:")
    print(f"   pip install {' '.join(missing)}")
else:
    print()
    print("   ✓ All dependencies installed")

print()

# ============================================================================
# 6. SUMMARY
# ============================================================================

print("="*60)
print("  SETUP COMPLETE")
print("="*60)
print()
print("Next steps:")
print()
print("  1. Download AEMO DER Register (manual, see above)")
print()
print("  2. Run notebooks in order:")
print("     - notebooks/01_environment_test.ipynb")
print("     - notebooks/02_aemo_data_exploration.ipynb")
print("     - notebooks/03_statistics_and_maps_v2.ipynb")
print("     - notebooks/04_network_zones_overlay.ipynb")
print()
print("  3. Run dashboard data prep:")
print("     python prepare_dashboard_data.py")
print()
print("  4. Build Power BI dashboard using outputs/dashboards/ files")
print()
print("="*60)
