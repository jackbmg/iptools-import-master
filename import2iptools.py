#!/usr/bin/env python

import sys
import csv
from iptools.client import Client, ClientError

if len(sys.argv) != 2:
	sys.exit("usage: api-snippets.py <csv input file>")
f = open(sys.argv[1], 'rb')
# how many lines are in the file (i.e. number of addresses to request)
num_lines = sum(1 for line in f)
f.seek(0)
r = csv.reader(f)
# Create an API client, replace token with your API token value
c = Client(token='ff88c253405f4b8981b1e7c6940c7a97', host='iptools.swg.usma.ibm.com')
# Find the subnet you want to request addreses from, in this case I'll look for one named 'A3/188/Ratl' which has enough available addresses
for row in r:
	for subnet in c.ipv4subnets.all():
		if subnet['name'] == (row[4]) and subnet['available'] >= num_lines:
				print 'subnet %s\n' % (subnet['name'])
				IPaddress = c.ipv4addresses.get(row[0])
				user1 = c.users.get(row[3])
				address = c.ipv4addresses.request(IPaddress['id'], assignee=[user1['id']])	
				domain = c.domains.get(row[2])
				name = c.domainnames.create(address['id'], row[1], domain['id'])
				print 'Assigned %s.%s to %s\n' % (name['hostname'], name['domain']['name'], address['address'])
				break
		elif subnet['name'] == (row[4]) and subnet['available'] < num_lines:
				print 'not enough room'	
