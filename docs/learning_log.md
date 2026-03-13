\# DER Integration Project - Learning Log



\## Purpose

Track daily progress, learnings, challenges, and insights throughout this project.



---


## Week 1 - Feb 13-19, 2026

### Feb 17 - Statistics & Mapping Analysis Complete

**What I did:**
- Built enhanced analysis notebook with statistics, charts and maps
- Successfully rendered bubble map and choropleth across all 872 QLD postcodes
- Identified key hierarchy insight from AEMO data

**Key Finding (HEADLINE STAT):**
- Queensland has 996,217 DER Sites → 1,216,361 Connections → 11,892,070 Solar Devices
- That's 9.78x devices per NMI connection
- Each device may use a different manufacturer protocol/API
- This is direct empirical evidence of data integration fragmentation at scale

**What I learned:**
- AEMO aggregates <10 site postcodes into a privacy row — must be cleaned before analysis
- Capacity reported in kVA not kW (power factor ~0.95 to convert)
- Postcode data has Business/Residential split requiring aggregation before mapping
- Precise coordinates (Lat_precise/Long_precise) available in matthewproctor dataset
- GeoJSON boundary sources on GitHub go stale — ABS official sources are more reliable

**Challenges faced:**
- Two broken GitHub URLs for coordinate and boundary data (ferocia archived, joelkoen 404)
- Numeric columns stored as strings with commas needed cleaning before calculations
- Notebook JSON formatting issue required debugging

**Resources used:**
- AEMO DER Register: aemo.com.au/energy-systems/electricity/der-register
- Postcode coords: github.com/matthewproctor/australianpostcodes
- Postcode boundaries: github.com/Offbeatmammal/AU_Postcode_Map (ABS 2021 official)

---

### Feb 18 - Network Zone Overlay & Market Segmentation

**What I did:**
- Created network operator classification (Energex vs Ergon) using postcode ranges
- Overlaid network zones onto DER maps
- Segmented battery market opportunity by network operator
- Identified top regional city opportunities for battery deployment

**Key Findings:**

**Geographic Concentration:**
- Energex (SE QLD) = 71% of state solar capacity in just 54% of postcodes
- Proves massive urban concentration in Brisbane-Gold Coast-Sunshine Coast corridor
- High DER density creates different grid challenges than dispersed regional deployment

**Battery Market Segmentation:**
- Total untapped: 1.09M solar connections without batteries (95.4% of solar base)
- Energex zone: 791K potential customers (high density, high competition)
- Ergon zone: 294K potential customers (concentrated in 6-8 regional cities)

**Regional City Opportunity (Top 3 Ergon postcodes):**
1. **4740 (Mackay)** - 174 MVA solar, 5.6% battery penetration
   - Cyclone-prone area = built-in reliability value proposition
   - Industrial + residential market
2. **4670 (Bundaberg/Gladstone)** - 141 MVA solar, 4.7% battery penetration
   - Industrial energy hub with high electricity costs
   - Port city with commercial opportunity
3. **4350 (Toowoomba)** - 124 MVA solar, 3.4% battery penetration
   - QLD's largest inland city (140K population)
   - Urban density without metro competition
   - Lowest battery penetration = highest growth potential

**What I learned:**

**Network Operator Context:**
- Energex = SE Queensland (urban, high density)
  - Grid challenges: voltage rise from high solar export, peak demand, transformer limits
  - Battery value prop: grid services + bill savings + VPP participation
- Ergon = Regional/Remote Queensland (97% of state land area)
  - Grid challenges: voltage drop, long feeders, reliability in storms/bushfires
  - Battery value prop: backup power + reliability + energy independence

**Market Strategy Insights:**
- Regional cities (Tier 2) = urban density + lower competition + stronger reliability pitch
- Toowoomba is "regional" by network operator but urban by character (perfect hybrid)
- Word-of-mouth spreads faster in tight-knit regional communities
- Federal battery rebate (30% off) + mandatory VPP = perfect timing for regional expansion

**Technical Learnings:**
- Network operator boundaries don't align perfectly with postcodes (some boundary zones)
- Postcode-based classification is pragmatic but approximate (would be better with GIS polygons)
- Suburb names in coordinate datasets are often wrong (alphabetically-first locality, not actual area)
- 4350 initially misclassified as Energex due to postcode range being too broad

**Challenges faced:**
- NEM regional zone GeoJSON not readily available from AEMO
- Used Energex/Ergon boundaries as proxy for network analysis
- Postcode range classification required manual verification against known service territories
- Coordinate dataset suburb labels misleading (ignore them, trust postcode numbers)

**Resources used:**
- Energex/Ergon service territory documentation
- Queensland Government Open Data Portal (Ergon GIS data)
- Manual verification of network boundaries using energy retailer websites
- AEMO market documentation for understanding NEM zones vs distribution networks

**Data Quality Notes:**
- Battery penetration varies significantly by postcode (2-15% range)
- Some high-solar postcodes show surprisingly low battery uptake (opportunity)
- Regional cities show lower average penetration than metro but more variation
- Commercial/industrial postcodes harder to classify (mixed use, multiple NMIs)

**Next steps:**
- Refine postcode classification ranges (4350 moved from Energex to Ergon)
- Add network constraint overlay (DAPR data from Energex/Ergon if available)
- Build Power BI dashboard with network zone filters
- Protocol analysis notebook: does device fragmentation differ by network zone?
- Create exportable postcode targeting list for battery installers

---

### Feb 19 - Documentation & Week 1 Wrap-up

**What I did:**
- Updated learning log with all technical findings
- Updated resources.md with technical notes and data sources
- Created LinkedIn posts for Week 1 checkpoint
- Prepared Git commit for Week 1 completion

**Reflections on Week 1:**
- Moved from "just analyzing data" to "actionable market intelligence"
- Understanding real-world context (network operators, grid challenges) makes analysis meaningful
- Data-driven market segmentation (regional cities) is more valuable than generic insights
- GitHub version control + documentation = professional portfolio standard
- Battery penetration % is more interesting business metric than total capacity numbers

**Skills developed:**
- Python: pandas aggregation, plotly mapping, data cleaning pipelines
- Geographic analysis: postcode classification, coordinate merging, spatial clustering
- Market analysis: segmentation, opportunity sizing, value proposition mapping
- Documentation: learning logs, technical notes, resource management
- Communication: translating technical findings into business insights

**What worked well:**
- Iterative notebook development (02 → 03 → 04 building on each other)
- Using enriched CSV files to pass data between notebooks (clean workflow)
- Documenting issues and solutions in learning log (helps recall)
- Asking clarifying questions before building (avoided wasted work)

**What I'd do differently:**
- Verify network operator boundaries BEFORE building classification logic
- Check coordinate dataset suburb labels earlier (would have saved confusion)
- Create data dictionary upfront mapping AEMO column names to readable aliases
- Test classification logic on known postcodes before running full dataset

**Preparation for Week 2:**
- Week 1 established foundation: data loaded, cleaned, mapped, segmented
- Week 2 focus: network constraints, protocol analysis, Power BI dashboard
- LinkedIn presence: 2 posts planned (Week 1 checkpoint + regional cities insight)
- Portfolio pieces ready: 3 Jupyter notebooks, interactive maps, market analysis

---

**Status:** Week 1 Complete ✓

**Next steps:**
- Add NEM regional zone overlay to maps
- Cross-reference with Ergon/Energex network constraint data
- Begin protocol analysis notebook
- Build Power BI dashboard from enriched CSV