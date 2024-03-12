import requests, re

#region Data generation from WN to json files



def getWN_IDs(file, out_file):
    """
    Uses the data.pos files from the db files downloaded form WN
    to retreive all Synset IDs and places them in an a csv
    :param file: data.pos
    :param out_file: CSV filename
    :return: Creates a CSV containing list of WN ids from data.pos file
    """

    pattern = re.compile("\d\d\d\d\d\d\d\d \d\d \D")
    with open(file) as infile:
        with open(out_file, 'w') as outfile:
            for line in infile:
                for match in re.finditer(pattern, line):
                    outfile.write(f"{match.group()[:8]}-{match.group()[12]}\n")



def createArray(f):
    """
    converts the csv file from getWN_IDs() to an array to be used
    by pullJSON()
    :param f: file name
    :return: array of IDs
    """

    array = []
    with open(f) as file_name:
        for line in file_name:
            array.append(line[:-1])

    return array

def pullJSON(ids, outfile):
    """
    Creates a JSON file containing WN data for IDs given.
    :param ids: takes an array of IDs associated with Synsets
    :param outfile: file name for output file
    :return: pulls json file for each id on wordnet-rdf
    """

    print("Pulling JSONfiles from WordNet...")
    with open(outfile, "wb") as file:
        for id in ids:
            url=f"http://wordnet-rdf.princeton.edu/json/id/{id}"
            r = requests.get(url, allow_redirects=False)
            file.write(r.content+"\n".encode('ascii'))
            print(f"{id} pulled.")

    print("Completed pull.")



def initDataPull(infile, outfile, outjson):
    """
    Takes the necessary files and outputs a scraped JSON file
    :param infile: WN Database file "data.pos"
    :param outfile: File name for WN "data.pos" ID list
    :param outjson: File name for JSON file containing scarped data
    :return: generates usable files for Neo4j import
    """

    getWN_IDs(infile, outfile)

    a = createArray(outfile)

    pullJSON(a, outjson)



#endregion

def main():
    # Source files
    data_adj = "./wn_source/data.adj"
    data_adv = "./wn_source/data.adv"
    data_verb = "./wn_source/data.verb"
    data_noun = "./wn_source/data.noun"

    # ID outfile names
    adj_synsetIDs = "./output/adj_synsetIDs.csv"
    adv_synsetIDs = "./output/adv_synsetIDs.csv"
    verb_synsetIDs = "./output/verb_synsetIDs.csv"
    noun_synsetIDs = "./output/noun_synsetIDs.csv"

    # Compiled JSON file names
    adj_json = "./output/data.adj.json"
    adv_json = "./output/data.adv.json"
    verb_json = "./output/data.verb.json"
    noun_json = "./output/data.noun.json"

    initDataPull(data_adj, adj_synsetIDs, adj_json)
    initDataPull(data_adv, adv_synsetIDs, adv_json)
    initDataPull(data_verb, verb_synsetIDs, verb_json)
    initDataPull(data_noun, noun_synsetIDs, noun_json)

if __name__ == "__main__":
    main()