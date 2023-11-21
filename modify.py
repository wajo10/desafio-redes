from ncclient import manager
import xmltodict

# Configuración de conexión NETCONF
host = 'sandbox-iosxe-latest-1.cisco.com'
port = 830  # Puerto NETCONF típico
username = 'admin'
password = 'C1sco12345'

# Plantilla para cambiar la descripción de la interfaz
config_template = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <GigabitEthernet>
                <name>2</name>
                <description>Network Interface</description>
            </GigabitEthernet>
        </interface>
    </native>
</config>
'''


# Conexión NETCONF
with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as m:
    # Editar configuración
    netconf_reply = m.edit_config(target='running', config=config_template)

    # Imprimir respuesta
    print(xmltodict.parse(netconf_reply.xml))
