import requests

def get_data(url,headers=None):
    response = requests.get(url,headers = headers)
    if response.status_code == 200:
        return response.text
    else:
        return {"error": "Failed to retrieve data"} 
    
if __name__ =="__main__":
    input_url = input("Enter URL: ")
    data = get_data(input_url)
    print("Data retrieved:", data)