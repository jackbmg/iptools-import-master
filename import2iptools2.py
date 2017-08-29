#!/usr/bin/env python

import sys
import csv
from iptools.client import Client, ClientError

if len(sys.argv) != 3:
	sys.exit("usage: api-snippets.py <csv input file> <subnet title>")
# Create an API client, replace token with your API token value
c = Client(token='token here', host='lit-iptoolstest2.swg.usma.ibm.com')

with open(sys.argv[1],'rb') as hf:
	hf.seek(0)
	r=csv.reader(hf)
	for subnet in c.ipv4subnets.all():
		if subnet['name'] == (sys.argv[2]):
			print 'subnet %s has %s addresses left' % (subnet['name'], subnet['available'])
	for row in r:
			user1 = c.users.get(row[3])
			IPAddress = c.ipv4addresses.get(row[0])
			if IPAddress['status'] == 'A':
				address = c.ipv4addresses.request(IPAddress['id'], assignee=[user1['id']])
			elif IPAddress['status'] == 'S':
				print '%s address is already assigned' % (row[0])
				continue
			elif IPAddress['status'] == 'R':
				print '%s address is reserved' % (row[0])
				continue
			domain = c.domains.get(row[2])
			name = c.domainnames.create(address['id'], row[1], domain['id'])
			print 'Assigned %s.%s to %s\n' % (name['hostname'], name['domain']['name'], address['address'])

	

