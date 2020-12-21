import requests
import time
import json
import csv


def main():
	with open("addresses.csv",'r') as in_file:
		# data = csv.reader(in_file)
		data = in_file.read().splitlines()

	addrs = {}
	for i in data:
		row = i.split(",")
		addrs[row[0]] = row[1]

	batches = []
	batch = "https://blockchain.info/multiaddr?active="
	for addr in addrs.keys():
		if len(batch) + len(addr) > 4096:
			# create new batch of addresses (length of URL max 4096?)
			batches.append(batch)
			batch = "https://blockchain.info/multiaddr?active=" + addr + "|"
		else:
			batch += addr + "|"

	found = False
	for batch in batches:
		batch = batch[:-1]
		response = requests.get(batch)
		for i in response.json()["addresses"]:
			if i["n_tx"] != 0:
				print(i)
				print(addrs[i["address"]])
				found = True
		if found:
			break
		time.sleep(10)



if __name__ == "__main__":
	main()