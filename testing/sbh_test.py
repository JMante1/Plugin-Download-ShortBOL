import requests
import urllib
import requests, zipfile, io

eval_url = "http://127.0.0.1:5000/evaluate"
run_url = "http://127.0.0.1:5000/run"

run_data =  "{‘complete_sbol’: ‘https://dev.synbiohub.org/public/igem/BBa_E0240/1/sbol', ‘shallow_sbol’: ‘https://dev.synbiohub.org/public/igem/BBa_E0240/1/sbolnr', ‘genbank’: ‘https://dev.synbiohub.org/public/igem/BBa_E0240/1/gb', ‘top_level’: ‘https://synbiohub.org/public/igem/BBa_E0240/1', ‘size’: 39, ‘type’: ‘Component’, ‘instanceUrl’: ‘https://dev.synbiohub.org/'}"

def test():
    eval_response = requests.post(eval_url, '{‘type’: ‘Component’}')
    run_response = requests.post(run_url, data=run_data)

    print(eval_response.text)
    z = zipfile.ZipFile(io.BytesIO(run_response.content))
    z.extractall("out")


if __name__ == "__main__": test()