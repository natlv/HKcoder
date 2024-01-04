# This program is for easy checking of bus arrival time
from urllib.request import urlopen
import re

# If you are not sure of your bus stop name, you can search it up in the url below
url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

data = html

user_input = (input("Enter bus stop name: ")).upper()
name_en_value = re.search(f'"name_en":"{re.escape(user_input)}"', data, re.IGNORECASE)
if name_en_value:
    pattern = r'(.{{29}}){}'.format(re.escape(user_input))
    matches = re.findall(pattern, data)

    if matches:
        print("Route no.\tDestination\tEstimated arrival time")
        for match in matches:
            stop_value = match[-29:-13]
            problem_substring = 'name_en'
            if problem_substring not in stop_value:
                new_url = "https://data.etabus.gov.hk//v1/transport/kmb/stop-eta/{}".format(stop_value)
                new_page = urlopen(new_url)
                new_html_bytes = new_page.read()
                new_html = new_html_bytes.decode("utf-8")
                new_data = new_html

                routes = re.findall(r'"route":"(.*?)"', new_data)
                dest_en = re.findall(r'"dest_en":"(.*?)"', new_data)
                eta = re.findall(r'"eta":"(.*?)"', new_data)

                for i in range(len(eta)):
                    # In the following lines, 'new_pattern' and 'new_matches' are used to make the output look nicer
                    new_pattern = r'T(.*?)\+'
                    new_matches = re.findall(new_pattern, eta[i])
                    print(routes[i], "\t", dest_en[i], "\t", new_matches[0]) 
    else:
        print("Stop value not found")
else:
    print("Name not found")

