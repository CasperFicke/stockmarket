from django.shortcuts import render
import os

# home view.
def home(request):
  import json
  import requests
  iexcloud_apikey = os.getenv('IEXCLOUD_APIKEY')

  if request.method == "POST":
    ticker = request.POST['ticker_symbol']
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/quote?token=" + iexcloud_apikey)
    try:
      api_result = json.loads(api_request.content)
    except Exception as e:
      api_result = "Error..."
    return render(request, 'home.html', {'api_result': api_result})
  else:
    return render(request, 'home.html', {'ticker': "enter a ticker symbol above.."})
  
# about view
def about(request):
  return render(request, 'about.html', {})