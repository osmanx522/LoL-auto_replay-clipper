import requests
import time
import urllib3
import clipper.config as config

urllib3.disable_warnings()

def url_request_get(url):
    r = requests.get(url, verify= False, timeout=3)
    if r.status_code == 200:
        json_dic = r.json()
        return (r.status_code, json_dic)
    else:
        return (r.status_code, None)

def player_scores(json_dic):
    try:
        player_id = json_dic["activePlayer"]["riotId"]
        for cha in json_dic["allPlayers"]:
            if cha["riotId"] == player_id:
                return (player_id, cha["scores"])
        return (None, None)
    except KeyError:
        return (None, None)
    
def api(flag, on_works):
    previous_death_score = None
    previous_kill_score = None
    while not flag.is_set():
        try:
            status_code, json_dic = url_request_get(config.LOL_LOCAL_URL)
            if status_code != 200:
                print(f"[Error Code: {status_code}] Sunucuyla başarılı bağlantı sağlanamadı")
            else:
                player, score_dic  = player_scores(json_dic)
                if player is None:
                    print("Oyuncu Bulunamadı")
                else:
                    kills = score_dic["kills"]
                    deaths = score_dic["deaths"]
                    print(f"Player:{player} | Kills:{kills}| Deaths:{deaths}")
                    if previous_death_score is None and previous_kill_score is None:
                        previous_death_score = deaths
                        previous_kill_score = kills
                    if deaths > previous_death_score:
                        print(f"Öldün! (Toplam:{deaths})")
                        on_works("death")
                        previous_death_score = deaths
                    if kills > previous_kill_score:
                        print(f"Öldürdün! (Toplam:{kills})")
                        on_works("kill")
                        previous_kill_score = kills

        except requests.exceptions.ConnectTimeout:
            print("Hata Maça Bağlanılamadı (exceptions.ConnecTimeout)")
        except requests.exceptions.ConnectionError:
            #Maçta değilse bu kısım çalışır
            previous_death_score = None
            previous_kill_score = None
            print("Hata Maç Açık Değil (exceptions.ConnectionError)")
        except requests.exceptions.ReadTimeout:
            print("Hata Maça Bağlanıldı ama Cevap Gelmedi (exceptions.ReadTimeout)")
        time.sleep(0.5)