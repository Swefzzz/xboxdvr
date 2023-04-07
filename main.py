from flask import Flask, render_template, abort
import requests
import json
import time

app = Flask(__name__)
app.template_folder = ''  # set the path to your template directory

# cache the headers and the time they were last updated
headers_cache = None
headers_cache_time = 0


def get_headers():
  #url = 'https://xboxdvrauth.swefz.repl.co/'
  #response = requests.get(url)
  #print(response.text)
  #items = response.json()
  #xsts_token = items.get('xsts_token')
  #user_hash = items.get('user_hash')
  headers = {
    'Authorization':
    f'XBL3.0 x=2535448728635324;eyJlbmMiOiJBMTI4Q0JDK0hTMjU2IiwiYWxnIjoiUlNBLU9BRVAiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJ4NXQiOiIxZlVBejExYmtpWklFaE5KSVZnSDFTdTVzX2cifQ.ZtxpfyBtCkuGEN79aDl92rTILUBNIZZaMC484hP49Gx2Dc_Q4dHJH5kDwmiQDS434Nd7WC6yNxZSKcyvbtJAY1abhDjW6DXR5IUkNN4yMjdRg9T2UWPBJUcWPdp6by6WAA3zO7ApJJlDyheB61rCO1zVnlcgU0a86QL_GWSGv74.ZNLkWbZZqYHfHJBPzql3MQ.CsGzsRJgLrDglkNLWE2wh9fNEXVMEVNfzxqoefrdVu5vUNLWKnLQjcr0tRz2-kC4vZreTPGsW9ri9OKSMoCIdlA8hEo-mKzU4E7xlekV4LE0l5pGwiFW-3hDofMm0Eo5UB6ScEWYuW9F5uCigepzOWuE2fNxH5I4i3BFQ_6vQwhiX2qENZZcdsbpVxbq7x22d60Y6OAPJbgbW9m7bCgkBggLcLv7sGVY8BHEIVExNdfMOhBK8Pp3nR3NNnuKudUUJNeN3e-20x9DcUYUQUMiy3Lbs9htOZ2-7VfZP5n2etAvoKbwHNEAsehUucwAvBufaJRjpcdz1PzOiJYPf__hEG72wNooiirdDKIK8dRmMsreqgUWOlWfjY37cwA_hhqUiYmLN4O5XRuLHqXVaIgxFKcoKHCo__8JsY4S3YchWafJs96JDjX8tcoGff9jyinpqrzi_k_1KAjTjAns_gikmHaBgKi5fbG0dNI5q6TZUFtjSr85W1OreSPMtXxHfUtWEnEnpnaSlx8oJOYo0v7wizPm-zr7xn7CBIgyY8XnjMglxEQSlmMUf5mG4b2Q-n9gIKdi2yYy_D0b6b58fw61NbdXdrRkBrkxoxM8FjWZBmbLTdF8OdOxeV3rZeMkK0ROBuT-KFNODY85zVNyqREjIaeGOTl40uTWjstEq9kOzVa2EKU6jX6-wJpDowZCQDgc44yQ9QVJ1xSdl3yzDXgTxL975_fH5ApkA7cwPvHbDrH9XD7cuMTULVDVapFcW32un8Ov52Ch-XAydfC3O_1OaTaCdAE7M8bPX0OZci5gyZqMUDEAOaEQwjOth6aqxHFE5YeXLgxNLaRihho9mQF_wYHDG342cUIKFOLalj1TM6BvAoM1zrySRHfhJ7yVE65bBTE6Jmuwa0b-Rb7hqXAEZKAR_Zu9jYR4rUEpPXo9jNlw4_1_PdOL7XaGxmu9x7HDtTRJXNEik2ElJyWU7jZtSvScK9CjG6ajXUalbzoIbdDCxeB5uQ5nMXxW7U4cl5-wCYH5o1CJ_c-gayORWfxUoY4Sky7wZeRjWrfTo4xN9cGgi8GfEq3462_NBIoimBVKdoomy8u7fBQjxwe5JrrajPRppyzzUHutn9sOU_mS6LcrzHOe91q5I-HCybYiH7msgq12EgjZuCXauPnl6nDdU5uOWBwa73g0VfSHwx6NWNIgGV_mdqfcFKHQpuqVz55e2gjHRccJEZuavvy79k3ckRcB65MAhAf1lkMnZ56BN6rLoHStgF9b0plWkYHWzhDjrS8kiTTuOGBP6evm9KNhojS1j0zi7Zg5BCFN1nol4Kj7EYjPfDry8m6TIYsXGYMYWrfLOFLWihDeh_zEZ_BfTnCFvWuNkv-3YtM7MqnS3LoEbF3A999gnryjYGLdXQ9djuQS7qIOkRKNLJ8hoS_72Szn28K7A9C3qJcUo41iKZvHxuUDZnpE21S-BmVB1eVF.Ra5MoUOPVnr61-IhjIDzhm3KrOZD33Oz4OW2nvM1TEI',
    #'Authorization': f'XBL3.0 x={user_hash};{xsts_token}',
    'X-XBL-Contract-Version': '2',
    'Content-Type': 'application/json'
  }
  return headers


