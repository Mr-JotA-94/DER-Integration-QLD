\# Project Resources \& References



\## Key Websites \& Portals



\### Data Sources

\- \[AEMO DER Register](https://www.aemo.com.au/energy-systems/electricity/der-register/data-der)

\- \[AEMO Data Dashboard](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem)

\- \[Energy Queensland](https://www.energyqueensland.com.au/)



\### Standards \& Protocols

\- \[IEEE 2030.5 Standard](https://standards.ieee.org/standard/2030\_5-2018.html)

\- \[CSIP-AUS (Australian Profile)](https://arena.gov.au/knowledge-bank/der-standards-and-protocols/)

\- \[OpenADR Alliance](https://www.openadr.org/)



\### Industry Organizations

\- \[Clean Energy Council](https://www.cleanenergycouncil.org.au/)

\- \[ARENA - Australian Renewable Energy Agency](https://arena.gov.au/)

\- \[Smart Energy Council](https://www.smartenergy.org.au/)



\## Academic Papers \& Research



\### DER Integration

\- \[Add papers as you find them]



\### VPP Case Studies

\- \[Add case studies]



\## Companies to Watch

\- Evergen

\- Reposit Power  

\- ShineHub

\- Intellihub (GreenSync)

\- Energy Queensland



## Technical Notes
# Resources Update - Add to docs/resources.md

## Technical Notes

### kVA vs kW (important for all AEMO capacity data)
- AEMO DER Register reports capacity in **kVA** (kilovolt-amperes = apparent power)
- To convert to **kW** (real/active power): multiply by power factor (~0.95 for solar)
- Example: 10,770 kVA solar ≈ 10,231 kW ≈ 10.2 MW
- Always state kVA when citing AEMO figures directly
- This distinction matters when comparing to other sources that report in kW

### DER Hierarchy (AEMO data structure)
- **Site** = physical address / premises
- **Connection** = NMI (National Metering Identifier) grid connection point
- **Device** = individual DER unit (inverter, battery system, etc.)
- Queensland ratio: 1 site → 1.22 connections → 9.78 devices per connection
- This hierarchy is the source of protocol fragmentation in real-time DER orchestration

### NMI (National Metering Identifier)
- Unique 10-11 digit identifier for every electricity meter in Australia
- Format: State (1 digit) + Distribution area (2 digits) + Unique ID (7-8 digits)
- Example: 6305522341 (6 = QLD, 30 = Energex area)
- Used for billing, market settlement, and DER registration
- One premises can have multiple NMIs (e.g., dual occupancy, commercial buildings)

### Battery Penetration Rate
- Calculation: (Battery Connections / Solar Connections) × 100
- **NOT** a capacity ratio - it's a connection count ratio
- Queensland average: 4.6% (as of July 2025)
- Range: 2-15% across postcodes
- Low penetration = market opportunity for battery installers
- High penetration = early adopter areas, VPP aggregation potential

---

## Network Operators - Queensland

### Energex (SE Queensland)
- **Service area:** Brisbane, Gold Coast, Sunshine Coast, Ipswich, Logan, Moreton Bay
- **Coverage:** 25,000 km² (coastal corridor)
- **Population:** ~3.5 million (75% of Queensland population)
- **Postcodes:** Approximately 4000-4179, 4200-4230, 4300-4349, 4500-4521, 4550-4575
- **Grid characteristics:**
  - Urban/suburban distribution network
  - High customer density
  - Shorter feeder lines
  - Voltage management challenges from high DER penetration
- **DER stats:** 71% of Queensland's solar capacity in 54% of postcodes
- **Website:** energex.com.au
- **Parent company:** Energy Queensland (government-owned)

### Ergon Energy (Regional Queensland)
- **Service area:** All of Queensland except Energex territory
- **Coverage:** 1.7 million km² (97% of Queensland's land area)
- **Population:** ~1 million (25% of Queensland population)
- **Major regional cities:** Toowoomba, Mackay, Townsville, Cairns, Rockhampton, Bundaberg, Gladstone
- **Grid characteristics:**
  - Long rural feeder lines (some >100km)
  - Lower customer density
  - Reliability challenges (storms, bushfires, distance)
  - Voltage drop at end-of-line locations
- **DER stats:** 29% of Queensland's solar capacity across 46% of postcodes (more dispersed)
- **Website:** ergon.com.au
- **Parent company:** Energy Queensland (government-owned)

### Energy Queensland
- **Parent organization** of both Energex and Ergon Energy
- Government-owned corporation
- Publishes annual Distribution Annual Planning Reports (DAPR) with network constraint data
- Operates Queensland's electricity distribution networks
- Website: energyq.com.au

---

## Data Sources

### AEMO DER Register
- **URL:** https://www.aemo.com.au/energy-systems/electricity/der-register/data-der/data-downloads
- **Update frequency:** Quarterly (reported as of July 1, 2025 in this analysis)
- **Format:** CSV download
- **Aggregation level:** Postcode × Business/Residential
- **Privacy:** Postcodes with <10 DER sites aggregated into single row
- **Key columns:**
  - `Sum of Num_DER_Sites` - number of physical premises
  - `Sum of Num_DER_Connections` - number of NMI connection points
  - `Sum of Solar_Devices` - number of individual solar inverter systems
  - `Sum of Solar_capacity_kVA` - total solar capacity in kVA
  - `Sum of Battery_Connections` - number of battery storage connections
  - `Sum of Battery_Storage_kVAh` - total battery storage in kVAh
  - `nmi_bus_res2` - classification (RESIDENTIAL or BUSINESS)

### Australian Postcode Coordinates
- **Source:** matthewproctor/australianpostcodes (GitHub)
- **URL:** https://github.com/matthewproctor/australianpostcodes
- **Direct CSV:** https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.csv
- **Last updated:** September 2025
- **Derived from:** G-NAF (Geocoded National Address File) - official government data
- **Key columns:**
  - `postcode` - 4-digit Australian postcode
  - `locality` - suburb/locality name (can be misleading - use first alphabetically)
  - `state` - Australian state (QLD, NSW, VIC, etc.)
  - `lat` / `long` - standard coordinates
  - `Lat_precise` / `Long_precise` - higher precision coordinates (use when available)
  - `sa3name`, `sa4name` - Statistical Area names (regional groupings)
- **Note:** One postcode can have multiple localities - dataset includes multiple rows per postcode in some cases

### Australian Postcode Boundaries (GeoJSON)
- **Source:** Offbeatmammal/AU_Postcode_Map (GitHub)
- **URL:** https://github.com/Offbeatmammal/AU_Postcode_Map
- **Direct GeoJSON:** https://raw.githubusercontent.com/Offbeatmammal/AU_Postcode_Map/main/POA_2021_AUST_GDA2020_15percent.json
- **Based on:** ABS 2021 Postal Area boundaries (official)
- **Simplification:** 15% of original polygon complexity (faster rendering)
- **File size:** ~15MB
- **GeoJSON key:** `POA_CODE21` (Postal Area Code 2021)
- **Coordinate system:** GDA2020 (Australian standard)

### Network Operator Boundaries
- **Energex:** No official GeoJSON available - use postcode classification
- **Ergon Energy:** GIS data available through Queensland Government Open Data Portal
- **Practical approach:** Postcode range-based classification (approximate but functional)

---

## Key Companies & Organizations

### Battery Installers (Queensland-focused)
- **Halcol Energy** - https://halcolenergy.com.au/ (Sunshine Coast/Brisbane)
- **Solar Battery Group** - Claims Australia's largest battery installer
- **MC Electrical** - https://www.mcelectrical.com.au/ (Brisbane, Mark Cavanagh)
- **Stag Electrical** - Award-winning, 10,000+ installations
- **Solar Run** - Southeast Queensland focus

### VPP Operators (Active in Queensland)
- **AGL Virtual Power Plant** - Acquired Tesla SA VPP, largest residential VPP in Australia
- **Reposit Power** - Independent VPP platform, "grid credits" model
- **Evergen** - VPP software platform, partners with Amber Electric
- **Tesla Energy Plan** - via Energy Locals, Powerwall-specific
- **Amber Electric** - Wholesale pass-through pricing + VPP participation

### Network Operators
- **Energex** - https://www.energex.com.au/
- **Ergon Energy** - https://www.ergon.com.au/
- **Energy Queensland** - https://www.energyq.com.au/ (parent company)

### Market Operator & Regulator
- **AEMO (Australian Energy Market Operator)** - https://www.aemo.com.au/
- **AER (Australian Energy Regulator)** - https://www.aer.gov.au/
- **Clean Energy Council** - https://www.cleanenergycouncil.org.au/
- **ARENA (Australian Renewable Energy Agency)** - https://arena.gov.au/

---

## Standards & Protocols

### DER Communication Standards
- **IEEE 2030.5 (CSIP-AUS)** - Becoming mandatory in Australia for new DER installations
  - Version 1.2 rolling out mid-2026
  - Common Smart Inverter Profile - Australian variant
  - Device-to-aggregator communication standard
- **OpenADR** - Used for demand response programs
  - Aggregator-to-market level (not device level)
  - Common in commercial/industrial DER
- **Modbus** - Legacy protocol still used in many older systems
- **SunSpec** - Data model for solar inverters
- **Proprietary APIs** - Manufacturer-specific (Tesla, SolarEdge, Enphase, etc.)

### References
- IEEE 2030.5 overview: https://standards.ieee.org/standard/2030_5-2018.html
- CSIP-AUS documentation: https://arena.gov.au/knowledge-bank/der-standards-and-protocols/
- OpenADR Alliance: https://www.openadr.org/

---

## Policy & Programs

### Cheaper Home Batteries Program
- **Launch date:** July 1, 2025
- **Discount:** ~30% off battery systems through STCs (Small-scale Technology Certificates)
- **Eligibility:** Must be VPP-capable battery
- **Impact:** Mandatory VPP participation for rebate = every rebate-funded installation is potential VPP participant
- **Reference:** https://www.cleanenergyregulator.gov.au/

### Queensland Solar Programs
- **Solar for Rentals** - $3,500 rebate for rental properties
- **Interest-Free Loans** - $0 interest loans up to $5,000 for batteries
- Check current programs: https://www.qld.gov.au/environment/climate/climate-change/renewables

---

## Learning Resources

### AEMO Documentation
- DER Register User Guide
- NEM Data Model documentation
- Market settlement guide (understanding NMI structure)

### Network Planning
- Energex DAPR (Distribution Annual Planning Report) - annual network constraint maps
- Ergon DAPR - regional network challenges and planned upgrades
- Available: https://www.energyq.com.au/about-us/corporate-information/regulatory-obligations

### Technical Guides
- Clean Energy Council DER technical standards
- Battery installation AS/NZS standards
- VPP aggregation best practices

---

## Tools & Technologies Used

### Python Libraries
- **pandas** - data manipulation and aggregation
- **plotly** - interactive maps and charts
- **matplotlib / seaborn** - static visualizations
- **requests** - downloading data from web sources
- **json** - working with GeoJSON boundary files

### Development Environment
- **Jupyter Notebook** - interactive analysis and documentation
- **Git / GitHub** - version control and portfolio hosting
- **Python virtual environment (venv)** - isolated dependency management

### Data Formats
- **CSV** - AEMO data, postcode coordinates
- **GeoJSON** - postcode boundaries for choropleth maps
- **JSON** - configuration and metadata

---

## Geographic Reference

### Queensland Postcode Ranges (approximate)
- **4000-4179:** Brisbane metro and inner suburbs
- **4200-4230:** Gold Coast
- **4300-4349:** Ipswich, Logan, western Brisbane suburbs
- **4350-4399:** Toowoomba region (Ergon territory begins)
- **4400-4499:** Darling Downs, Southern Inland
- **4500-4521:** Moreton Bay, Caboolture
- **4550-4575:** Sunshine Coast
- **4600-4699:** Wide Bay, Bundaberg, Maryborough
- **4700-4799:** Central Queensland (Rockhampton, Gladstone, Mackay)
- **4800-4899:** North Queensland (Townsville, Cairns)

### Regional Cities (Tier 2 Markets)
1. **Toowoomba (4350)** - 140K population, largest inland city
2. **Mackay (4740)** - 80K population, sugar capital, cyclone-prone
3. **Townsville (4810)** - 180K population, largest northern city
4. **Cairns (4870)** - 150K population, tropical tourism hub
5. **Rockhampton (4700)** - 80K population, beef capital
6. **Bundaberg (4670)** - 70K population, industrial/agricultural
7. **Gladstone (4680)** - 65K population, major port and energy hub
8. **Maryborough (4650)** - 55K population, heritage city

---

**Last Updated:** February 19, 2026
**Data Version:** AEMO DER Register July 2025 snapshot



\## Tutorials \& Learning Resources

\- \[Add helpful tutorials]



---



\*Updated: 13/03/2026

