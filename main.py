import time, configparser
from prometheus_client import start_http_server, Gauge
from src import rest

config = configparser.ConfigParser()
config.read('config.ini')

timeout = int(config['exporter']['timeout'].replace('"', ''))
port = int(config['exporter']['port'].replace('"', ''))

idrac_health = Gauge('idrac_health_status', 'iDRAC health status', ['status'])
avg_power = Gauge('idrac_average_power_watts', 'Average power consumption in watts')
power_consumed = Gauge('idrac_power_consumed_watts', 'Current power consumption in watts')
internal_temp = Gauge('idrac_internal_temp_celsius', 'Internal temperature in Celsius')
intake_temp = Gauge('idrac_intake_temp_celsius', 'Intake temperature in Celsius')
exhaust_temp = Gauge('idrac_exhaust_temp_celsius', 'Exhaust temperature in Celsius')

system_model = Gauge('idrac_system_model', 'System model')
system_serial = Gauge('idrac_system_serial', 'System serial number')
system_power_state = Gauge('idrac_system_power_state', 'System power state')
system_uuid = Gauge('idrac_system_uuid', 'System UUID')
system_manufacturer = Gauge('idrac_system_manufacturer', 'System manufacturer')
system_asset_tag = Gauge('idrac_system_asset_tag', 'System asset tag')
system_sku = Gauge('idrac_system_sku', 'System SKU')
system_part_number = Gauge('idrac_system_part_number', 'System part number')
system_power_state = Gauge('idrac_system_power_state_info', 'System power state info')

sensor_ps1_current = Gauge('idrac_sensor_ps1_current', 'PS1 Current')
sensor_ps2_current = Gauge('idrac_sensor_ps2_current', 'PS2 Current')
sensor_ps1_voltage = Gauge('idrac_sensor_ps1_voltage', 'PS1 Voltage')
sensor_ps2_voltage = Gauge('idrac_sensor_ps2_voltage', 'PS2 Voltage')
sensor_board_power = Gauge('idrac_sensor_board_power', 'System Board Power Consumption')
sensor_cpu_vcore = Gauge('idrac_sensor_cpu_vcore', 'CPU VCORE Voltage')
sensor_fan_1a = Gauge('idrac_sensor_fan_1a', 'Fan Embedded 1A Speed')
sensor_fan_1b = Gauge('idrac_sensor_fan_1b', 'Fan Embedded 1B Speed')
sensor_cpu1_temp = Gauge('idrac_sensor_cpu1_temp', 'CPU1 Temperature')
sensor_board_inlet_temp = Gauge('idrac_sensor_board_inlet_temp', 'System Board Inlet Temperature')
sensor_board_exhaust_temp = Gauge('idrac_sensor_board_exhaust_temp', 'System Board Exhaust Temperature')
sensor_psu1_max_freq = Gauge('idrac_sensor_psu1_max_freq', 'PSU Slot 1 Maximum Frequency')
sensor_psu2_max_freq = Gauge('idrac_sensor_psu2_max_freq', 'PSU Slot 2 Maximum Frequency')
sensor_psu1_input_power = Gauge('idrac_sensor_psu1_input_power', 'PSU Slot 1 Input Power')
sensor_psu2_input_power = Gauge('idrac_sensor_psu2_input_power', 'PSU Slot 2 Input Power')
sensor_psu1_output_power = Gauge('idrac_sensor_psu1_output_power', 'PSU Slot 1 Output Power')
sensor_psu2_output_power = Gauge('idrac_sensor_psu2_output_power', 'PSU Slot 2 Output Power')
sensor_system_airflow = Gauge('idrac_sensor_system_airflow', 'System Air Flow')


    # fetch_idrac_state()
    # fetch_temperature_metrics("Internal")
    # fetch_temperature_metrics("Intake")
    # fetch_temperature_metrics("Exhaust")
    # fetch_power_metrics("AverageConsumedWatts")
    # fetch_power_metrics("PowerConsumedWatts")
    # fetch_fan_metrics("1A", "PWM")
    # fetch_fan_metrics("1B", "RPM")

    # fetch_system_info("Model")
    # fetch_system_info("SerialNumber")
    # fetch_system_info("PowerState")
    # fetch_system_info("UUID")
    # fetch_system_info("Manufacturer")
    # fetch_system_info("AssetTag")
    # fetch_system_info("SKU")
    # fetch_system_info("PowerState")
    # fetch_system_info("PartNumber")

    # fetch_sensor_metrics("PS1Current1")
    # fetch_sensor_metrics("PS2Current2")
    # fetch_sensor_metrics("PS1Voltage")
    # fetch_sensor_metrics("PS2Voltage")
    # fetch_sensor_metrics("SystemBoardPwrConsumption")
    # fetch_sensor_metrics("CPUVCOREVR")
    # fetch_sensor_metrics("Fan.Embedded.1A")
    # fetch_sensor_metrics("Fan.Embedded.1B")
    # fetch_sensor_metrics("CPU1Temp")
    # fetch_sensor_metrics("SystemBoardInletTemp")
    # fetch_sensor_metrics("SystemBoardExhaustTemp")
    # fetch_sensor_metrics("PSU.Slot.1_MaximumFrequency")
    # fetch_sensor_metrics("PSU.Slot.2_MaximumFrequency")
    # fetch_sensor_metrics("PSU.Slot.1_InputPower")
    # fetch_sensor_metrics("PSU.Slot.2_InputPower")
    # fetch_sensor_metrics("PSU.Slot.1_OutputPower")
    # fetch_sensor_metrics("PSU.Slot.2_OutputPower")
    # fetch_sensor_metrics("SystemAirFlow")

