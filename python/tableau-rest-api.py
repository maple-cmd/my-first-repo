import requests
import xml.etree.ElementTree as ET

# --- 1. 認証情報とエンドポイント ---
TABLEAU_SERVER = 'https://your-tableau-server.com'
USERNAME = 'your-username'
PASSWORD = 'your-password'
SITE = ''  # Default site は空文字（空白）
FLOW_ID = 'your-flow-id'

# --- 2. ログインしてトークンを取得 ---
def login():
    url = f"{TABLEAU_SERVER}/api/3.21/auth/signin"
    headers = {"Content-Type": "application/xml"}
    xml_payload = f'''
    <tsRequest>
        <credentials name="{USERNAME}" password="{PASSWORD}">
            <site contentUrl="{SITE}" />
        </credentials>
    </tsRequest>
    '''
    res = requests.post(url, data=xml_payload, headers=headers)
    res.raise_for_status()
    root = ET.fromstring(res.text)
    token = root.find('.//t:token', namespaces={'t': 'http://tableau.com/api'}).text
    site_id = root.find('.//t:site', namespaces={'t': 'http://tableau.com/api'}).attrib['id']
    user_id = root.find('.//t:user', namespaces={'t': 'http://tableau.com/api'}).attrib['id']
    return token, site_id, user_id

# --- 3. Flow を実行 ---
def run_flow(token, site_id):
    url = f"{TABLEAU_SERVER}/api/3.21/sites/{site_id}/flows/{FLOW_ID}/runNow"
    headers = {
        "Content-Type": "application/xml",
        "X-Tableau-Auth": token
    }

    xml_payload = f'''
    <tsRequest>
        <flowRunSpec flowId="{FLOW_ID}" runMode="Standard" />
    </tsRequest>
    '''

    res = requests.post(url, headers=headers, data=xml_payload)
    res.raise_for_status()
    return res.text

# --- 4. ログアウト ---
def logout(token):
    url = f"{TABLEAU_SERVER}/api/3.21/auth/signout"
    headers = {"X-Tableau-Auth": token}
    requests.post(url, headers=headers)

# --- 実行部 ---
if __name__ == '__main__':
    try:
        token, site_id, user_id = login()
        result = run_flow(token, site_id)
        print("Flow 実行結果:\n", result)
    except Exception as e:
        print("エラー:\n", e)
    finally:
        logout(token)
