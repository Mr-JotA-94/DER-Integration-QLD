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



\## Tutorials \& Learning Resources

\- \[Add helpful tutorials]



---



\*Updated: 15/02/2026

