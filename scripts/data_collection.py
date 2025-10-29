import pandas as pd
import numpy as np
import datetime

print("Starting data simulation...")

# --- Configuration ---
N_ROWS = 5000       # Total number of sensor readings to simulate
RIGS = ['RIG-001', 'RIG-002']
WELL = 'WELL-101A'
START_DATE = datetime.datetime(2025, 10, 25, 6, 0, 0)

# --- Data Generation ---
data = []
current_depth_rig1 = 0
current_depth_rig2 = 0

for i in range(N_ROWS):
    # Alternate between rigs
    rig_id = RIGS[i % 2]

    # Simulate time passing
    timestamp = START_DATE + datetime.timedelta(minutes=i * 5)

    # Simulate data for each rig
    if rig_id == 'RIG-001':
        # Rig 1 drills a bit faster and more consistently
        rop = np.random.normal(loc=30, scale=5)  # Avg 30 m/hr
        wob = np.random.normal(loc=15, scale=2)  # Avg 15 tons
        torque = np.random.normal(loc=20, scale=3) # Avg 20 kNm
        mud_pressure = np.random.normal(loc=2500, scale=100) # Avg 2500 psi
        current_depth_rig1 += rop * (5/60) # ROP is in m/hr, timestamp is 5 min
        depth = current_depth_rig1
    else:
        # Rig 2 is a bit more erratic
        rop = np.random.normal(loc=25, scale=8)  # Avg 25 m/hr, more variance
        wob = np.random.normal(loc=18, scale=3)  # Avg 18 tons
        torque = np.random.normal(loc=22, scale=4) # Avg 22 kNm
        mud_pressure = np.random.normal(loc=2600, scale=150) # Avg 2600 psi
        current_depth_rig2 += rop * (5/60)
        depth = current_depth_rig2

    # Ensure no negative values (common cleaning step we'll do in ETL, but good to simulate)
    rop = max(0, rop)

    # Append the reading
    data.append({
        'timestamp': timestamp,
        'rig_id': rig_id,
        'well_id': WELL,
        'depth_m': depth,
        'rop_m_hr': rop,
        'wob_tons': wob,
        'torque_kNm': torque,
        'mud_pressure_psi': mud_pressure
    })

# --- Create DataFrame and Save ---
df = pd.DataFrame(data)

# Introduce some common "dirty data" problems for our ETL to solve
# 1. Add some missing values (e.g., sensor dropout)
df.loc[df.sample(frac=0.01).index, 'rop_m_hr'] = np.nan
# 2. Add some duplicated rows (e.g., data system glitch)
df = pd.concat([df, df.sample(n=50)])

# Save to CSV
# We save this in the parent directory (root) to be easily found by the notebook.
output_path = 'raw_sensor_data.csv'
df.to_csv(output_path, index=False)

print(f"Successfully generated {len(df)} rows of raw sensor data.")
print(f"Saved to '{output_path}'")
