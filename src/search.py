import requests
import json
import re

def get_latest_gpt4_paper():
    url = "https://api.arxiv.org:443/v1/search"
    params = {
        "query": "gpt-4",
        "max_results": 1,
        "sort_by": "submittedDate",
        "order": 1,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = json.loads(response.text)
        paper_id = data["meta"]["results"][0]["id"]
        return paper_id
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection error occurred: {conn_error}")
    except Exception as general_error:
        print(f"General error occurred: {general_error}")
    return None

def get_paper_details(paper_id):
    url = f"https://api.arxiv.org:443/v1/paper/{paper_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.text)
        return data
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection error occurred: {conn_error}")
    except Exception as general_error:
        print(f"General error occurred: {general_error}")
    return None

def extract_software_applications(paper_data):
    abstract = paper_data["abstract"]
    applications = re.findall(r"software\s(?:\w+\s)?(?:application|app|program|tool)", abstract, re.IGNORECASE)
    return applications

def main():
    paper_id = get_latest_gpt4_paper()
    if paper_id:
        paper_data = get_paper_details(paper_id)
        if paper_data:
            applications = extract_software_applications(paper_data)
            print("Potential software applications in the latest GPT-4 paper:")
            for application in applications:
                print(application)
        else:
            print("Failed to fetch paper details.")
    else:
        print("Failed to find the latest GPT-4 paper.")

if __name__ == "__main__":
    main()