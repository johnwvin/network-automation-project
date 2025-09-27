import yaml
from jinja2 import Environment, FileSystemLoader
import sys

# --- Policy Definition ---
PROHIBITED_WORDS = ['insecure', 'legacy', 'temp']

print("--- Starting Validation ---")

# Load variables and template
with open('host_vars/csr-router-1.yml') as f:
    variables = yaml.safe_load(f)

# --- NEW AND IMPROVED POLICY CHECK ---
print("Checking for prohibited words in interface descriptions...")

# Get the list of interfaces from the YAML data
interface_list = variables.get('interfaces', [])

# Loop through each interface in the list
for interface in interface_list:
    description = interface.get('description', '').lower()
    
    # Check the current description for any prohibited words
    found_prohibited = [word for word in PROHIBITED_WORDS if word in description]
    
    if found_prohibited:
        interface_name = interface.get('name', 'Unknown')
        print(f"\n❌ VALIDATION FAILED on interface '{interface_name}':")
        print(f"   Found prohibited word '{found_prohibited[0]}' in description: '{interface.get('description')}'")
        sys.exit(1) # Cause the pipeline to fail

print("\n✅ All interface descriptions passed policy check.")
print("--- Validation Successful ---")