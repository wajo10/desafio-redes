import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ncclient import manager
import difflib

# Device connection details
HOST = 'sandbox-iosxe-latest-1.cisco.com'
PORT = 830
USER = 'admin'
PASS = 'C1sco12345'


# Function to connect to the device
def connect_to_device(host, port, user, password):
    return manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False)


# Function to get the current configuration
def get_current_config(m):
    return m.get_config(source='running').xml


def format_xml(xml_string):
    """ Formatea el XML para una comparación uniforme. """
    tree = ET.ElementTree(ET.fromstring(xml_string))
    for elem in tree.iter():
        if "message-id" in elem.attrib:
            del elem.attrib["message-id"]
    rough_string = ET.tostring(tree.getroot(), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def compare_configs_and_print_diff(old_config, new_config):
    old_config_formatted = format_xml(old_config)
    new_config_formatted = format_xml(new_config)

    if old_config_formatted != new_config_formatted:
        old_config_lines = old_config_formatted.splitlines()
        new_config_lines = new_config_formatted.splitlines()
        diff = difflib.unified_diff(old_config_lines, new_config_lines)
        diffStr = list(diff)


        # Save on file
        with open('logfile.txt', 'w') as f:
            f.write('\n'.join(diffStr))
            print('Diferencias encontradas:\n' + '\n'.join(diffStr))

        return True

    return False


# Function to monitor and alert
def monitor_and_alert():
    last_config = None
    while True:
        with connect_to_device(HOST, PORT, USER, PASS) as m:
            current_config = get_current_config(m)
            if last_config and compare_configs_and_print_diff(last_config, current_config):
                print("Configuration has changed!")
            else:
                print("Configuration has not changed!")
                # print("Current config: \n{}".format(current_config))

            last_config = current_config
        time.sleep(6)  # Wait for 60 seconds before checking again


# Run the monitoring function
monitor_and_alert()
