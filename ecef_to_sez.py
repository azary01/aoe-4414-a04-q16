# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Converts an ECEF position to SEZ coordinates
# Parameters:
#  o_x_km: x coordinate of the ground station in ECEF
#  o_y_km: y coordinate of the ground station in ECEF
#  o_z_km: z coordinate of the ground station in ECEF
#  x_km: x coordinate of the object in ECEF
#  y_km: y coordinate of the object in ECEF
#  z_km: z coordinate of the object in ECEF
# Output:
#  Displays the objects SEZ coordinates relative to the ground station
#
# Written by Austin Zary
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

## calc_denom
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-ecc**2.0 * math.sin(lat_rad)**2.0)

# initialize script arguments
o_x_km = float('nan') # x coordinate of the ground station in ECEF
o_y_km = float('nan') # y coordinate of the ground station in ECEF
o_z_km = float('nan') # z coordinate of the ground station in ECEF
x_km = float('nan') # x coordinate of the object in ECEF
y_km = float('nan') # y coordinate of the object in ECEF
z_km = float('nan') # z coordinate of the object in ECEF

# parse script arguments
if len(sys.argv)==7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
    print(\
        'Usage: '\
        'python3 arg1 arg2 ...'\
    )
    exit()

# write script below this line

# Calculate distance from the ground station in ECEF coordinates:
x_local = x_km - o_x_km
y_local = y_km - o_y_km
z_local = z_km - o_z_km

# Find the lattitude and longitude of the ground station:
# calculate longitude
lon_rad = math.atan2(o_y_km,o_x_km)

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1

# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

# Calculate the SEZ coordinates:
s_km = (x_local*math.cos(lon_rad) + y_local*math.sin(lon_rad))*math.sin(lat_rad) - z_local*math.cos(lat_rad)
e_km = -x_local*math.sin(lon_rad) + y_local*math.cos(lon_rad)
z_km = (x_local*math.cos(lon_rad) + y_local*math.sin(lon_rad))*math.cos(lat_rad) + z_local*math.sin(lat_rad)

# Output:
print(s_km)
print(e_km)
print(z_km)