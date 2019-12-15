import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '{subscription key}',
}

params = urllib.parse.urlencode({
     'gtin': '{string}',
    'tpnb': '{string}',
    'tpnc': '{string}',
    'catid': '{string}',
})


try:
    conn = http.client.HTTPSConnection('dev.tescolabs.com')
    conn.request("GET", "/grocery/products/?query={query}&offset={offset}&limit={limit}&%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))