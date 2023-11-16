import meraki
import os

# 5 GHz Radio Settings mismatch auto-audit for Meraki WLAN  - By Gabriel TOUBEAU (github.com/gabtoub)
 
# Get environment variable for API Key or prompt user and initialize connection to Dashboard

api_key = os.environ["MERAKI_API_KEY"]

if not api_key:
    api_key = input("No environment variable found - Please enter your API key: ")
dashboard = meraki.DashboardAPI(api_key,print_console=False)

# Get Organizations from Meraki Dashboard API

organizations = dashboard.organizations.getOrganizations()
for org in organizations:
    print(f"Name: {org['name']}, ID:{org['id']}")

# Display Networks from an Org ID
org_id = input("Please enter your Org ID: ")

# Get all Wireless devices in selected Organization
devices_list=dashboard.organizations.getOrganizationDevices(org_id,productTypes=["wireless"])

# Get Wireless Radio settings and status for each device
for dev in devices_list :
    dev_wireless_settings=dashboard.wireless.getDeviceWirelessRadioSettings(dev['serial'])
    dev_wireless_status=dashboard.wireless.getDeviceWirelessStatus(dev['serial'])
    # If there is a 5 GHz configured  channel, compare : 
    for bss in dev_wireless_status['basicServiceSets']:
        if bss['band'] == '5 GHz':
            # Compare with excluding when AutoRF set (none)
            if bss['channel'] != dev_wireless_settings['fiveGhzSettings']['channel'] and dev_wireless_settings['fiveGhzSettings']['channel'] is not None :
                print(f"Mismatch on 5 GHz radio : {dev['name']} - Config ch : {dev_wireless_settings['fiveGhzSettings']['channel']} - Actual ch : {bss['channel']} ")
            else :
                print (f"OK 5 GHz on : {dev['name']}")
            # Stop on first case
            break
 