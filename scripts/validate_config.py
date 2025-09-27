import yaml
from jinja2 import Environment, FileSystemLoader

# --- Policy Definition ---
PROHIBITED_WORDS = ['insecure', 'legacy', 'temp']

print("--- Starting Validation ---")

# Load variables and template
with open('host_vars/csr-router-1.yml') as f:
    variables = yaml.safe_load(f)

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('interface_description.j2')

# Render the configuration
config = template.render(variables)

# --- Policy Check ---
print("Checking for prohibited words...")
description = variables.get('interface_desc', '').lower()
found_prohibited = [word for word in PROHIBITED_WORDS if word in description]

if found_prohibited:
    print(f"❌ VALIDATION FAILED: Prohibited word '{found_prohibited[0]}' found in description.")
    exit(1) # Cause the pipeline to fail

print("✅ Policy check passed.")
print("--- Validation Successful ---")
