from flask import Flask, request, abort, send_from_directory, make_response
import os, shutil, tempfile
import sys
sys.path.insert(0,'shortbol')
import shortbol.SBOL2ShortBOL as SB2Short
import requests

shortbol_library = os.path.join("shortbol", "templates")

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Download ShortBOL Plugin Flask Server is up and running")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    rdf_type = data['type']
    
    ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
    #uses rdf types
    #Check if the SBOL designs will always be collections
    accepted_types = {'Activity', 'Agent', 'Association', 'Attachment', 'Collection',
                      'CombinatorialDerivation', 'Component', 'ComponentDefinition',
                      'Cut', 'Experiment', 'ExperimentalData',
                      'FunctionalComponent','GenericLocation',
                      'Implementation', 'Interaction', 'Location',
                      'MapsTo', 'Measure', 'Model', 'Module', 'ModuleDefinition'
                      'Participation', 'Plan', 'Range', 'Sequence',
                      'SequenceAnnotation', 'SequenceConstraint',
                      'Usage', 'VariableComponent'}
    
    acceptable = rdf_type in accepted_types
    
    # #to ensure it shows up on all pages
    # acceptable = True
    ################## END SECTION ####################################
    
    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415

@app.route("/run", methods=["POST"])
def run():
    #temporary directory to write intermediate files to
    temp_dir = tempfile.TemporaryDirectory()
    data = request.get_json(force=True)

    complete_sbol = data['complete_sbol']

    try:

        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################

        run_data = requests.get(complete_sbol)
        sbol_input = os.path.join(temp_dir.name, "temp_shb.txt")
        with open(sbol_input, "w+") as sbol_file:
            sbol_file.write(run_data.text)
            result = SB2Short.produce_shortbol(sbol_file.name, shortbol_library)

        #print("***************************************************")
        #print(result)

        out_shb = "Out.txt"
        file_out_name = os.path.join(temp_dir.name, out_shb)
        with open(file_out_name, 'w+') as out_file:
            out_file.write(result)


        #print("--------------------------------------------------")
        #f = open(file_out_name, 'r')
        #file_contents = f.read()
        #print(file_contents)
        #f.close()

        ################## END SECTION ####################################

        return  send_from_directory(temp_dir.name, out_shb, attachment_filename="test.txt", as_attachment=True)

        
    except Exception as e:
        print(e)
        abort(400)
