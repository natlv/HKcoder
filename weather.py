from urllib.request import urlopen
import re

url = "https://www.hko.gov.hk/textonly/v2/forecast/englishwx2.htm"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

match_results = re.findall(r'(?<=At )(.*)(?=</pre>)', html, re.DOTALL)
formatted_results = '\n\n'.join(match_results)
formatted_results = formatted_results.replace("&#039;", "'")
print(formatted_results)



