import requests
import time
import threading
import urllib3

urllib3.disable_warnings()

def url_request_get(url):
    r = requests.get(url, verify= False, timeout=3)
    if r.status_code == 200:
        json_dic = r.json()
        return (r.status_code, json_dic)
    else:
        return (r.status_code, None)

def player_death_score(json_dic):
    try:
        player_id = json_dic["activePlayer"]["riotId"]
        for cha in json_dic["allPlayers"]:
            if cha["riotId"] == player_id:
                return (player_id, cha["scores"]["deaths"])
        return (None, None)
    except KeyError:
        return (None, None)
    
def api(fps, resolution, url:str, after_death_second, after_death, flag, buffer):
    previous_death_score = None
    while not flag.is_set():
        try:
            status_code, json_dic = url_request_get(url)
            if status_code != 200:
                print(f"[Error Code: {status_code}] Sunucuyla başarılı bağlantı sağlanamadı")
            else:
                player, death_score = player_death_score(json_dic)
                print(f"Oyuncu:{player} | Ölüm:{death_score}")
                if player is None:
                    print("Oyuncu Bulunamadı")
                else:
                    if previous_death_score is None:
                        previous_death_score = death_score
                    elif death_score > previous_death_score:
                        print(f"Öldün! (Toplam:{death_score})")
                        previous_death_score = death_score
                        threading.Thread(target=after_death, args=(fps, resolution, after_death_second, buffer), daemon=True).start()

        except requests.exceptions.ConnectTimeout:
            print("Hata Maça Bağlanılamadı (exceptions.ConnecTimeout)")
        except requests.exceptions.ConnectionError:
            #Maçta değilse bu kısım çalışır
            previous_death_score = None
            print("Hata Maç Açık Değil (exceptions.ConnectionError)")
        except requests.exceptions.ReadTimeout:
            print("Hata Maça Bağlanıldı ama Cevap Gelmedi (exceptions.ReadTimeout)")
        time.sleep(0.5)