import requests, configparser, logging
from requests.auth import HTTPBasicAuth

logging.captureWarnings(True)

config = configparser.ConfigParser()
config.read('config.ini')

idrac_ip = config['idrac1']['ip'].replace('"', '')
idrac_user = config['idrac1']['user'].replace('"', '')
idrac_pass = config['idrac1']['pass'].replace('"', '')

url = f"https://{idrac_ip}/redfish/v1/"

session = requests.Session()
session.auth = (idrac_user, idrac_pass)
session.verify = False

def fetch_idrac_state():
    system_url = f"{url}Systems/System.Embedded.1"
    system_response = session.get(system_url)
    if system_response.status_code == 200:
        system_data = system_response.json()
        idrac_state = system_data['Status']['Health']
        print(idrac_state)
        return idrac_state
    else:
        print("null")
        return "null"


# AverageConsumedWatts or PowerConsumedWatts
def fetch_power_metrics(type):
    power_url = f"{url}Chassis/System.Embedded.1/Power"
    power_response = session.get(power_url)
    if type == "AverageConsumedWatts":
        if power_response.status_code == 200:
            power_data = power_response.json()
            power_metrics = power_data["PowerControl"][0]["PowerMetrics"]["AverageConsumedWatts"]
            print(power_metrics)
            return power_metrics
        else:
            return None
    if type == "PowerConsumedWatts":
        if power_response.status_code == 200:
            power_data = power_response.json()
            power_metrics = power_data["PowerControl"][0]["PowerConsumedWatts"]
            print(power_metrics)
            return power_metrics
        else:
            return None


# Internal, Intake, Exhaust
def fetch_temperature_metrics(probe):
    thermal_url = f"{url}Chassis/System.Embedded.1/ThermalSubsystem/ThermalMetrics"
    thermal_response = session.get(thermal_url)
    if thermal_response.status_code == 200:
        thermal_data = thermal_response.json()
        thermal_temp = thermal_data["TemperatureSummaryCelsius"][probe]["Reading"]
        print(thermal_temp)
        return thermal_temp
    else:
        return None

# 1A, 1B, or 1, 2 depending on chassis 
# RPM or PWM type
def fetch_fan_metrics(probe, data_type):
    thermal_url = f"{url}Chassis/System.Embedded.1/ThermalSubsystem/Fans/Fan.Embedded.{probe}"
    thermal_response = session.get(thermal_url)
    if thermal_response.status_code == 200:
        thermal_data = thermal_response.json()
        if data_type == "RPM":
            fan_speed = thermal_data["SpeedPercent"]["SpeedRPM"]
            print(fan_speed)
            return fan_speed
        elif data_type == "PWM":
            fan_speed = thermal_data["Oem"]["Dell"]["FanPWM"]
            print(fan_speed)
            return fan_speed
    else:
        return None
    
# Model, SerialNumber, PowerState, UUID, Manufacturer, AssetTag, SKU, BiosVersion
def fetch_system_info(type):
    system_url = f"{url}Systems/System.Embedded.1"
    system_response = session.get(system_url)
    if system_response.status_code == 200:
        system_data = system_response.json()
        if type == "Model":
            model = system_data["Model"]
            print(model)
            return model
        elif type == "SerialNumber":
            serial_number = system_data["SerialNumber"]
            print(serial_number)
            return serial_number
        elif type == "PowerState":
            power_state = system_data["PowerState"]
            print(power_state)
            return power_state
        elif type == "UUID":
            uuid = system_data["UUID"]
            print(uuid)
            return uuid
        elif type == "Manufacturer":
            manufacturer = system_data["Manufacturer"]
            print(manufacturer)
            return manufacturer
        elif type == "AssetTag":
            asset_tag = system_data["AssetTag"]
            print(asset_tag)
            return asset_tag
        elif type == "SKU":
            bios_version = system_data["SKU"]
            print(bios_version)
            return bios_version
        elif type == "PowerState":
            power_state = system_data["PowerState"]
            print(power_state)
            return power_state
        elif type == "PartNumber":
            part_number = system_data["PartNumber"]
            print(part_number)
            return part_number
        else:
            print("null")
            return "null"
    else:
        print("null")
        return "null"


fetch_idrac_state()
fetch_temperature_metrics("Internal")
fetch_temperature_metrics("Intake")
fetch_temperature_metrics("Exhaust")
fetch_power_metrics("AverageConsumedWatts")
fetch_power_metrics("PowerConsumedWatts")
fetch_fan_metrics("1A", "PWM")
fetch_fan_metrics("1B", "PWM")

fetch_system_info("Model")
fetch_system_info("SerialNumber")
fetch_system_info("PowerState")
fetch_system_info("UUID")
fetch_system_info("Manufacturer")
fetch_system_info("AssetTag")
fetch_system_info("SKU")
fetch_system_info("PowerState")
fetch_system_info("PartNumber")



