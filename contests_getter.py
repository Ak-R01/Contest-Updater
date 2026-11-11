import requests
import subprocess

def notify_mako(title, message,timeout = "5000", urgency="normal"):
  CF_icon = "/home/akshit/.local/share/icons/CF.png"
  """
  Sends notification to Mako using notify-send
  urgency = low or normal or critical 
  """
  subprocess.run([
    "notify-send",
    f"--urgency={urgency}",
    f"--expire-time={timeout}",
    f"--icon={CF_icon}",
    title,
    message
  ])

def get_data():
  url = "https://codeforces.com/api/contest.list?"
  quer_params = {}
  response = requests.get(url,params=quer_params)
  if(response.status_code == 200):
    data = response.json()
    result = data["result"]
    # filtered_data = [x for x in result if x['phase'] == 'BEFORE' and any(d in x["name"] for d in ("Div. 2", "Div. 3", "Div. 4"))]
    filtered_data = [x for x in result if x['phase'] == 'BEFORE']
    return filtered_data
  else:
    notify_mako("Contest Alert","Failed to Fetch from CodeForces",urgency="critical")  

if __name__ == "__main__":
  get_data()