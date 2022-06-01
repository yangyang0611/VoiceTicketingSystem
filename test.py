import requests
import time

TOKEN = '5a3852950933f6034de7791c35815e80b336fac45271'  # 请替换成自己的TOKEN
REFERER = 'https://www.google.com/recaptcha/api2/demo'
BASE_URL = 'https://www.yescaptcha.com'
SITE_KEY = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'  # 请替换成自己的SITE_KEY


def create_task():
    url = f"{BASE_URL}/v3/recaptcha/create?token={TOKEN}&siteKey={SITE_KEY}&siteReferer={REFERER}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print('response data:', data)
            return data.get('data', {}).get('taskId')
    except requests.RequestException as e:
        print('create task failed', e)


def polling_task(task_id):
    url = f"{BASE_URL}/v3/recaptcha/status?token={TOKEN}&taskId={task_id}"
    count = 0
    while count < 120:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print('polling result', data)
                status = data.get('data', {}).get('status')
                print('status of task', status)
                if status == 'Success':
                    return data.get('data', {}).get('response')
        except requests.RequestException as e:
            print('polling task failed', e)
        finally:
            count += 1
            time.sleep(1)


if __name__ == '__main__':
    task_id = create_task()
    print('create task successfully', task_id)
    response = polling_task(task_id)
    print('get response:', response[0:40]+'...')
