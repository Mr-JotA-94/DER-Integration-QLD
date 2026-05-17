"""
Dashboard Data Preparation Script
==================================

Generates curated datasets for Power BI and React dashboards from QLD DER analysis.

Outputs:
    - dashboard_summary.csv: High-level metrics for KPI cards
    - postcode_details.csv: Complete postcode-level data for maps and filters
    - network_comparison.csv: Energex vs Ergon comparison
    - top_opportunities.csv: Ranked postcodes by various criteria
    - protocol_landscape.json: Manufacturer/protocol data for visualization
    - geojson_features.json: Simplified GeoJSON for web mapping

Usage:
    python prepare_dashboard_data.py
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
OUTPUTS = PROJECT_ROOT / 'outputs' / 'dashboards'

# Create outputs directory
OUTPUTS.mkdir(parents=True, exist_ok=True)

print("="*60)
print("  DASHBOARD DATA PREPARATION")
print("="*60)
print()


# ============================================================================
# 1. LOAD PROCESSED DATA
# ============================================================================

print("1. Loading processed data...")

# Main dataset with network zones
df = pd.read_csv(
    DATA_PROCESSED / 'qld_der_with_network_zones.csv',
    dtype={'postcode': str}
)

print(f"   ✓ Loaded {len(df):,} postcodes")
print()


# ============================================================================
# 2. SUMMARY METRICS (for KPI cards)
# ============================================================================

print("2. Generating summary metrics...")

summary = {
    'metric': [],
    'value': [],
    'format': [],
    'category': []
}

# Total metrics
summary['metric'].extend([
    'Total Solar Connections',
    'Total Battery Connections',
    'Untapped Battery Customers',
    'Battery Penetration Rate',
    'Total Solar Capacity (MVA)',
    'Total Battery Storage (MVAh)',
    'Average Devices per Connection',
    'Total Postcodes'
])

solar_conns = df['Solar_Connections'].sum()
battery_conns = df['Battery_Connections'].sum()
untapped = solar_conns - battery_conns
battery_pen = (battery_conns / solar_conns * 100)
solar_mva = df['Solar_kVA'].sum() / 1000
battery_mvah = df['Battery_Storage_kVAh'].sum() / 1000
avg_devices = df['Solar_Devices'].sum() / df['Solar_Connections'].sum()

summary['value'].extend([
    solar_conns,
    battery_conns,
    untapped,
    battery_pen,
    solar_mva,
    battery_mvah,
    avg_devices,
    len(df)
])

summary['format'].extend([
    'integer',
    'integer',
    'integer',
    'percentage',
    'decimal_1',
    'decimal_1',
    'decimal_2',
    'integer'
])

summary['category'].extend(['scale'] * 8)

# Network operator split
for network in ['Energex', 'Ergon']:
    net_df = df[df['Network_Operator'] == network]
    
    summary['metric'].extend([
        f'{network} Solar Capacity (MVA)',
        f'{network} Untapped Customers',
        f'{network} Battery Penetration %',
        f'{network} Postcodes'
    ])
    
    net_solar_conns = net_df['Solar_Connections'].sum()
    net_battery_conns = net_df['Battery_Connections'].sum()
    
    summary['value'].extend([
        net_df['Solar_kVA'].sum() / 1000,
        net_solar_conns - net_battery_conns,
        (net_battery_conns / net_solar_conns * 100) if net_solar_conns > 0 else 0,
        len(net_df)
    ])
    
    summary['format'].extend([
        'decimal_1',
        'integer',
        'percentage',
        'integer'
    ])
    
    summary['category'].extend(['network'] * 4)

df_summary = pd.DataFrame(summary)
df_summary.to_csv(OUTPUTS / 'dashboard_summary.csv', index=False)

print(f"   ✓ Created dashboard_summary.csv ({len(df_summary)} metrics)")
print()


# ============================================================================
# 3. POSTCODE DETAILS (for maps and detailed views)
# ============================================================================

print("3. Preparing postcode details...")

# Select and rename columns for clarity
postcode_details = df[[
    'postcode', 'Suburb', 'Region', 'lat', 'lon',
    'Network_Operator',
    'DER_Sites', 'DER_Connections',
    'Solar_Connections', 'Solar_Devices', 'Solar_kVA',
    'Battery_Connections', 'Battery_Devices', 'Battery_kVA', 'Battery_Storage_kVAh',
    'Battery_Penetration_pct', 'Devices_per_Connection'
]].copy()

# Add derived columns
postcode_details['Untapped_Customers'] = (
    postcode_details['Solar_Connections'] - postcode_details['Battery_Connections']
)

postcode_details['Solar_MVA'] = postcode_details['Solar_kVA'] / 1000
postcode_details['Battery_MVAh'] = postcode_details['Battery_Storage_kVAh'] / 1000

# Calculate opportunity score (simple weighted formula)
# Higher score = better opportunity for battery installers
postcode_details['Opportunity_Score'] = (
    (postcode_details['Untapped_Customers'] / postcode_details['Untapped_Customers'].max() * 0.4) +
    (postcode_details['Solar_MVA'] / postcode_details['Solar_MVA'].max() * 0.3) +
    ((100 - postcode_details['Battery_Penetration_pct']) / 100 * 0.3)
) * 100

postcode_details['Opportunity_Score'] = postcode_details['Opportunity_Score'].round(1)

# Add opportunity tier classification
postcode_details['Opportunity_Tier'] = pd.cut(
    postcode_details['Opportunity_Score'],
    bins=[0, 33, 66, 100],
    labels=['Low', 'Medium', 'High']
)

postcode_details.to_csv(OUTPUTS / 'postcode_details.csv', index=False)

print(f"   ✓ Created postcode_details.csv ({len(postcode_details)} postcodes)")
print()


# ============================================================================
# 4. NETWORK COMPARISON (Energex vs Ergon)
# ============================================================================

print("4. Creating network operator comparison...")

network_comp = df.groupby('Network_Operator').agg({
    'postcode': 'count',
    'DER_Sites': 'sum',
    'Solar_Connections': 'sum',
    'Battery_Connections': 'sum',
    'Solar_kVA': lambda x: x.sum() / 1000,
    'Battery_Storage_kVAh': lambda x: x.sum() / 1000,
    'Battery_Penetration_pct': 'mean'
}).round(2)

network_comp.columns = [
    'Postcodes',
    'DER_Sites',
    'Solar_Connections',
    'Battery_Connections',
    'Solar_MVA',
    'Battery_MVAh',
    'Avg_Battery_Penetration_pct'
]

network_comp['Untapped_Customers'] = (
    network_comp['Solar_Connections'] - network_comp['Battery_Connections']
)

network_comp['Market_Share_Solar_pct'] = (
    network_comp['Solar_MVA'] / network_comp['Solar_MVA'].sum() * 100
).round(1)

network_comp.reset_index(inplace=True)
network_comp.to_csv(OUTPUTS / 'network_comparison.csv', index=False)

print(f"   ✓ Created network_comparison.csv")
print()


# ============================================================================
# 5. TOP OPPORTUNITIES (ranked postcodes)
# ============================================================================

print("5. Ranking top opportunities...")

# Multiple ranking criteria
rankings = {}

# Top by untapped customers
rankings['untapped'] = postcode_details.nlargest(20, 'Untapped_Customers')[[
    'postcode', 'Suburb', 'Network_Operator', 'Untapped_Customers',
    'Solar_MVA', 'Battery_Penetration_pct', 'Opportunity_Score'
]].copy()
rankings['untapped']['Rank_Criteria'] = 'Untapped Customers'

# Top by solar capacity (existing market)
rankings['solar_cap'] = postcode_details.nlargest(20, 'Solar_MVA')[[
    'postcode', 'Suburb', 'Network_Operator', 'Solar_MVA',
    'Untapped_Customers', 'Battery_Penetration_pct', 'Opportunity_Score'
]].copy()
rankings['solar_cap']['Rank_Criteria'] = 'Solar Capacity'

# Top by opportunity score (balanced)
rankings['opportunity'] = postcode_details.nlargest(20, 'Opportunity_Score')[[
    'postcode', 'Suburb', 'Network_Operator', 'Opportunity_Score',
    'Untapped_Customers', 'Solar_MVA', 'Battery_Penetration_pct'
]].copy()
rankings['opportunity']['Rank_Criteria'] = 'Opportunity Score'

# Regional cities only (Ergon territory)
regional = postcode_details[postcode_details['Network_Operator'] == 'Ergon']
rankings['regional'] = regional.nlargest(15, 'Opportunity_Score')[[
    'postcode', 'Suburb', 'Network_Operator', 'Opportunity_Score',
    'Untapped_Customers', 'Solar_MVA', 'Battery_Penetration_pct'
]].copy()
rankings['regional']['Rank_Criteria'] = 'Regional Cities'

# Combine all rankings
top_opportunities = pd.concat(rankings.values(), ignore_index=True)
top_opportunities.to_csv(OUTPUTS / 'top_opportunities.csv', index=False)

print(f"   ✓ Created top_opportunities.csv ({len(top_opportunities)} records)")
print()


# ============================================================================
# 6. PROTOCOL LANDSCAPE (for visualization)
# ============================================================================

print("6. Creating protocol landscape data...")

# Based on research, create manufacturer distribution estimate
# (AEMO doesn't publish this, so using Australian market share estimates)

manufacturers = [
    {
        'name': 'Fronius',
        'market_share': 0.25,
        'protocol': 'Solar.web API (Proprietary)',
        'category': 'Premium European',
        'csip_aus_support': True,
        'integration_complexity': 'Medium',
        'control_capability': 'Monitoring + Limited Control'
    },
    {
        'name': 'SolarEdge',
        'market_share': 0.20,
        'protocol': 'SolarEdge Cloud API (Proprietary)',
        'category': 'Premium (DC Optimizers)',
        'csip_aus_support': True,
        'integration_complexity': 'High',
        'control_capability': 'Monitoring + Panel-level Data'
    },
    {
        'name': 'Enphase',
        'market_share': 0.15,
        'protocol': 'Enlighten API (Proprietary)',
        'category': 'Microinverters',
        'csip_aus_support': True,
        'integration_complexity': 'High',
        'control_capability': 'Monitoring + Per-inverter Control'
    },
    {
        'name': 'Sungrow',
        'market_share': 0.18,
        'protocol': 'iSolarCloud API + Modbus',
        'category': 'Value Chinese',
        'csip_aus_support': False,
        'integration_complexity': 'Medium',
        'control_capability': 'Monitoring Only (most models)'
    },
    {
        'name': 'GoodWe',
        'market_share': 0.08,
        'protocol': 'SEMS Portal API',
        'category': 'Budget Chinese',
        'csip_aus_support': False,
        'integration_complexity': 'Medium',
        'control_capability': 'Monitoring Only'
    },
    {
        'name': 'Huawei',
        'market_share': 0.06,
        'protocol': 'FusionSolar API',
        'category': 'Commercial/Utility',
        'csip_aus_support': True,
        'integration_complexity': 'Medium',
        'control_capability': 'Monitoring + Control (newer models)'
    },
    {
        'name': 'SMA',
        'market_share': 0.04,
        'protocol': 'Sunny Portal API + Modbus',
        'category': 'Premium German',
        'csip_aus_support': True,
        'integration_complexity': 'Low',
        'control_capability': 'Monitoring + Control'
    },
    {
        'name': 'Tesla',
        'market_share': 0.02,
        'protocol': 'Powerwall Gateway API',
        'category': 'Integrated Solar+Battery',
        'csip_aus_support': True,
        'integration_complexity': 'Low',
        'control_capability': 'Full Control (batteries)'
    },
    {
        'name': 'Legacy/Other',
        'market_share': 0.02,
        'protocol': 'Modbus (local only)',
        'category': 'Pre-2015 installations',
        'csip_aus_support': False,
        'integration_complexity': 'Very High',
        'control_capability': 'Monitoring Only (if any)'
    }
]

# Calculate estimated device counts
total_devices = df['Solar_Devices'].sum()

for mfr in manufacturers:
    mfr['estimated_devices_qld'] = int(total_devices * mfr['market_share'])

# Integration cost estimates
integration_costs = {
    'per_api_setup': 25000,  # One-time per manufacturer
    'per_api_maintenance': 5000,  # Annual per manufacturer
    'total_apis_needed': len([m for m in manufacturers if m['market_share'] > 0.01]),
    'csip_aus_setup': 75000,  # One-time for CSIP-AUS
    'csip_aus_maintenance': 12000  # Annual
}

protocol_data = {
    'manufacturers': manufacturers,
    'integration_costs': integration_costs,
    'timeline': {
        '2026': {
            'csip_aus_adoption': 0.10,
            'legacy_proprietary': 0.90
        },
        '2028': {
            'csip_aus_adoption': 0.25,
            'legacy_proprietary': 0.75
        },
        '2030': {
            'csip_aus_adoption': 0.40,
            'legacy_proprietary': 0.60
        },
        '2035': {
            'csip_aus_adoption': 0.70,
            'legacy_proprietary': 0.30
        }
    }
}

with open(OUTPUTS / 'protocol_landscape.json', 'w') as f:
    json.dump(protocol_data, f, indent=2)

print(f"   ✓ Created protocol_landscape.json")
print()


# ============================================================================
# 7. SIMPLIFIED GEOJSON (for web mapping)
# ============================================================================

print("7. Creating simplified GeoJSON for web...")

# For React dashboard, we want a lightweight GeoJSON
# Include only postcodes with DER data and key metrics

features = []

for _, row in postcode_details.iterrows():
    feature = {
        'type': 'Feature',
        'properties': {
            'postcode': row['postcode'],
            'suburb': row['Suburb'],
            'network': row['Network_Operator'],
            'solar_mva': round(row['Solar_MVA'], 1),
            'battery_pen': round(row['Battery_Penetration_pct'], 1),
            'untapped': int(row['Untapped_Customers']),
            'opp_score': round(row['Opportunity_Score'], 1),
            'opp_tier': row['Opportunity_Tier']
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [row['lon'], row['lat']]
        }
    }
    features.append(feature)

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open(OUTPUTS / 'geojson_features.json', 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"   ✓ Created geojson_features.json ({len(features)} features)")
print()


# ============================================================================
# 8. SUMMARY REPORT
# ============================================================================

print("="*60)
print("  DASHBOARD DATA PREPARATION COMPLETE")
print("="*60)
print()
print("Generated files in outputs/dashboards/:")
print()
print("  Power BI ready:")
print("    - dashboard_summary.csv (KPI metrics)")
print("    - postcode_details.csv (main dataset)")
print("    - network_comparison.csv (Energex vs Ergon)")
print("    - top_opportunities.csv (ranked postcodes)")
print()
print("  React dashboard ready:")
print("    - geojson_features.json (map data)")
print("    - protocol_landscape.json (protocol viz)")
print()
print("Next steps:")
print("  1. Import CSVs into Power BI")
print("  2. Use JSON files in React dashboard")
print("  3. Build visualizations!")
print()
print("="*60)
