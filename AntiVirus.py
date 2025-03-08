import requests
def AntiVirus(file_path):
    try:
        URL = "https://www.virustotal.com/api/v3/files"
        analysis_url = "https://www.virustotal.com/api/v3/analyses/"
        FILES = { "file": (file_path, open(file_path, "rb"), "image/jpeg") }
        HEADERS = {
            "accept": "application/json",
            "x-apikey": "7e724551e51bb137bcfc5b89ff68225d4f01ac70374ee61341cc6b0fa040a773"
        }
    
        response1 = requests.post(URL, files=FILES, headers=HEADERS)
        response1 = response1.text
        response1 = response1.replace('"' , "")
        analysis_id = response1.split(" ")
        analysis_id = analysis_id[analysis_id.index("id:")+1]
        analysis_url += analysis_id.replace("," , "")
        response2 = requests.get(analysis_url, headers=HEADERS)
        response2 = response2.text
        print(response2)
        analysis = response2.split(" ")
        print(analysis)
        if(int(analysis[analysis.index('{"malicious":')+1].replace("," , ""))!= 0 ):
            return True , "this file is a threat"
        elif(int(analysis[analysis.index('"suspicious":')+1].replace("," , ""))!= 0):
            return True , "this file is suspicous"
        else:
            return False , "this file is not a threat"
    except Exception as e:
        return False ,e
if(__name__ == "__main__"):
    file_path = input("please enter a file you want to scan: ")
    isVirus , message = AntiVirus(file_path)
    print(message)