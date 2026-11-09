#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import warnings
from datetime import timedelta
import xarray as xr
import glob
warnings.filterwarnings('ignore')

# Find days where ALL three datasets have data, then mask to those days only
def get_valid_days(ds, var='rain_intensity'):
    """Return a set of dates (day resolution) where the variable has at least one non-NaN value."""
    data = ds[var] if var in ds else next(iter(ds.data_vars.values()), None)
    if data is None:
        return set()
    # Collapse any non-time dims, check for any valid value per day
    daily_valid = (
        np.isfinite(data.values).any(axis=tuple(range(1, data.ndim)))
        if data.ndim > 1 else np.isfinite(data.values)
    )
    times = ds.time.values
    days = pd.to_datetime(times).normalize()  # truncate to date
    return set(days[daily_valid])

# Build a boolean mask for each dataset's time coordinate
def mask_to_common_days(ds, common_days):
    common_days = pd.DatetimeIndex(common_days).normalize()
    time_days = ds["time"].dt.floor("D")
    mask = time_days.isin(common_days)
    ds_filtered = ds.where(mask, drop=True)
    return ds_filtered

def main():
    # Define datasets to load: (name, glob_pattern, variable, height_level, y_offset, color)
    datasets_config = [
        ('Nant Winds', '/qfs/people/gold396/ORACLE/wfip3/nant.lidar.10min.z01.c1/*', 'wd', 100, 1.0, 'blue'),
        ('Nant Rain', '/rcfs/projects/oracle/gold396/Disdrometer_Data/wfip3/nant.ld.z01.b1/*', 'rain_intensity', None, 0.5, 'blue'),
    ]

    # Load all datasets efficiently
    datasets = {}
    for name, pattern, _, _, _, _ in datasets_config:
        try:
            ds = xr.open_mfdataset(sorted(glob.glob(pattern)), combine='by_coords')
            datasets[name] = ds
            print(f"✓ Loaded {name}: {len(ds.time)} time steps")
        except Exception as e:
            print(f"✗ Failed to load {name}: {e}")




    wind_days = get_valid_days(datasets['Nant Winds'], 'wd')
    rain_days = get_valid_days(datasets['Nant Rain'], 'rain_intensity')

    common_days = wind_days & rain_days
    print(f"Nant Winds valid days:  {len(wind_days)}")
    print(f"Nant Rain valid days: {len(rain_days)}")
    print(f"Overlapping days:       {len(common_days)}")

    datasets['Nant Winds']  = mask_to_common_days(datasets['Nant Winds'],  common_days)
    datasets['Nant Rain'] = mask_to_common_days(datasets['Nant Rain'], common_days)

    print(f"\nAfter masking:")
    for name in ['Nant Winds', 'Nant Rain']:
        print(f"  {name}: {len(datasets[name].time)} time steps")

    del wind_days, rain_days, common_days

    # Make sure eveything has same time coordinate
    datasets['Nant Winds'] = datasets['Nant Winds'].reindex(time=datasets["Nant Rain"]["time"], method="ffill")

    WD = datasets['Nant Winds']['wd'].sel(height=100, method = 'nearest').compute()

    ds1 = datasets["Nant Rain"]   # Dataset

    # # Boolean masks (True where condition met)
    # mask_ns = ((WD > 315) | (WD < 45) | ((WD > 135) & (WD < 225)))
    # mask_ew = (((WD > 45) & (WD < 135)) | ((WD > 225) & (WD < 315)))

    new_ds = ds1.copy()
    new_ds["wind_direction"] = WD
    new_ds["wind_speed"] = datasets["Nant Winds"]["ws"].sel(height=100, method='nearest').compute()
    new_ds["vertical_wind_speed"] = datasets["Nant Winds"]["w"].sel(height=100, method='nearest').compute()

    output_dir = '/rcfs/projects/oracle/gold396/NANT'
    os.makedirs(output_dir, exist_ok=True)

    # Get sorted unique dates from new_ds
    dates = sorted(set(pd.to_datetime(new_ds.time.values).normalize()))

    for date in dates:
        date_str = pd.Timestamp(date).strftime('%Y%m%d')
        
        # Extract all data for this day from new_ds
        day_ds = new_ds.sel(time=slice(date, date + timedelta(days=1) - timedelta(seconds=1)))
        
        # Compute to materialize Dask arrays before saving
        day_ds = day_ds.compute()
        
        # Save to daily file
        output_file = os.path.join(output_dir, f"nant_merged_{date_str}.nc")
        day_ds.to_netcdf(output_file)
        print(f"✓ Saved {date_str}: {output_file}")

    print(f"\nTotal daily files saved: {len(dates)}")


    # The entire script content should be indented under this function
    # (from line 11 to line 112)
    pass

if __name__ == "__main__":
    main()
