from flask import Flask, request, abort, send_from_directory, make_response
import os, shutil, tempfile
import sys
sys.path.insert(0,'shortbol')
import shortbol.SBOL2ShortBOL as SB2Short
import requests

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Download Test Plugin Flask Server is up and running")

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
    #delete if not needed
    #cwd = os.getcwd()
    
    #temporary directory to write intermediate files to
    temp_dir = tempfile.TemporaryDirectory()
    data = request.get_json(force=True)

    #top_level_url = data['top_level']
    complete_sbol = data['complete_sbol']
    #instance_url = data['instanceUrl']
    #genbank_url = data['genbank']
    #size = data['size']
    #rdf_type = data['type']
    #shallow_sbol = data['shallow_sbol']
    
    url = complete_sbol.replace('/sbol','')
    #cwd = os.path.join(cwd, complete_sbol)

    try:

        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        #read in test.html
        #file_in_name = os.path.join(cwd, "plugintest.sbol")

        #with open('sbolfile', 'wb').write(file_in_name.content):
        with open(url.content, 'r') as sbolfile:
            shortbol_library = os.path.join("shortbol", "templates")
            result = SB2Short.produce_shortbol(sbolfile.name, shortbol_library)
        
        #write out file to temporary directory
        out_name = "Out.html"
        file_out_name = os.path.join(temp_dir.name, out_name)
        with open(file_out_name, 'w') as out_file:
            out_file.write(result)
        #this file could be a zip archive or any path and file name relative to temp_dir
        download_file_name = out_name

        ################## END SECTION ####################################

        return  send_from_directory(temp_dir.name,download_file_name, 
                                   as_attachment=True, attachment_filename=out_name)

        
    except Exception as e:
        print(e)
        abort(400)
