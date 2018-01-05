# This is used to see so I don't make stupid changes

import deftree
import os
import timeit
import csv
import datetime
import cProfile


root_path = os.path.dirname(__file__)
profiling_document = os.path.join(root_path, 'profile.defold')
csv_profile_data = os.path.join(root_path, 'profiling.csv')


def timing_parse():
    print("Warning: This can take anything between 0 seconds to minutes")
    times = 300
    value = timeit.timeit(
        stmt="deftree.parse('{}')".format(profiling_document),
        setup="import deftree; import os", number=times)

    print("Total time spent: {}, Number of times ran: {}".format(value, times))
    return value/times


def store_timing_data():
    if not os.path.exists(csv_profile_data):
        with open(csv_profile_data, "w", newline='') as csvfile:
            _writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            _writer.writerow(['sep=,'])
            _writer.writerow(["Date", "Version", "Average Time", "profile.defold modified"])

    with open(csv_profile_data, "a", newline='') as csvfile:
        now = datetime.datetime.now()
        profile_doc = datetime.datetime.fromtimestamp(os.path.getmtime(profiling_document))

        _writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        _writer.writerow(
            [now.strftime("%Y-%m-%d"), deftree.__version__, timing_parse(), profile_doc.strftime("%Y-%m-%d %H:%M")])


def profile_parse():
    cProfile.run('for x in range(200): deftree.parse("{}")'.format(profiling_document))

store_timing_data()
