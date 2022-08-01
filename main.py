import string, random, sys, os, ctypes, threading, requests, configparser, time, pyfade
from itertools import cycle
from pystyle import *

def refreshTitle():
    global successful, failed
    accs_per_min=0
    starttime=time.time()

    while True:
        if successful!=0:
            accs_per_min=round(successful/((time.time()-starttime)/60))
        ctypes.windll.kernel32.SetConsoleTitleW(f"SpotiGen | Rate: {accs_per_min}/min | successful: {successful} | Failed: {failed} | Threads: {threading.active_count()}")

def getRandomString(length):
    pool=string.ascii_lowercase+string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def getList(fileName: str) -> list:
        try:
            with open(fileName, 'r') as f:
                content = f.read().splitlines()
                f.close()
            return(content)
        except FileNotFoundError:
            return([])

def getProxy():
    return({"https://": f"http://{next(proxies_rotated)}"})

def checkProxy(proxy):
    global dead_proxies, all_proxies_dead

    if len(proxies)-len(dead_proxies)<=1:
        all_proxies_dead=True
        return "stop"

    if proxy in dead_proxies:
        return "dead"
    else:
        return "alive"

def printt(text):
    sys.stdout.write("\n"+text)

def genAccount():
    global successful, failed, dead_proxies, all_proxies_dead
    nick = acc_name+" | "+getRandomText(5)
    passw = getRandomString(12)
    email = getRandomText(7)+"@gmail.com"

    while True:
        active_proxy=getProxy()
        result_proxy=checkProxy(active_proxy)
        if result_proxy=="stop":
            break
        elif result_proxy=="dead":
            dead_proxies.append(active_proxy)
        else:
            break

    if all_proxies_dead==True:
        return


    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.72",
             "X-Client-Id": getRandomString(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": "male" if random.randint(0, 1) else "female",
            "birth_year": random.randint(1990, 2000),
            "displayname": nick,
            "iagree": "true",
            "birth_month": random.randint(1, 11),
            "password_repeat": passw,
            "password": passw,
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": email,
            "birth_day": random.randint(1, 20)}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload, proxies=active_proxy)

    if r.status_code==200:
        if r.json()['status']==1:
            successful=successful+1
            result=f"+ | {email}:{passw} | successful"
            combos.append(email+":"+passw)
            printt(result)
            return
        else:
            failed=failed+1
            result=f"- | {email}:{passw} | dead proxy"
            if r.status_code==429:
                result=f"- | {email}:{passw} | ratelimited proxy"
                dead_proxies.append(active_proxy)
            printt(result) 
            return
    else:
        failed=failed+1
        result=f"- | {email}:{passw} | dead proxy"
        if r.status_code==429:
            result=f"- | {email}:{passw} | ratelimited proxy"
            dead_proxies.append(active_proxy)
        printt(result) 
        return

if __name__ == "__main__":
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW(f"SpotiGen | Rate: N/A | successful: 0 | Failed: 0 | Threads: 0")

    config = configparser.ConfigParser()
    config.read("settings.ini")
    proxy_file=config["Settings"]["proxies"]
    result_file=config["Settings"]["result"]
    accs_to_gen=config["Settings"]["accounts to gen"]
    max_threads=config["Settings"]["max threads"]
    acc_name=config["Settings"]["account name"]

    accs_to_gen=int(accs_to_gen)
    max_threads=int(max_threads)
    currentaccs=len(getList(result_file))
    proxies=getList(proxy_file)
    proxies_rotated=cycle(proxies)
    all_proxies_dead=False
    threads=[]
    combos=[]
    dead_proxies=[]
    successful=0
    failed=0

    ascii="""
███████╗██████╗  ██████╗ ████████╗██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝ ██╔════╝████╗  ██║
███████╗██████╔╝██║   ██║   ██║   ██║██║  ███╗█████╗  ██╔██╗ ██║
╚════██║██╔═══╝ ██║   ██║   ██║   ██║██║   ██║██╔══╝  ██║╚██╗██║
███████║██║     ╚██████╔╝   ██║   ██║╚██████╔╝███████╗██║ ╚████║
╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝"""
    print(pyfade.Fade.Vertical(pyfade.Colors.green_to_black, Center.XCenter(ascii)))
    print(pyfade.Fade.Horizontal(pyfade.Colors.green_to_black, text = f"""┌────────────────────────────────────────────────────────────────────────────────────────┐"""))
    print(pyfade.Fade.Horizontal(pyfade.Colors.yellow_to_green, text = f"Accounts to gen: {accs_to_gen} | Threads: {max_threads} | Proxies: {len(proxies)} | email:password | {result_file}".center(os.get_terminal_size().columns)))
    print(pyfade.Fade.Horizontal(pyfade.Colors.green_to_black, text = f"""└────────────────────────────────────────────────────────────────────────────────────────┘"""))
    input(pyfade.Fade.Horizontal(pyfade.Colors.yellow_to_green, text = f"""Press enter to start..."""))

    threading.Thread(target=refreshTitle).start()
    while successful<accs_to_gen:
        if all_proxies_dead==False:
            if threading.active_count()<=max_threads:
                threading.Thread(target=genAccount).start()
        else:
            break

    accountsnow=len(getList(result_file))

    time.sleep(5)

    print("")
    if all_proxies_dead==True:
        printt("All proxies dead/ratelimited,\ntry again in over an hour or with different proxies")
    printt(f"Finished. Combos saved into {result_file}")
    printt(f"Generated {successful} accounts")
    printt(f"Total accounts in {result_file}: {accountsnow}")
    printt("Press enter to exit...")
    with open(result_file, "a") as f:
        for combo in combos:
            f.write(combo+"\n")
        f.close()
    input("")
    os._exit(1)

