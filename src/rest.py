import requests, configparser, logging, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.captureWarnings(True)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # logging.info(idrac_state)
        return idrac_state
    else:
        return "null"

def fetch_indicator_led_state():
    system_url = f"{url}Systems/System.Embedded.1"
    system_response = session.get(system_url)
    if system_response.status_code == 200:
        system_data = system_response.json()
        indicator_led_state = system_data['IndicatorLED']
        # logging.info(indicator_led_state)
        return indicator_led_state
    else:
        return "null"

# AverageConsumedWatts or PowerConsumedWatts
def fetch_power_metrics(type):
    power_url = f"{url}Chassis/System.Embedded.1/Power"
    power_response = session.get(power_url)
    if type == "AverageConsumedWatts":
        if power_response.status_code == 200:
            power_data = power_response.json()
            power_metrics = power_data["PowerControl"][0]["PowerMetrics"]["AverageConsumedWatts"]
            # logging.info(power_metrics)
            return power_metrics
        else:
            return None
    if type == "PowerConsumedWatts":
        if power_response.status_code == 200:
            power_data = power_response.json()
            power_metrics = power_data["PowerControl"][0]["PowerConsumedWatts"]
            # logging.info(power_metrics)
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
        # logging.info(thermal_temp)
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
            # logging.info(fan_speed)
            return fan_speed
        elif data_type == "PWM":
            fan_speed = thermal_data["Oem"]["Dell"]["FanPWM"]
            # logging.info(fan_speed)
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
            # logging.info(model)
            return model
        elif type == "SerialNumber":
            serial_number = system_data["SerialNumber"]
            # logging.info(serial_number)
            return serial_number
        elif type == "PowerState":
            power_state = system_data["PowerState"]
            # logging.info(power_state)
            return power_state
        elif type == "UUID":
            uuid = system_data["UUID"]
            # logging.info(uuid)
            return uuid
        elif type == "Manufacturer":
            manufacturer = system_data["Manufacturer"]
            # logging.info(manufacturer)
            return manufacturer
        elif type == "AssetTag":
            asset_tag = system_data["AssetTag"]
            # logging.info(asset_tag)
            return asset_tag
        elif type == "SKU":
            bios_version = system_data["SKU"]
            # logging.info(bios_version)
            return bios_version
        elif type == "PowerState":
            power_state = system_data["PowerState"]
            # logging.info(power_state)
            return power_state
        elif type == "PartNumber":
            part_number = system_data["PartNumber"]
            # logging.info(part_number)
            return part_number
        else:
            # logging.info("null")
            return "null"
    else:
        # logging.info("null")
        return "null"


# PS1Current1, PS2Current2, PS1Voltage, PS2Voltage, SystemBoardPwrConsumption, CPUVCOREVR, Fan.Embedded.1A, Fan.Embedded.1B, CPU1Temp, SystemBoardInletTemp, SystemBoardExhaustTemp
# PSU.Slot.1_MaximumFrequency, PSU.Slot.2_MaximumFrequency, PSU.Slot.1_InputPower, PSU.Slot.2_InputPower, PSU.Slot.1_OutputPower, PSU.Slot.2_OutputPower, SystemAirFlow
def fetch_sensor_metrics(sensor_id):
    sensor_url = f"{url}Chassis/System.Embedded.1/Sensors/{sensor_id}"
    sensor_response = session.get(sensor_url)
    if sensor_response.status_code == 200:
        sensor_data = sensor_response.json()
        sensor_reading = sensor_data["Reading"]
        # logging.info(sensor_reading)
        return sensor_reading
    else:
        return None
    
def fetch_intrusion_metrics():
    intrusion_url = f"{url}Chassis/System.Embedded.1/Security"
    intrusion_response = session.get(intrusion_url)
    if intrusion_response.status_code == 200:
        intrusion_data = intrusion_response.json()
        intrusion_status = intrusion_data["IntrusionSensor"]
        # logging.info(intrusion_status)
        return intrusion_status
    else:
        return None
    


# try: 
#     fetch_idrac_state()
#     fetch_temperature_metrics("Internal")
#     fetch_temperature_metrics("Intake")
#     fetch_temperature_metrics("Exhaust")
#     fetch_power_metrics("AverageConsumedWatts")
#     fetch_power_metrics("PowerConsumedWatts")
#     fetch_fan_metrics("1A", "PWM")
#     fetch_fan_metrics("1B", "RPM")

#     fetch_system_info("Model")
#     fetch_system_info("SerialNumber")
#     fetch_system_info("PowerState")
#     fetch_system_info("UUID")
#     fetch_system_info("Manufacturer")
#     fetch_system_info("AssetTag")
#     fetch_system_info("SKU")
#     fetch_system_info("PowerState")
#     fetch_system_info("PartNumber")

#     fetch_sensor_metrics("PS1Current1")
#     fetch_sensor_metrics("PS2Current2")
#     fetch_sensor_metrics("PS1Voltage")
#     fetch_sensor_metrics("PS2Voltage")
#     fetch_sensor_metrics("SystemBoardPwrConsumption")
#     fetch_sensor_metrics("CPUVCOREVR")
#     fetch_sensor_metrics("Fan.Embedded.1A")
#     fetch_sensor_metrics("Fan.Embedded.1B")
#     fetch_sensor_metrics("CPU1Temp")
#     fetch_sensor_metrics("SystemBoardInletTemp")
#     fetch_sensor_metrics("SystemBoardExhaustTemp")
#     fetch_sensor_metrics("PSU.Slot.1_MaximumFrequency")
#     fetch_sensor_metrics("PSU.Slot.2_MaximumFrequency")
#     fetch_sensor_metrics("PSU.Slot.1_InputPower")
#     fetch_sensor_metrics("PSU.Slot.2_InputPower")
#     fetch_sensor_metrics("PSU.Slot.1_OutputPower")
#     fetch_sensor_metrics("PSU.Slot.2_OutputPower")
#     fetch_sensor_metrics("SystemAirFlow")

# except requests.exceptions.RequestException as e:
#     exit(f"Error creating session: {e}")

