"""
Data Loading Utilities
=======================

Helper functions for loading data with flexible file naming and formats.

Usage in notebooks:
    from src.data_loader import load_aemo_data
    
    df = load_aemo_data()
"""

import pandas as pd
import os
import glob
from pathlib import Path

# ============================================================================
# AEMO COLUMN NAME MAPPING
# ============================================================================
# AEMO changes column names between releases. This mapping handles variations.
# The loader will automatically detect and rename columns to standardized names.

AEMO_COLUMN_MAPPINGS = {
    # Standard name: [possible variations in AEMO files]
    'state': ['state', 'State'],
    'postcode': ['postcode', 'Postcode'],
    'nmi_bus_res': ['nmi_bus_res2', 'Bus_Resid', 'nmi_bus_res', 'Business_Residential'],
    'DER_Sites': ['Sum of Num_DER_Sites', 'Num_DER_Sites', 'DER_Sites'],
    'DER_Connections': ['Sum of Num_DER_Connections', 'Num_DER_Connections', 'DER_Connections'],
    'Installed_DER_capacity_kVA': ['Sum of Installed_DER_capacity_kVA', 'Installed_DER_capacity_kVA'],
    'Solar_Connections': ['Sum of Solar_Connections', 'Solar_Connections'],
    'Solar_Devices': ['Sum of Solar_Devices', 'Solar_Devices'],
    'Solar_capacity_kVA': ['Sum of Solar_capacity_kVA', 'Solar_capacity_kVA'],
    'Battery_Connections': ['Sum of Battery_Connections', 'Battery_Connections'],
    'Battery_Devices': ['Sum of Battery_Devices', 'Battery_Devices'],
    'Battery_capacity_kVA': ['Sum of Battery_capacity_kVA', 'Battery_capacity_kVA'],
    'Battery_Storage_kVAh': ['Sum of Battery_Storage_kVAh', 'Battery_Storage_kVAh'],
    'Num_Other_Connections': ['Sum of Num_Other_Connections', 'Num_Other_Connections'],
    'Installed_OtherDER_capacity_kVA': ['Sum of Installed_OtherDER_capacity_kVA', 'Installed_OtherDER_capacity_kVA']
}


def standardize_column_names(df):
    """
    Standardize AEMO column names to consistent format.
    
    Handles variations in column naming across different AEMO data releases.
    Maps known column name variations to standardized names.
    
    Args:
        df: pandas DataFrame with raw AEMO columns
        
    Returns:
        pandas DataFrame with standardized column names
    """
    rename_dict = {}
    
    for standard_name, variations in AEMO_COLUMN_MAPPINGS.items():
        for variant in variations:
            if variant in df.columns:
                rename_dict[variant] = standard_name
                break  # Use first match
    
    if rename_dict:
        df = df.rename(columns=rename_dict)
        print(f"  ✓ Standardized {len(rename_dict)} column names")
        
        # Show what was renamed for transparency
        for old, new in rename_dict.items():
            if old != new:
                print(f"    '{old}' → '{new}'")
    
    return df

def find_file(directory, patterns):
    """
    Find first file matching any of the given patterns.
    
    Args:
        directory: Directory to search in
        patterns: List of glob patterns to try
        
    Returns:
        Path to first matching file, or None
    """
    for pattern in patterns:
        files = glob.glob(os.path.join(directory, pattern))
        if files:
            return files[0]
    return None


