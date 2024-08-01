import pandas as pd
import random

# Define possible values for each field
chains = ['INPUT', 'FORWARD', 'OUTPUT']
protocols = ['tcp', 'udp']
actions = ['ACCEPT', 'DROP']

# Function to generate a random IP address
def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate a random port number
def generate_port():
    return random.randint(1, 65535)

# Generate sample data
sample_data = {
    'chain': [random.choice(chains) for _ in range(200)],
    'protocol': [random.choice(protocols) for _ in range(200)],
    'source': [generate_ip() for _ in range(200)],
    'source_port': [generate_port() for _ in range(200)],
    'destination': [generate_ip() for _ in range(200)],
    'destination_port': [generate_port() for _ in range(200)],
    'action': [random.choice(actions) for _ in range(200)]
}

# Create a DataFrame
df = pd.DataFrame(sample_data)

# Save the DataFrame to a CSV file
df.to_csv('sample_firewall_rules_200.csv', index=False)

print("Sample CSV file 'sample_firewall_rules_2000.csv' generated successfully.")