def creds():
  if 'cached_headers' not in globals(
  ) or time.time() - globals()['last_headers_fetch_time'] > 3600:
    globals()['cached_headers'] = get_headers()
    globals()['last_headers_fetch_time'] = time.time()
  return globals()['cached_headers']


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/gamertag/<gamertag>/')
@app.route('/gamertag/<gamertag>')
def gamertag(gamertag):
  headers = creds()
  response = requests.get(
    f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
    headers=headers)
  responsejson = json.loads(response.text)
  if response.ok:
    gamertag = responsejson['profileUsers'][0]['settings'][0]['value']
  else:
    gamertag = "LocationFinder"
  return render_template('gamertag.html', gamertag=gamertag)


@app.route('/gamertag/<gamertag>/clips/')
@app.route('/gamertag/<gamertag>/clips')
def clips(gamertag):
  headers = creds()
  response = requests.get(
    f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
    headers=headers)
  responsejson = json.loads(response.text)
  while response.status_code == 429:
    # Sleep for 10 seconds before retrying
    print("Rate Limited")
    time.sleep(10)
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
      headers=headers)
  while response.status_code == 403:
    headers = creds()
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
      headers=headers)
    responsejson = json.loads(response.text)
  if response.status_code == 200:

    gamertag = responsejson['profileUsers'][0]['settings'][0]['value']
    avatar_url = responsejson['profileUsers'][0]['settings'][1]['value']
    id = responsejson['profileUsers'][0]['id']

    url = 'https://mediahub.xboxlive.com/gameclips/search'
    data = f'{{"query": "OwnerXuid eq {id}"}}'
    response = requests.post(url, headers=headers, data=data)

    gameclips_json = json.loads(response.text)
    if 'values' in gameclips_json:
      gameclips = []
      for clip in gameclips_json['values']:
        gameclip = {}
        gameclip['thumbnail_url'] = clip['contentLocators'][2]['uri']
        gameclip['clip_url'] = clip['contentLocators'][0]['uri']
        gameclip['unique_id'] = clip['contentId']
        gameclip['game_title'] = clip['titleName']
        gameclip['date_created'] = clip['uploadDate']
        gameclips.append(gameclip)
    else:
      gameclips = []
    return render_template('clips.html',
                           gamertag=gamertag,
                           gameclips=gameclips,
                           avatar=avatar_url)
  elif response.status_code == 404:  #gamertag not found
    return render_template('notfound.html')
  else:
    data = {
      "content": f"An error occurred: {response.status_code, response.text}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
      "https://discord.com/api/webhooks/1084251953976066248/gfIo_N1K16lWZVqIkYkNQKWmnCwIpz870P51p35AUWhVMfvqh3UHV0d8Vqh9GMpZFT4x",
      data=json.dumps(data),
      headers=headers)


