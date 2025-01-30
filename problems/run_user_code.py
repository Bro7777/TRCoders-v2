import requests

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"

def run_code_in_piston(language, code, input_data):
    """
    Piston API'yi kullanarak kodu çalıştırır.
    """
    payload = {
        "language": language,
        "version": "*",  # Varsayılan en güncel sürüm
        "files": [{"name": "main", "content": code}],
        "stdin": input_data
    }
    

    try:
        response = requests.post(PISTON_API_URL, json=payload)
        response.raise_for_status()

        result = response.json()

        if "run" in result:
            #print(result['run']['stdout'].strip(), result['run']['stderr'].strip(), response.status_code)
            return result['run']['stdout'].strip(), result['run']['stderr'].strip(), response.status_code
        else:
            return "", "Unknown error occurred", response.status_code
    except requests.RequestException as e:
        return "", str(e), 500