def update_metrics():
    # Fetch and update iDRAC health status
    state = rest.fetch_idrac_state()  # returns a health status string
    # Convert state to a numeric value (for example: "OK" => 1, else 0)
    health_value = 1 if state.lower() in ['ok', 'optimal'] else 0
    idrac_health.labels(status=state).set(health_value)


    avg_power_value = rest.fetch_power_metrics("AverageConsumedWatts")
    power_consumed_value = rest.fetch_power_metrics("PowerConsumedWatts")
    if avg_power_value is not None:
        avg_power.set(avg_power_value)
    if power_consumed_value is not None:
        power_consumed.set(power_consumed_value)

    internal = rest.fetch_temperature_metrics("Internal")
    intake = rest.fetch_temperature_metrics("Intake")
    exhaust = rest.fetch_temperature_metrics("Exhaust")
    if internal is not None:
        internal_temp.set(internal)
    if intake is not None:
        intake_temp.set(intake)
    if exhaust is not None:
        exhaust_temp.set(exhaust)

    model = rest.fetch_system_info("Model")
    serial = rest.fetch_system_info("SerialNumber")
    power_state = rest.fetch_system_info("PowerState")
    uuid = rest.fetch_system_info("UUID")
    manufacturer = rest.fetch_system_info("Manufacturer")
    asset_tag = rest.fetch_system_info("AssetTag")
    sku = rest.fetch_system_info("SKU")
    part_number = rest.fetch_system_info("PartNumber")
    power_state_info = rest.fetch_system_info("PowerState")

    if model is not None:
        system_model.set(model)
    if serial is not None:
        system_serial.set(serial)
    if power_state is not None:
        system_power_state.set(power_state)
    if uuid is not None:
        system_uuid.set(uuid)
    if manufacturer is not None:
        system_manufacturer.set(manufacturer)
    if asset_tag is not None:
        system_asset_tag.set(asset_tag)
    if sku is not None:
        system_sku.set(sku)
    if part_number is not None:
        system_part_number.set(part_number)
    if power_state_info is not None:
        system_power_state.set(power_state_info)
    
    ps1_current = rest.fetch_sensor_metrics("PS1Current1")
    ps2_current = rest.fetch_sensor_metrics("PS2Current2")
    ps1_voltage = rest.fetch_sensor_metrics("PS1Voltage")
    ps2_voltage = rest.fetch_sensor_metrics("PS2Voltage")
    board_power = rest.fetch_sensor_metrics("SystemBoardPwrConsumption")
    cpu_vcore = rest.fetch_sensor_metrics("CPUVCOREVR")
    fan_1a = rest.fetch_sensor_metrics("Fan.Embedded.1A")
    fan_1b = rest.fetch_sensor_metrics("Fan.Embedded.1B")
    cpu1_temp = rest.fetch_sensor_metrics("CPU1Temp")
    board_inlet_temp = rest.fetch_sensor_metrics("SystemBoardInletTemp")
    board_exhaust_temp = rest.fetch_sensor_metrics("SystemBoardExhaustTemp")
    psu1_max_freq = rest.fetch_sensor_metrics("PSU.Slot.1_MaximumFrequency")
    psu2_max_freq = rest.fetch_sensor_metrics("PSU.Slot.2_MaximumFrequency")
    psu1_input_power = rest.fetch_sensor_metrics("PSU.Slot.1_InputPower")
    psu2_input_power = rest.fetch_sensor_metrics("PSU.Slot.2_InputPower")
    psu1_output_power = rest.fetch_sensor_metrics("PSU.Slot.1_OutputPower")
    psu2_output_power = rest.fetch_sensor_metrics("PSU.Slot.2_OutputPower")
    system_airflow = rest.fetch_sensor_metrics("SystemAirFlow")
    if ps1_current is not None:
        sensor_ps1_current.set(ps1_current)
    if ps2_current is not None:
        sensor_ps2_current.set(ps2_current)
    if ps1_voltage is not None:
        sensor_ps1_voltage.set(ps1_voltage)
    if ps2_voltage is not None:
        sensor_ps2_voltage.set(ps2_voltage)
    if board_power is not None:
        sensor_board_power.set(board_power)
    if cpu_vcore is not None:
        sensor_cpu_vcore.set(cpu_vcore)
    if fan_1a is not None:
        sensor_fan_1a.set(fan_1a)
    if fan_1b is not None:
        sensor_fan_1b.set(fan_1b)
    if cpu1_temp is not None:
        sensor_cpu1_temp.set(cpu1_temp)
    if board_inlet_temp is not None:
        sensor_board_inlet_temp.set(board_inlet_temp)
    if board_exhaust_temp is not None:
        sensor_board_exhaust_temp.set(board_exhaust_temp)
    if psu1_max_freq is not None:
        sensor_psu1_max_freq.set(psu1_max_freq)
    if psu2_max_freq is not None:
        sensor_psu2_max_freq.set(psu2_max_freq)
    if psu1_input_power is not None:
        sensor_psu1_input_power.set(psu1_input_power)
    if psu2_input_power is not None:
        sensor_psu2_input_power.set(psu2_input_power)
    if psu1_output_power is not None:
        sensor_psu1_output_power.set(psu1_output_power)
    if psu2_output_power is not None:
        sensor_psu2_output_power.set(psu2_output_power)
    if system_airflow is not None:
        sensor_system_airflow.set(system_airflow)
    

if __name__ == '__main__':
    # Start Prometheus exporter server on port 8000
    start_http_server(port)
    print(f"Prometheus exporter running on http://localhost:{port}/metrics")
    
    # Periodically update metrics every 30 seconds
    while True:
        update_metrics()
        time.sleep(timeout)