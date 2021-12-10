#!/usr/bin/env python

import os
import re
import json
import functions


with open('websites.json') as fp:

    config = json.load(fp)

    streams = []
    labels = []
    labels_str = []
    base_labels = [None] * len(config['pcaps'])

    current_label = 1
    pat = re.compile(".*-curl\.pcap$")

    for domain in config['pcaps']:

        base_labels[current_label - 1] = domain


        current_label += 1

    functions.emptycsv()
    current_label = 1

    for domain in config['pcaps']:
        print(" - {}".format(domain))
        i = 0


        for file in os.listdir('./pcaps/{}'.format(domain)):
            if file.endswith(".pcap") and (pat.match(file) is None):

                file = os.path.join("./pcaps/{}".format(domain), file)

                # Reading the pcap file
                data = functions.readpcap(file)

                # Adding the data to streams list
                streams.append(data)

                # Adding data to the csv file
                functions.csvdata(domain, data)

                labels.append(current_label)
                labels_str.append(domain)

                i += 1

        print(f"    {i} pcap files")


        current_label += 1

    # Training the classifier
    functions.train(streams, labels)
