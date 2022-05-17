import argparse
import colorama
import csv
import json
import subprocess
from colorama import Fore, Back, Style
colorama.init()


parser = argparse.ArgumentParser(description='Scrape watch list')
parser.add_argument('-l', '--list',  help='watch list link', dest='path',
      metavar='filepath', required=True)
parser.add_argument('-c', '--crawler',  help='Crawler to use', dest='crawler',
      metavar='crawlerpath', required=True)


args = parser.parse_args()

print("------------------")
print("| Market watcher |")
print("------------------")

print("-> List:", args.path)

# Read watchlist
with open(args.path) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print("  Checking", row['Lien'])
        process = subprocess.run(['python', args.crawler, '-u', row['Lien']], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True)
        print(process.stdout)
        # print(process.stderr)
        res = json.loads(process.stdout)

        verdict = False
        if res['type'] == 'object':
            print(f"  {res['name']}")
            if(res['available']) == True:
                verdict = True   
        else:
            print(f"  {res['name']} - {row['Taille']} - {res['photo_alt']}")
            if(res['sizes'][row['Taille']] == True):
                verdict = True
                

        print(Back.GREEN if verdict else Back.RED)
        print(f"  {'Available' if verdict else 'Not Available'} - Price: {res['price']}")
        print(Style.RESET_ALL)