def load_aemo_data(data_raw_path='data/raw'):
    """
    Load AEMO DER Register data with flexible naming and format support.
    
    Handles:
        - CSV or Excel (.xlsx) formats
        - Various naming patterns
        - Multiple sheets (if Excel)
        
    Args:
        data_raw_path: Path to data/raw directory
        
    Returns:
        pandas DataFrame with AEMO data
        
    Raises:
        FileNotFoundError: If no AEMO file found
        ValueError: If file format not supported
    """
    
    # Patterns to search for (in order of preference)
    patterns = [
        'aemo_der_register_raw.csv',
        'aemo_der_register*.csv',
        'DER_Register*.csv',
        'aemo_der_register*.xlsx',
        'DER_Register*.xlsx'
    ]
    
    aemo_path = find_file(data_raw_path, patterns)
    
    if not aemo_path:
        raise FileNotFoundError(
            f"AEMO DER Register file not found in {data_raw_path}/\n"
            f"Expected patterns: {', '.join(patterns)}\n"
            f"Please download from: https://www.aemo.com.au/energy-systems/"
            f"electricity/der-register/data-der/data-downloads"
        )
    
    filename = os.path.basename(aemo_path)
    print(f"Loading AEMO data: {filename}")
    
    # Load based on extension
    if aemo_path.endswith('.csv'):
        df = pd.read_csv(aemo_path, dtype={'postcode': str})
        
    elif aemo_path.endswith('.xlsx'):
        # Try to load Excel file
        try:
            # First, check how many sheets
            excel_file = pd.ExcelFile(aemo_path)
            sheet_names = excel_file.sheet_names
            
            if len(sheet_names) == 1:
                # Single sheet - just load it
                df = pd.read_excel(aemo_path, sheet_name=0, engine='openpyxl', dtype={'postcode': str})
                
            else:
                # Multiple sheets - try to find the right one
                # Common AEMO sheet names
                target_sheets = [
                    'DER Register',
                    'Data',
                    'Sheet1',
                    sheet_names[0]  # Default to first sheet
                ]
                
                sheet_to_load = None
                for sheet in target_sheets:
                    if sheet in sheet_names:
                        sheet_to_load = sheet
                        break
                
                print(f"  Found {len(sheet_names)} sheets: {', '.join(sheet_names)}")
                print(f"  Loading sheet: '{sheet_to_load}'")
                
                df = pd.read_excel(aemo_path, sheet_name=sheet_to_load, engine='openpyxl', dtype={'postcode': str})
                
        except Exception as e:
            raise ValueError(
                f"Error loading Excel file: {e}\n"
                f"Try converting to CSV: Open in Excel → Save As → CSV format"
            )
    
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    
    # Standardize column names to handle AEMO naming variations
    df = standardize_column_names(df)
    
    print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")
    
    return df


def load_postcode_coords(data_raw_path='data/raw'):
    """
    Load Australian postcode coordinates.
    
    Args:
        data_raw_path: Path to data/raw directory
        
    Returns:
        pandas DataFrame with postcode coordinates
    """
    coords_path = os.path.join(data_raw_path, 'au_postcode_coords.csv')
    
    if not os.path.exists(coords_path):
        raise FileNotFoundError(
            f"Postcode coordinates not found: {coords_path}\n"
            f"Run setup_project.py to download, or manually download from:\n"
            f"https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.csv"
        )
    
    df = pd.read_csv(coords_path, dtype={'postcode': str})
    print(f"✓ Loaded {len(df):,} postcode coordinates")
    
    return df


def load_processed_data(filename, data_processed_path='data/processed'):
    """
    Load a processed dataset with helpful error messages.
    
    Args:
        filename: Name of file to load (e.g., 'qld_der_data.csv')
        data_processed_path: Path to data/processed directory
        
    Returns:
        pandas DataFrame
    """
    filepath = os.path.join(data_processed_path, filename)
    
    if not os.path.exists(filepath):
        # Provide helpful error message about which notebook creates this file
        notebook_map = {
            'qld_der_data.csv': '02_aemo_data_exploration.ipynb',
            'qld_der_postcode_enriched.csv': '03_statistics_and_maps_v2.ipynb',
            'qld_der_with_network_zones.csv': '04_network_zones_overlay.ipynb'
        }
        
        creating_notebook = notebook_map.get(filename, 'a previous notebook')
        
        raise FileNotFoundError(
            f"Processed file not found: {filepath}\n"
            f"This file is created by: {creating_notebook}\n"
            f"Run that notebook first to generate this file."
        )
    
    df = pd.read_csv(filepath, dtype={'postcode': str})
    print(f"✓ Loaded {filename}: {len(df):,} rows")
    
    return df


# Example usage for notebooks:
if __name__ == "__main__":
    # Test the loader
    print("Testing data loaders...\n")
    
    try:
        df_aemo = load_aemo_data()
        print("\n✓ AEMO data loader works!")
    except FileNotFoundError as e:
        print(f"\n✗ AEMO data not found: {e}")
    
    try:
        df_coords = load_postcode_coords()
        print("\n✓ Postcode coordinates loader works!")
    except FileNotFoundError as e:
        print(f"\n✗ Postcode coords not found: {e}")
