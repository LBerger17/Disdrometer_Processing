# Disdrometer_Processing
Process disdrometer data from a parsevel laser disdrometer


## Field Campaigns
- WFIP-3, 2024-2025
  - disdrometers installed at 3 sites: "ASIT", "BARG", "NANT"
    - ASIT & BARG had 2 disdrometers installed perpendicular to each other
    - NANT had a single disdrometer installed at a N-S orientation
    - winds from lidars at 100m at each site were used to create a merged product
- AWAKEN, 2022-2024
  - disdrometers installed at 3 sites: SH, SA1, and ST (at hub height on turbine H08)
  - SH and SA1 had 2 disdrometers installed perpendicular to each other, two surface met stations used to get surface wind direction (sa1.met.z02 & sh.met.z01)
  - ST had a single disdrometer installed on the hub, which rotated with the turbine's orientation (traditionally wind direction at hub height)
 
## Processing
- depending on site set up, one or two disdrometers, if only one its installed N-S oriented (z01), if two z01 is N-S and z02 is E-W
- merge based on wind direction, using 90 deg quadrants to select the disdrometer. Generally precipitation cells move in one direction per event, so this is fine.
- Precipitation events are defined as achieving an intensity greater than 0.01 mm/hr
- Events are separated by 10 minutes of consecutive no rain
- Data recorded at 0.067 hertz, processed data aggregated to 1 minute intervals
- Correct for shattering and false drops using the methods in Tokay et al 2013
- Found under the name LD_merge on the [DOE Wind Data Hub](https://wdh.energy.gov/data) 
    