@app.route('/gamertag/<gamertag>/screenshots/')
@app.route('/gamertag/<gamertag>/screenshots')
def screenshots(gamertag):
  headers = creds()
  response = requests.get(
    f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
    headers=headers)
  responsejson = json.loads(response.text)
  while response.status_code == 429:
    # Sleep for 10 seconds before retrying
    time.sleep(10)
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
      headers=headers)
    responsejson = json.loads(response.text)
  while response.status_code == 403:
    headers = creds()
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
      headers=headers)
    responsejson = json.loads(response.text)
  if response.status_code == 200:
    gamertag = responsejson['profileUsers'][0]['settings'][0]['value']
    id = responsejson['profileUsers'][0]['id']
    avatar_url = responsejson['profileUsers'][0]['settings'][1]['value']

    url = 'https://mediahub.xboxlive.com/screenshots/search'
    data = f'{{"query": "OwnerXuid eq {id}"}}'
    response = requests.post(url, headers=headers, data=data)
    gameclips_json = json.loads(response.text)
    gameclips = []
    if 'values' in gameclips_json:
      for clip in gameclips_json['values']:
        gameclip = {}
        gameclip['thumbnail_url'] = clip['contentLocators'][2]['uri']
        gameclip['game_title'] = clip['titleName']
        gameclip['date_created'] = clip['dateUploaded']
        gameclips.append(gameclip)
    else:
      gameclips = []
    return render_template('screenshots.html',
                           gamertag=gamertag,
                           gameclips=gameclips,
                           avatar=avatar_url)
  elif response.status_code == 404:  #gamertag not found
    return render_template('notfound.html')
  else:
    data = {
      "content": f"An error occurred: {response.status_code, response.text}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
      "https://discord.com/api/webhooks/1084251953976066248/gfIo_N1K16lWZVqIkYkNQKWmnCwIpz870P51p35AUWhVMfvqh3UHV0d8Vqh9GMpZFT4x",
      data=json.dumps(data),
      headers=headers)


@app.route('/gamertag/<gamertag>/clips/<unique_id>/')
@app.route('/gamertag/<gamertag>/clips/<unique_id>')
def clip(gamertag, unique_id):
  headers = creds()
  response = requests.get(
    f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
    headers=headers)
  responsejson = json.loads(response.text)
  while response.status_code == 429:
    # Sleep for 10 seconds before retrying
    time.sleep(10)
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=GameGameDisplayPicRaw,Gamertag',
      headers=headers)
    responsejson = json.loads(response.text)
  while response.status_code == 403:
    headers = creds()
    response = requests.get(
      f'https://profile.xboxlive.com/users/gt({gamertag})/profile/settings?settings=Gamertag,GameDisplayPicRaw',
      headers=headers)
    responsejson = json.loads(response.text)
  if response.status_code == 200:
    gamertag = responsejson['profileUsers'][0]['settings'][0]['value']
    id = responsejson['profileUsers'][0]['id']

    url = 'https://mediahub.xboxlive.com/gameclips/search'
    data = f'{{"query": "OwnerXuid eq {id}"}}'
    response = requests.post(url, headers=headers, data=data)

    gameclips_json = json.loads(response.text)
    gameclips = []  # replace with the unique id you are searching for
    for clip in gameclips_json['values']:
      if clip['contentId'] == unique_id:
        gameclip = {}
        gameclip['thumbnail_url'] = clip['contentLocators'][2]['uri']
        gameclip['clip_url'] = clip['contentLocators'][0]['uri']
        gameclip['game_title'] = clip['titleName']
        gameclip['date_created'] = clip['uploadDate']
        gameclips.append(gameclip)

    return render_template('clip.html', gamertag=gamertag, gameclips=gameclips)

  elif response.status_code == 404:  #gamertag not found
    return render_template('notfound.html')
  else:
    abort(404)
    data = {
      "content": f"An error occurred: {response.status_code, response.text}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
      "https://discord.com/api/webhooks/1084251953976066248/gfIo_N1K16lWZVqIkYkNQKWmnCwIpz870P51p35AUWhVMfvqh3UHV0d8Vqh9GMpZFT4x",
      data=json.dumps(data),
      headers=headers)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
