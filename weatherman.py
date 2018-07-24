import os
import sys

class WeathermanEntries:
    def __init__(self):
        self.entries = {}


    def set_entries(self, key, entries):
        self.entries[key] = entries


    def highest_temp(self, by = None):
        _highest_temp = 0.0
        _highest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                max_temp = d.get('Max TemperatureC')
                if max_temp is not None and max_temp.isalnum() \
                and float(max_temp) > _highest_temp:
                    _highest_temp = float(max_temp)
                    _highest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_highest_temp, _highest_temp_pkt)
        else:
            return (None, None)


    def lowest_temp(self, by = None):
        _lowest_temp = 100
        _lowest_temp_pkt = ''
        found = False

        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                min_temp = d.get('Min TemperatureC')
                if min_temp is not None and min_temp.isalnum() \
                and float(min_temp) < _lowest_temp:
                    _lowest_temp = float(min_temp)
                    _lowest_temp_pkt = d.get('PKT') or d.get('PKST')
                    found = True
        if found:
            return (_lowest_temp, _lowest_temp_pkt)
        else:
            return (None, None)


    def most_humid(self, by = None):
        _most_humid = 0
        _most_humid_pkt = ''
        found = False
        for e in wmentries.entries.keys():
            if by is not None and by not in e:
                continue
            for d in wmentries.entries[e]:
                most_humid = d.get('Max Humidity')
                if most_humid is not None and most_humid.isalnum() \
                and float(most_humid) > _most_humid:
                    _most_humid = float(most_humid)
                    _most_humid_pkt = d.get('PKT') or d.get('PKST')
                    found = True

        if found:
            return (_most_humid, _most_humid_pkt)
        else:
            return (None, None)

wmentries = WeathermanEntries()
    

class WeathermanEntry:

    def __init__(self, entry):
        self.entry = entry

    def get(self, key):
        return self.entry.get(key, None)

    def __str__(self):
        return str(self.entry)


def read_to_weatherman_entry(meta, line):
    return WeathermanEntry(dict(zip(meta, line)))


def read_file(file):
    f = open(file, "r")
    blank = f.readline().strip("\n")
    meta = f.readline().strip("\n").replace(", ", ",").split(",")
    entries = []
    for line in f.readlines():
        l = line.strip("\n").split(",");
        entries.append(read_to_weatherman_entry(meta, l))
    wmentries.set_entries(file, entries)


def main():
    path = sys.argv[1]
    mode = sys.argv[2]

    weatherdata = os.listdir(path)
    
    for file in weatherdata:
        read_file(os.path.join(path, file))

    if mode == '-e':
        year = sys.argv[3]
        highest_temp = wmentries.highest_temp(year)
        lowest_temp = wmentries.lowest_temp(year)
        most_humid = wmentries.most_humid(year)
        print("Highest:", highest_temp[0], "on", highest_temp[1])
        print("Lowest:", lowest_temp[0], "on", lowest_temp[1])
        print("Humidity:", most_humid[0], "on", most_humid[1])


main()
