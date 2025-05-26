import fabric.functions as fn
import requests
from azure.identity import ClientSecretCredential
import time

udf = fn.UserDataFunctions()

@udf.function()
def write_to_excel(idVal: str, firstName:str, lastName:str) -> str:
    TENANT_ID = ""
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    access_token = credential.get_token("https://graph.microsoft.com/.default").token

    site_id = ""
    table_name = ""
    excel_file_name = ""
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{excel_file_name}.xlsx:/workbook/tables/{table_name}/rows"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "values": [
            [idVal, firstName, lastName]
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    access_token = credential.get_token("https://analysis.windows.net/powerbi/api/.default").token

    group_id = ""
    dataset_id = ""
    refresh_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"

    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }   

    response = requests.post(refresh_url, headers=headers)
    time.sleep(10)

    if response.status_code == 201:
        return "Row added successfully!"
    else:
        return f"Error: {response.status_code} - {response.text}"