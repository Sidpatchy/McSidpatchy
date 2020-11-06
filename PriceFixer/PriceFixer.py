# This is a part of the custom player-protection used on McSidpatchy. More stuff like this will be open-sourced in the future. I tried to write comments but the commenting isn't really the greatest.
# It works by analyzing the amount a player has made in the last day from the logs and then parses that into a few dictionaries and does a lot of werid shit with indexing. Then, it finally overwrites the current worth.yml. The method used isn't very safe, but, nonetheless is used anyway.
# Ensure you have economy log enabled and PyYaml installed.
# To use this, simply place the contents of PriceFixer in the server's root directory and create a crontab to run it once per day.

import priceFixer.sLOUT as lout
import yaml

# Limit for how much a player is allowed to make in a day off of one item
allowableLimit = 500000

# Read latest.log and store it in latestLog
# The whole if-else statement just fixes a weird quirk with Visual Studio Code
if not lout.readFile('/logs/latest.log'):
    # It'll still run, just 5 seconds slower...
    f = open('PriceFixer/logs/latest.log')
    latestLog = f.readlines()
    f.close()

else:
    f = open('/logs/latest.log')
    latestLog = f.readlines()
    f.close()

players = []    # List of players
items = {}      # Dictionary of items
sales = {}      # Dictionary for storing the amount made per item.

# Extract economy logs
for line in latestLog:
    # If you use this it is in your best interest to use more criteria than this. I have included two that mean it will be safe-ish
    # if a player discovers what you are using to verify that the line of the file is actually from essentials they could completely break this whole thing.
    # Prices would be fine, however, a pathway to avoiding this whole script is very possible if a player discovers the criteria.
    if 'sold' in line and '[Essentials]' in line:
        line = line[46:]
        item = (line.partition('sold')[2]).split()[0]   # Store the item
        player = line.partition('sold')[0]              # Store the player
        profit = (line.partition('for')[2]).split()[0]  # Store ammount earned
        profit = profit.replace('$', '')                # Remove dollar sign
        profit = profit.replace(',', '')                # Remove comma
        
        # Store the values gathered above in a list
        # Store the player in a list and register player in items dictionary
        if not player in players:
            players.append(player)
            items[player] = []
            sales[player] = []
            print('Added "{}" to players'.format(player))

        # Store the item in a dictionary
        if not item in items[player]:
            items[player].append(item)
            # Add the item to the list the first time the item is found
            sales[player].append(float(profit))
        else:
            index = items[player].index(item)
            (sales[player])[index] = (sales[player])[index] + float(profit)

aboveLimit = [] # List of items that are above the value stored in allowableLimit

# Check if a player has made more than the allowed limit off of one type of item
for player in players:
    for item in items[player]:
        index = items[player].index(item)
        if (sales[player])[index] > allowableLimit:
            if not item in aboveLimit:
                aboveLimit.append(item)

print(aboveLimit)

for item in aboveLimit:
    # Remove underscores from item
    item = item.replace('_', '')

    # Variable used to store the YAML file while unsafely deleting its contents. Keep a backup of your yaml file!
    WholeAssYAMLFile = []

    # The whole if-else statement just fixes a weird quirk with Visual Studio Code
    if not lout.readFile('/logs/latest.log'):
        
        # Open the file and then store the file once the value has been trimmed.
        with open('PriceFixer/plugins/essentials/worth.yml', 'r') as f:
            file = yaml.safe_load(f)
            value = file['worth'][item]
            print(value)
            newValue = value / 4
            file['worth'][item] = newValue
            WholeAssYAMLFile = file

        # Delete the whole file and then write the new values to it.
        with open('PriceFixer/plugins/essentials/worth.yml', 'w+') as f:
            yaml.dump(WholeAssYAMLFile, f)
        print(item, 'had its price updated to', newValue, 'from', value)
    else:

        # Open the file and then store the file once the value has been trimmed.
        with open('plugins/essentials/worth.yml', 'r') as f:
            file = yaml.safe_load(f)
            value = file['worth'][item]
            print(value)
            newValue = value / 4
            file['worth'][item] = newValue
            WholeAssYAMLFile = file

        # Delete the whole file and then write the new values to it.
        with open('plugins/essentials/worth.yml', 'w+') as f:
            yaml.dump(WholeAssYAMLFile, f)
        print(item, 'had its price updated to', newValue, 'from', value)
