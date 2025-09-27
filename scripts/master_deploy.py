# scripts/master_deploy.py

from ncclient import manager
from netmiko import ConnectHandler
import yaml
from jinja2 import Environment, FileSystemLoader
import sys

# --- This function contains the logic from your old 'deploy_full_config.py' ---
def deploy_netconf(device_config, device_creds):
    print("--- Deploying via NETCONF ---")
    env = Environment(loader=FileSystemLoader('../templates/'), trim_blocks=True, lstrip_blocks=True)
    # Uses the full config template
    template = env.get_template('full_config.j2')
    config_xml = template.render(device_config)
    
    print("Generated XML:\n", config_xml)
    with manager.connect(**device_creds, hostkey_verify=False) as m:
        reply = m.edit_config(target='running', config=config_xml)
        print("Device Reply:", reply)

def deploy_cli(device_config, device_creds):
    print("--- Deploying via CLI (Netmiko) ---")
    env = Environment(loader=FileSystemLoader('../templates/'), trim_blocks=True, lstrip_blocks=True)
    # Assumes a corresponding CLI template exists
    template = env.get_template('cli_config.j2')
    config_cli = template.render(device_config)
    
    print("Generated CLI:\n", config_cli)
    with ConnectHandler(**device_creds) as net_connect:
        output = net_connect.send_config_set(config_cli.splitlines())
        print("Device Output:", output)
        net_connect.save_config()

# --- Main Dispatcher Logic ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python master_deploy.py <device_name>")
        sys.exit(1)
        
    device_name = sys.argv[1]
    
    with open(f'../host_vars/{device_name}.yml') as f:
        device_config = yaml.safe_load(f)

    # In a real pipeline, these would come from a secure vault
    device_creds = {
        'host': device_config.get('management_ip'),
        'username': 'your_username',
        'password': 'your_password'
    }

    # Decide which function to call based on the YAML file
    if device_config.get('connection_type') == 'netconf':
        device_creds['port'] = 830
        device_creds['device_params'] = {'name': 'csr'}
        deploy_netconf(device_config, device_creds)
    elif device_config.get('connection_type') == 'cli':
        device_creds['device_type'] = 'cisco_ios'
        deploy_cli(device_config, device_creds)
    else:
        print(f"Error: Unknown connection_type for device {device_name}")
        sys.exit(1)

if __name__ == '__main__':
    main()