import dpkt
import socket
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from joblib import dump


def emptycsv(): #empty csv file
	with open("./data.csv", 'w') as f:
		f.write("")


def csvdata(website, data): #write data inside the file
    with open("./data.csv", 'a') as f:
        f.write("{},{}\n".format(website, ','.join(str(num) for num in data)))


def inet_to_str(inet): #convert to string
    return socket.inet_ntop(socket.AF_INET, inet)


def shuffle(x, y): #shuffling the datasets

    for n in range(len(x) - 1):
        rnd = random.randint(0, (len(x) - 1))
        x1 = x[rnd]
        x2 = x[rnd - 1]

        y1 = y[rnd]
        y2 = y[rnd - 1]

        x[rnd - 1] = x1
        x[rnd] = x2

        y[rnd - 1] = y1
        y[rnd] = y2

    return x, y


def readpcap(file): #reading the pcap and returning the sizes

    fp = open(file, 'rb')

    pcap = dpkt.pcap.Reader(fp)

   
    sizes = [0] * 40  #we used the first 40 packets
    i = 0

    outgoing_addr = None
    outgoing_packets = 0
    incoming_packets = 0
    packets_total = 0
    incoming_size = 0

    for i, j in pcap:
        packet_size = len(j)
        outgoing = True
        eth = dpkt.ethernet.Ethernet(j)

        # Storing the IP packet
        ip = eth.data

        src = inet_to_str(ip.src)

        if packets_total == 0:
            outgoing_addr = src
            outgoing_packets += 1

        elif src == outgoing_addr:
            outgoing_packets += 1

        else:
            incoming_packets += 1
            incoming_size += packet_size
            outgoing = False

        if i < 40:
            # Adding the size to the array.
            sizes[i] = packet_size if outgoing else -packet_size
            i += 1

        packets_total += 1

  
    ratio = float(incoming_packets) / (outgoing_packets if outgoing_packets != 0 else 1)



    sizes.reverse()
    sizes.append(ratio)
    sizes.append(incoming_packets)
    sizes.append(outgoing_packets)
    sizes.append(packets_total)
    sizes.append(incoming_size)
    sizes.reverse() #order by sizes
    return sizes


def train(streams, labels): #training the classifier

 
    streams, labels = shuffle(streams, labels)

    stream_amount = len(streams)
    training_size = int(stream_amount * 0.9)

  
    training_x = streams[:training_size]
    training_y = labels[:training_size]

    testing_x = streams[training_size:]
    testing_y = labels[training_size:]

    print(("Training size: {}".format(training_size)))
    print(("Testing size:  {}".format(stream_amount - training_size)))

    clf = KNeighborsClassifier(n_neighbors=3)
    clf = clf.fit(training_x, training_y)

    # Getting the prediction
    predictions = clf.predict(testing_x)

    print(("Accuracy: %s%%" % (accuracy_score(testing_y, predictions) * 100,)))
