from flask import Flask, request, jsonify, render_template
from urllib.request import urlopen
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/bus-arrival", methods=['GET', 'POST'])
def get_bus_arrival():

    if request.method == 'POST':

        url = "https://data.etabus.gov.hk/v1/transport/kmb/stop"

        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        data = html

        bus_stop_name = request.form['bus_stop_name']
        # bus_stop_name = "wu kai sha station"
        if bus_stop_name:
            user_input = bus_stop_name.upper()
            name_en_value = re.search(f'"name_en":"{re.escape(user_input)}"', data, re.IGNORECASE)
            if name_en_value:
                pattern = r'(.{{29}}){}'.format(re.escape(user_input))
                matches = re.findall(pattern, data)

                if matches:
                    bus_arrivals = []
                    for match in matches:
                        stop_value = match[-29:-13]
                        if 'name_en' not in stop_value:
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
                                
                                bus_arrivals.append({
                                    "route": routes[i],
                                    "destination": dest_en[i], 
                                    "estimated_arrival_time": new_matches[0]
                                })
                    # return jsonify(bus_arrivals)
                    table = "<table><tr><th>Route</th><th>Destination</th><th>Estimated Arrival Time</th></tr>"
                    for arrival in bus_arrivals:
                        table += f"<tr><td>{arrival['route']}</td><td>{arrival['destination']}</td><td>{arrival['estimated_arrival_time']}</td></tr>"
                    table += "</table>"

                    table += "<br><a href='/'>Search for another bus stop</a>"

                    return table
                    
                else:
                    return jsonify({"error": "Stop value not found"})
            else:
                return jsonify({"error": "Name not found"})
        else:
            return jsonify({"error": "bus_stop_name parameter is required"})
    else:
        return jsonify({"error": "Invalid request method"})

if __name__ == "__main__":
    app.run(debug=True)