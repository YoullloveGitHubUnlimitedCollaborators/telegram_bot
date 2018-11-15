import Variables as var
import requests
import datetime
import time
import re

upd = var.telegram_methods['updates']
send = var.telegram_methods['send']

class MyBot:

    def __init__(self, bot_token=None, ):
        self.token = bot_token

    def get_updates(self, offset=None, timeout = 30):
        params = {'timeout': timeout, 'offset': offset}
        res = requests.get(var.telegram_api_url.format(self.token)+upd, params)
        result_json = res.json()['result']
        return result_json

    def get_chat_id(self):
        return self.get_updates(self.token)['result'][-1]['message']['chat']['id']

    def get_last_message(json_answer):
        text_answer = json_answer['result'][-1]['message']['text']
        return text_answer

    def send_message(self, chat_id, text):
        params = {'chat_id':chat_id,'text':text}
        res = requests.post(var.telegram_api_url.format(var.telegram_token)+send, params)
        return res

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            print(get_result[-1])
            print(len(get_result))
            last_update = get_result[-1]
        else:
            print(get_result[len(get_result)-1])
            print(len(get_result))
            last_update = get_result[len(get_result)-1]

        return last_update
    def timeconvert(self,seconds):
        minutes = seconds % 3600
        hours = minutes % 216000
        return "%02d:%02d" % (hours, minutes)


ThisBot = MyBot(var.telegram_token)
now = datetime.date.today()


def echo_wait():
    new_offset = None

    while True:
        ThisBot.get_updates(new_offset)

        last_update = ThisBot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']

        if last_chat_text == "/currencynow":
            message = requests.get(var.bank_api_url).json()
            for x in range(len(message)):

                if message[x]['Cur_Abbreviation'] == 'USD':
                    result = 'За '+str(now)+' курс '+str(message[x]["Cur_OfficialRate"])+' за 1 '+str(message[x]['Cur_Name'])
                    ThisBot.send_message(last_chat_id,result)

                if message[x]['Cur_Abbreviation'] == 'EUR':
                    result = 'За '+str(now)+' курс '+str(message[x]["Cur_OfficialRate"])+' за 1 '+str(message[x]['Cur_Name'])
                    ThisBot.send_message(last_chat_id,result)

        if last_chat_text == "/currencydate":
            ThisBot.send_message(last_chat_id, 'Курс валют за какую дату вас интересует?')
            ThisBot.send_message(last_chat_id, 'В формате YYYY-MM-DD')
            cd_offset = new_offset
            while True:
                ThisBot.get_updates(cd_offset)
                last_update = ThisBot.get_last_update()
                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']

                time.sleep(10)
                if last_chat_text != "/currencydate" and re.match(r'\d{4}-\d{2}-(\d{2})',last_chat_text):
                    rec = var.bank_api_url1+var.bank_methods['onDate']+last_chat_text+var.bank_methods['today']
                    message = requests.get(rec).json()
                    for x in range(len(message)):

                        if message[x]['Cur_Abbreviation'] == 'USD':
                            result = 'За ' + last_chat_text + ' курс ' + str(message[x]["Cur_OfficialRate"]) + ' за 1 ' + str(
                                message[x]['Cur_Name'])
                            ThisBot.send_message(last_chat_id, result)

                        if message[x]['Cur_Abbreviation'] == 'EUR':
                            result = 'За ' + last_chat_text + ' курс ' + str(message[x]["Cur_OfficialRate"]) + ' за 1 ' + str(
                                message[x]['Cur_Name'])
                            ThisBot.send_message(last_chat_id, result)
                    break
                else:
                    ThisBot.send_message(last_chat_id, "Пожалуйста следуйте формату ввода даты: YYYY-MM-DD")
                    time.sleep(10)


        if last_chat_text == "/weathernow":
            req = var.weather_api_url+var.weather_methods['day']+"Minsk"+var.weather_token
            message = requests.get(req).json()
            place = "\t\t"+message["name"]+"\n"
            date = "Сегодня: "+time.strftime("%a, %d %b %Y", time.localtime(message['dt']))+"\n"
            aver_temp = "Темерпатура: "+str(round(message['main']['temp']-273.15))+" по цельсию"+"\n"
            pressure = "Давление: "+str(round(message['main']['pressure']))+" pHA\n"
            sunrise = "Восход: "+time.strftime("%H:%M:%S ", time.localtime(message['sys']['sunrise']))+"\n"
            sunset = "Закат: "+time.strftime("%H:%M:%S ", time.localtime(message['sys']['sunset']))
            result_message = place + date + aver_temp + pressure + sunrise + sunset
            print(result_message)
            ThisBot.send_message(last_chat_id,result_message)

        if last_chat_text == "/weatherweek":
            req = var.weather_api_url + var.weather_methods['week'] + "Minsk" + var.weather_token
            message = requests.get(req).json()

            for x in range(len(message)):
                place = "\t\t" + message['city']["name"] + "\n"
                date = "Сегодня: " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(message['list'][x]['dt'])) + "\n"
                print(date)
                # aver_temp = "Темерпатура: " + str(round(message['main']['temp'] - 273.15)) + " по цельсию" + "\n"
                # pressure = "Давление: " + str(round(message['main']['pressure'])) + " pHA\n"
                # sunrise = "Восход: " + time.strftime("%H:%M:%S ", time.localtime(message['sys']['sunrise'])) + "\n"
                # sunset = "Закат: " + time.strftime("%H:%M:%S ", time.localtime(message['sys']['sunset']))
                # result_message = place + date + aver_temp + pressure + sunrise + sunset
                # print(result_message)
                # ThisBot.send_message(last_chat_id, result_message)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        echo_wait()
    except KeyboardInterrupt:
        exit()