import requests
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = ""
account_sid = "twilio계정의 ID"
auth_token = "twilio에서의 auth_token"


weather_params = {
    "lat": 0.0, # 날씨를 알고 싶은 지역의 위도
    "lon": 0.0, # 날씨를 알고 싶은 지역의 경도
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:   # 자기자신에게 메시지 보내기
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔",          # 자기자신에게 보낼 텍스트
        from_="",                                              # twilio에서 받은 전화번호(Trial number)
        to="your verified number"                                          # twilio에 등록한 전화번호(본인 전화번호)
    )
    print(message.sid)  # 메시지가 id를 생성했다면 성공적으로 전송되었다는 것을 의미

