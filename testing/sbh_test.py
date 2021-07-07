import os

import requests
import urllib
import requests, zipfile, io

eval_url = "http://127.0.0.1:8080/evaluate"
run_url = "http://127.0.0.1:8080/run"

data = """{"complete_sbol": "http://localhost:5000/public/plugintest.sbol", 
            "shallow_sbol": "", 
            "genbank": "", 
            "top_level": "", 
            "size": 39, 
            "type": "Component", 
            "instanceUrl": ""}"""

def test():
    save_path = 'out'
    file_name = "test.txt"

    completeName = os.path.join(save_path, file_name)

    eval_response = requests.post(eval_url, data=data)
    run_response = requests.post(run_url, data=data)
    print(eval_response.text)
    print(run_response.text)
    print(run_response.headers)
    print(run_response.status_code)

    file1 = open(completeName, "w")
    file1.write(run_response.text)
    file1.close()


if __name__ == "__main__": test()