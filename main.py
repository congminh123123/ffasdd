from distutils.command.config import config
import json, threading
import time, random, requests, os
from typing import Type
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service
from tkinter import CENTER, Label, Scrollbar, ttk, Tk, Button, font, IntVar, Checkbutton, messagebox,Entry,StringVar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from anycaptcha import AnycaptchaClient, RecaptchaV2TaskProxyless
import subprocess
# from cryptography.fernet import Fernet
import base64
import pprint
def solve_captcha(api_key):
    url = "https://taki.app"
    site_key = "6LfmRGUfAAAAAGG5FhRIf35aqavpta2VR28un4v6"
    # api_key = api
    client = AnycaptchaClient(api_key)
    is_invisible=True
    task = RecaptchaV2TaskProxyless(website_url=url, website_key=site_key,is_invisible=is_invisible)
    job = client.createTask(task)
    job.join(200)
    result=job.get_solution_response()
    
    return result

def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log

def chuc_nang():
    def ChucNang(vitri):
        while True:
            stt = Taki_App.check_stt
            Taki_App.check_stt += 1
            profile = Taki_App.list_profile[stt]
            Taki_App.table.item(Taki_App.table.get_children()[stt], \
                text="blub", values=(stt + 1, profile["name"], "Đang mở profile", time.strftime("%H:%M:%S", time.localtime()))) # Cập nhật trạng thái profile
            try:
                capabilities = DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
                # Gọi profile bằng api
                remotePort = str(random.randint(9000, 12000))
                requests.get(f"http://{Taki_App.API_URL}/v2/start?profile_id=%s&remote_debug_port=%s&addination_args=--window-size=1200,1000 --window-position=%s,%s"%(profile["id"], remotePort, 0, 0))
                time.sleep(3)
                options = Options()
                service = Service(file_config["foldergmp"] + "\\gpmdriver.exe")
                # service.creationflags = CREATE_NO_WINDOW
                options.debugger_address = f'127.0.0.1:{remotePort}'
                browser = webdriver.Chrome(service= service,desired_capabilities=capabilities, options=options)
                wait, action = WebDriverWait(browser, 2), ActionChains(browser)
                Taki_App.table.item(Taki_App.table.get_children()[stt], \
                    text="blub", values=(stt + 1, profile["name"], "Mở chrome thành công", time.strftime("%H:%M:%S", time.localtime()))) # Cập nhật trạng thái profile
                browser.switch_to.window(browser.current_window_handle)
                time.sleep(2)
            except:
                try:
                    for handle in browser.window_handles:
                        browser.switch_to.window(handle)
                        browser.close()
                except:
                    pass
                return

            try:
                browser.get("https://taki.app/wallet/?staking=true")
                Taki_App.table.item(Taki_App.table.get_children()[stt], \
                    text="blub", values=(stt + 1, profile["name"], "Stake", time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(5)
                # js_user = '''return document.querySelector("#__next > div.css-qx5r5a.ej2twmx21 > div > aside > div.css-168cv3d.eajy9i89 > div.css-14e08vj.ej2twmx21 > div.css-1gk9w.eajy9i87 > div.css-1b77vh5.eajy9i86").click()'''
                # browser.execute_script(js_user)
                time.sleep(1)
                browser.get("https://taki.app")
                wait.until(EC.presence_of_element_located((By.ID, "header")))
                Taki_App.table.item(Taki_App.table.get_children()[stt], \
                    text="blub", values=(stt + 1, profile["name"], "Feed", time.strftime("%H:%M:%S", time.localtime())))
                # js_top = '''return document.querySelector("#content-wrapper > div.css-g4jln6.eno6ygk2 > div > div > div > div:nth-child(1)").click()'''
                # browser.execute_script(js_top)
                logs = browser.get_log("performance")
                events = process_browser_logs_for_network_events(logs)
                author = ''
                check_id = False
                check_author = False
                id_user = ''
                # for request in browser.requests:  
                #     if request.response:  
                #         print(  
                #             request.url,  
                #             request.response.status_code,  
                #             request.response.headers['Content-Type'])  

                # with open("log_entries.txt", "a") as out:
                #     for event in events:
                #         pprint.pprint(event, stream=out)
                with open("log_entries1.txt", "a") as out:
                    for event in events:
                        try:
                            word = "refresh_token"
                            auth_raw = event['params']['request']['postData']
                            test = str(auth_raw)
                            # auth_raw = event['params']['documentURL']['postData']
                            if (event['params']['documentURL'] == "https://taki.app/wallet/?staking=true"):
                                # pprint.pprint(event, stream=out)
                                auth_raw_1 = event['params']['request']
                                # with open("log_entries1.txt", "a") as out:
                                #     out.write(str(auth_raw_1) + '\n')
                                # print(auth_raw = event['params']['request'])
                            test_1 = test.split("refresh_token")
                            if (len(test_1) > 2):
                                # with open("log_entries2.txt", "a+") as out1:
                                #     out1.write(profile["name"]+"|"+test + '\n')
                                with open("log_entries.txt", "a+") as out2:
                                    out2.write(profile["name"]+"|"+test_1[2] + '\n')
                            auth_raw = event['params']['request']['headers']['Authorization']
                            # print(event['params']['documentURL'])
                            if (event['params']['documentURL'] == "https://taki.app/home/"):
                                # print(event['params']['request']['url'])
                                url_e = event['params']['request']['url'].split('https://firestore.googleapis.com/v1/projects/gettaki-production/databases/(default)/documents/users/')
                                id_user = url_e[1].split(':')[0]
                                # print(id_user)
                                check_id = True


                            if len(auth_raw) > 20:
                                author = auth_raw
                                check_author = True
                                # break
                            if check_author & check_id:
                                break

                        except:
                            pass
                # Author = author.strip()
                # js_user = '''return document.querySelector("#__next > div > div > div.css-qx5r5a.ej2twmx21 > div > aside > div.css-168cv3d.eajy9i89 > div.css-14e08vj.ej2twmx21").click()'''
                # browser.execute_script(js_user)
                # time.sleep(1)
    
                time.sleep(2)
                headers_share = {
                        'authority': 'asia-southeast1-gettaki-production.cloudfunctions.net',
                        'accept': '*/*',
                        'accept-language': 'vi',
                        'authorization': f'{author.strip()}',
                        'content-type': 'application/json',
                        'origin': 'https://taki.app',
                        'referer': 'https://taki.app',
                        'sec-ch-ua': '"" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                    }
                
                # if "Complete the captcha to continue to Taki" in browser.page_source:
                #     for i in range(7):
                #         try:
                #             api_key = solve_captcha(file_config["api_anycaptcha"])

                #             url_get_capt = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/user-updateCaptcha'
                #             data_get_capt = {
                #                 'data':{'id':f'{id_user}','captchaToken':f'{api_key}'}
                #             }
                #             response = requests.post(url_get_capt, headers=headers_share, json=data_get_capt)
                #             result_api = json.loads(response._content.decode('utf-8'))
                #             t= result_api['result']['result']
                #             if t:
                #                 break
                #             time.sleep(1)
                #         except:
                #             pass
                    
                # try:
                #     url_share = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/reward-completeTweetAction'
                #     data_share = {
                #         'data': 'null'
                #     }
                #     response = requests.post(url_share, headers=headers_share, json=data_share)
                #     Taki_App.table.item(Taki_App.table.get_children()[stt], \
                #     text="blub", values=(stt + 1, profile["name"], "Tweet", time.strftime("%H:%M:%S", time.localtime())))
                # except:
                #     pass


                
                # try:
                #     Taki_App.table.item(Taki_App.table.get_children()[stt], \
                #     text="blub", values=(stt + 1, profile["name"], "Buy Taki", time.strftime("%H:%M:%S", time.localtime())))
                #     data_share = {
                #         'data':{'idempotencyKey':'8dfd25f3-fcac-47ca-9b57-326ea134cc8a','source':'TAKI','sourceAmount':0.05,'target':f'{file_config["user_1"]}','targetAmountEstimated':5}
                #     }
                #     url_buy = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/coin-buy'

                #     response = requests.post(url_buy, headers=headers_share, json=data_share)
                #     if response.status_code != 200:
                #         time.sleep(1)
                #         response = requests.post(url_buy, headers=headers_share, json=data_share)
                       
    
                #     time.sleep(1)
                #     data_share = {
                #         'data':{'idempotencyKey':'8dfd25f3-fcac-47ca-9b57-326ea134cc8a','source':'TAKI','sourceAmount':0.05,'target':f'{file_config["user_2"]}','targetAmountEstimated':5}
                #     }
                #     url_buy = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/coin-buy'

                #     response = requests.post(url_buy, headers=headers_share, json=data_share)
                #     if response.status_code != 200:
                #         time.sleep(1)
                #         response = requests.post(url_buy, headers=headers_share, json=data_share)
                        
                #     time.sleep(1)
                #     data_share = {
                #         'data':{'idempotencyKey':'8dfd25f3-fcac-47ca-9b57-326ea134cc8a','source':'TAKI','sourceAmount':0.05,'target':f'{file_config["user_3"]}','targetAmountEstimated':5}
                #     }
                #     url_buy = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/coin-buy'

                #     response = requests.post(url_buy, headers=headers_share, json=data_share)
                #     if response.status_code != 200:
                #         time.sleep(1)
                #         response = requests.post(url_buy, headers=headers_share, json=data_share)
                #     time.sleep(1)

                # except:
                #     pass

                # try:
                #     Taki_App.table.item(Taki_App.table.get_children()[stt], \
                #     text="blub", values=(stt + 1, profile["name"], "Give Taki", time.strftime("%H:%M:%S", time.localtime())))
                #     for i in range(7):
                #         with open("list_post.txt", mode="r") as file:
                #             done_profile = file.read().strip("\n").split("\n")
                #         id_post = random.randint(0, len(done_profile))
                #         data_like = {
                #             'data':{'entityId':f'{done_profile[id_post]}','entityType':'post'}
                #         }
                #         url_like = 'https://asia-southeast1-gettaki-production.cloudfunctions.net/paidLike-buy'

                #         # response = requests.post(url_like, headers=headers_share, json=data_like)

                #         result_api = json.loads(response._content.decode('utf-8'))
                #         t= result_api['result']['result']
                #         if t:
                #             break
                #         time.sleep(1)
                # except:
                #     pass
                
            except:
                pass

            try:
                for handle in browser.window_handles: # Đóng chrome sau khi chạy xong
                    browser.switch_to.window(handle)
                    browser.close()
            except:
                pass
            try:
                Taki_App.table.item(Taki_App.table.get_children()[stt], \
                    text="blub", values=(stt + 1, profile["name"], "Hoàn tất!", time.strftime("%H:%M:%S", time.localtime()))) # Cập nhật trạng thái profile
            except:
                quit()
    # Cấu hình
    with open("config\\config.json", mode= "r", encoding="utf-8-sig") as file:
        file_config = json.loads(file.read())
    for luong in range(20000):
        threads = []
        for vitri in range(file_config["thread"]):
            threads += [threading.Thread(target=ChucNang, args={vitri})]
        for t in threads:
            t.start()
            time.sleep(1)
        for t in threads:
            t.join(500)



class giao_dien():
    def __init__(self):
        # Khai báo giao diện chính
        self.giao_dien_chinh = Tk()
        self.giao_dien_chinh.title('Taki app v2.0')
        WA= self.giao_dien_chinh.winfo_screenwidth()
        MA= self.giao_dien_chinh.winfo_screenheight()
        self.giao_dien_chinh.geometry('700x451+%d+%d' %(WA/2-350, MA/2-280))
        # Khai báo font chữ
        self.text_font_10 = font.Font(family="Helvetica", size=10, weight='bold')
        self.text_font_15 = font.Font(family="Helvetica", size=15, weight='bold')
    def back_ground(self):
        # Hàm điều khiển chrome
        def bat_dau():
            self.API_CLOSE = False
            self.check_stt = 0
            with open("check threaded.dat", mode="w") as file:
                file.write(str(0))
            threading.Thread(target=chuc_nang).start()
        btn_bat_dau = Button(self.giao_dien_chinh, width=15, text="Khởi Chạy", command= bat_dau)
        btn_bat_dau['font'] = self.text_font_15
        btn_bat_dau.place(x= 1, y= 10, width= 140, height= 40)
        def btn_close_chrome():
            self.API_CLOSE = True
        btn_close_chrome = Button(self.giao_dien_chinh, width=15, text="Đóng chrome", command= btn_close_chrome)
        btn_close_chrome['font'] = self.text_font_15
        btn_close_chrome.place(x= 1, y= 55, width= 140, height= 40)
        # Button chức năng của treeview
        def btn_change_value(): # Tải lại Profile
            try:
                with open("config\\config.json", mode= "r", encoding="utf-8-sig") as file:
                    file_config = json.loads(file.read())
                    with open(file_config["folder gmp"] + "\\api_port.dat", mode="r") as file:
                        self.API_URL = "127.0.0.1:" + file.read()
                        self.list_profile, abc = requests.get(f"http://{self.API_URL}/v2/profiles").json(), []
                        for i in Taki_App.table.get_children():
                            self.table.delete(i)
                        for check_pro in range(file_config["start_id"], file_config["end_id"]):
                            for check_prof in self.list_profile:
                                if str(check_pro) == check_prof["name"]:
                                    abc.append(check_prof)
                                    break
                        self.list_profile = abc
                        for i in range(1000000):
                            try:
                                profile = self.list_profile[i]
                                self.table.insert("",'end',text="L1",values=(i + 1, profile["name"], "", ""))
                            except:
                                break
                        messagebox.showinfo("Thông báo!", "Cập nhật profile thành công")
            except:
                messagebox.showerror("Thông báo lỗi!", "Vui lòng sửa lại đường dẫn folder GMPLogin")
                os.popen("config\\config.json")
                quit()
        btn_change_value = Button(self.giao_dien_chinh, width=15, text="Tải lại Profile", command= btn_change_value)
        btn_change_value['font'] = self.text_font_10
        btn_change_value.place(x= 597, y= 77, width= 103, height= 22)
        def btn_config(): # Sửa config
            os.popen("config\\config.json")
        btn_config = Button(self.giao_dien_chinh, width=15, text="Sửa config", command= btn_config)
        btn_config['font'] = self.text_font_10
        btn_config.place(x= 512, y= 77, width= 85, height= 22)
        def btn_config(): # Đóng chrome khẩn cấp
            self.API_CLOSE = True
            os.system("powershell.exe -command Stop-Process -Name 'chrome'")
        btn_config = Button(self.giao_dien_chinh, width=15, text="Đóng chrome khẩn cấp", command= btn_config)
        btn_config['font'] = self.text_font_10
        btn_config.place(x= 350, y= 77, width= 165, height= 22)
        # Lựa chọn chức năng
        current_machine_id = subprocess.check_output('wmic csproduct get uuid').split('\n')[1].strip()
        print(current_machine_id)
        self.CheckVar1 = StringVar() 
        Checkbtn_1 = Entry(self.giao_dien_chinh, textvariable = self.CheckVar1) # Random search từ khóa
        # Checkbtn_1 = Checkbutton(self.giao_dien_chinh, text = "Key", variable = self.CheckVar1,
        #                         onvalue = 0, offvalue = 1)
        Checkbtn_1.configure(font=self.text_font_10)
        Checkbtn_1.place(x= 150, y= 0, width= 300, height= 40)
        self.CheckVar1.set(current_machine_id)

        self.table = ttk.Treeview(self.giao_dien_chinh, columns= ("STT", 'Tên profile', 'Trạng Thái', 'Thời Gian'), show='headings')
        self.table.place(x= 0, y= 100, width= 680, height= 350) # Vị trí Treeview
        vsb = Scrollbar(self.giao_dien_chinh, orient="vertical", command=self.table.yview)
        vsb.place(x= 680, y= 101, height=348) # Vị trí thanh scroll
        self.table.configure(yscrollcommand=vsb.set) # Liên kết Treeview và thanh scroll
        self.table.heading('STT', text='STT')
        self.table.heading('Tên profile', text='Tên profile')
        self.table.heading('Trạng Thái', text='Trạng Thái')
        self.table.heading('Thời Gian', text='Thời Gian')
        self.table.column('#0', minwidth=0, width=0)
        self.table.column('#1', stretch= False, minwidth=20, width=30, anchor= CENTER)
        self.table.column('#2', stretch= False, minwidth=70, width=150, anchor= CENTER)
        self.table.column('#3', stretch= True, minwidth=100, width=350)
        self.table.column('#4', stretch= True, minwidth=100, width=100, anchor= CENTER)
        with open("config\\config.json", mode= "r", encoding="utf-8-sig") as file:
                file_config = json.loads(file.read())

        try:
            with open(file_config["foldergmp"] + "\\api_port.dat", mode="r") as file:
                self.API_URL = "127.0.0.1:" + file.read()
                self.list_profile, abc = requests.get(f"http://{self.API_URL}/v2/profiles").json(), []
                for check_pro in range(file_config["start_id"], file_config["end_id"]):
                    for check_prof in self.list_profile:
                        if str(check_pro) == check_prof["name"]:
                            abc.append(check_prof)
                            break
                self.list_profile = abc
                for i in range(100000):
                    try:
                        profile = self.list_profile[i]
                        self.table.insert("",'end',text="L1",values=(i + 1, profile["name"], "", ""))
                    except:
                        break
        except:
            messagebox.showerror("Thông báo lỗi!", "Vui lòng sửa lại đường dẫn folder GMPLogin")
            os.popen("config\\config.json")
            quit()
if __name__ == "__main__":
    Taki_App = giao_dien()
    Taki_App.back_ground()
    Taki_App.giao_dien_chinh.mainloop()