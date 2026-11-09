# Disdrometer_Processing
Process disdrometer data from a parsevel laser disdrometer


## Field Campaigns
- WFIP-3, 2024-2025
  - disdrometers installed at 3 sites: "ASIT", "BARG", "NANT" (asit.ld.z01.b1, asit.ld.z02.b1, barg.ld.z01.b1, barg.ld.z02.b1, nant.ld.z01.b1)
    - ASIT & BARG had 2 disdrometers installed perpendicular to each other
    - NANT had a single disdrometer installed at a N-S orientation
    - winds from lidars at 100m at each site were used to create a merged product
    - DQ corrections applied and optionally merging if 2 disdrometers present (asit.ldmerge.z01.c0, nant.ldmerge.z01.c0, barg.ldmerge.z01.c0)
- AWAKEN, 2022-2024
  - disdrometers installed at 3 sites: SH, SA1, and ST (at hub height on turbine H08) (sa1.ld.z01.b1, sa1.ld.z02.b1, sh.ld.z01.b1, sh.ld.z02.b1, sat.ld.z01.b1)
  - SH and SA1 had 2 disdrometers installed perpendicular to each other, two surface met stations used to get surface wind direction (sa1.met.z02 & sh.met.z01)
  - ST had a single disdrometer installed on the hub, which rotated with the turbine's orientation (traditionally wind direction at hub height)
  - when winds are from the south, sa1 is the inflow site unimpeded by turbines and sh is the outflow site)
  - when processed will have names like (sa1.ldmerge.z01.c0, sh.ldmerge.z01.c0, sat.ldmerge.z01.c0)
 
## Processing
- 00 files are the original text files recorded by the instrument, b1 are processed into daily netcdf files. The original b1 files omit the spectral data. Reprocessed b1 files contain the spectral data for droplet size and fall speed.
- depending on site set up, one or two disdrometers, if only one its installed N-S oriented (z01), if two z01 is N-S and z02 is E-W
- merge based on wind direction, using 90 deg quadrants to select the disdrometer. Generally precipitation cells move in one direction per event, so this is fine.
- Precipitation events are defined as achieving an intensity greater than 0.01 mm/hr
- Events are separated by 10 minutes of consecutive no rain
- Data recorded at 0.067 hertz, processed data aggregated to 1 minute intervals
- Correct for shattering and false drops using the methods in [Tokay et al 2013](https://journals.ametsoc.org/view/journals/atot/30/8/jtech-d-12-00163_1.xml)
- Found under the name LD_merge on the [DOE Wind Data Hub](https://wdh.energy.gov/data) 
    
