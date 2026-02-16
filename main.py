import winreg
import json
import shutil
import os
from tkinter import *
from tkinter import ttk
import traceback
import vdf

def exit():
    os._exit(0)

tk = Tk()
Id = {}
tk.protocol("WM_DELETE_WINDOW", exit)
tk.geometry("1000x600+450+250")
AccInFolder = {}
IDV2= {}
try:
    with open('pyconfig.json', 'r',encoding='utf-8') as f:
        Id = json.load(f)
except:
    print('No file')
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
    path, _ = winreg.QueryValueEx(key, "SteamPath")
    winreg.CloseKey(key)
    vdfPath = path
    path = path + '/userdata/'
except FileNotFoundError:
    print('Steam Error')

vdfFile = vdf.load(open(vdfPath + '/config/' + 'loginusers.vdf', 'r', encoding='utf-8'))
for i in Id.values():
    IDV2[i] = int(i) + 76561197960265728
for i in (vdfFile['users'].keys() - IDV2):
    
    if str(int(i)-76561197960265728) in set(os.listdir(path)):
        AccInFolder[vdfFile['users'][str(i)]['PersonaName']] = int(i) - 76561197960265728
        print(AccInFolder)
    else:
        print(str(int(i)-76561197960265728))

if not os.path.isdir('files'):  
    os.mkdir('files')
    print('Folder Created')
    
def Save(Id):
    try:
        with open('pyconfig.json', 'w', encoding='utf-8') as f:
            json.dump(Id, f,ensure_ascii=False,)
    except:
        print('Save Error')


def New():
    global Id  
    try:
        accName = id_list.get()
        accId = AccInFolder[accName]
        accId = str(accId)
        try:
            shutil.copytree(path+accId, f'files\\'+accId)
            try:
                Id[accName] = accId
                Save(Id)
                print(Id)
            except Exception:
                print(traceback.format_exc()) 
                print('Error 3')
        except Exception:
            print(traceback.format_exc()) 
            print('Error №2 NEW, Coping')
    except:
        print('Error NEW 1')
    
def Del():
    delAcc = del_list.get()
    shutil.rmtree('files/' + Id[delAcc])
    del Id[delAcc]
    Save(Id)

    
def ComboUpdate():
    list_Set.configure(values=list(Id.keys()), state="readonly")
    list_Set_1.configure(values=list(Id.keys()), state="readonly")
    id_list.configure(values=list(set(AccInFolder.keys()) - set(list(Id.keys()))), state="readonly")
    del_list.configure(values=list(Id.keys()), state="readonly")
    try: id_list.current(0) 
    except:
        pass

        
        
       
def Clear():
    try:
        os.remove('pyconfig.json')
        shutil.rmtree('files')
        os._exit(0)
    except:
        os._exit(0)
def Set(): 
    try:
        ac1 = list_Set.get()
        ac2 = list_Set_1.get()
        if ac1 in Id:
            if ac2 in Id:
                shutil.rmtree(path+Id[ac2])
                shutil.copytree(f'files\\'+Id[ac1], path+Id[ac2], dirs_exist_ok=True)
                print('настройки замененны ')
            else:
                print('нет куда копировать')
        else:
            print('нет что копировать')
            print(ac1)
            print(ac2)
            print(Id)
    except:
        print('Ошибка Set')
def Update():
    try:
        for i in range(len(Id)):
            key = list(Id.values())[i]
            print('обработан ' + key)
            shutil.rmtree('files\\'+key)
            shutil.copytree(path+key, 'files\\'+key)
    except:
        print('ошибка Update')
        
def pr():
    print(Id)


ttk.Label(text='Для смены настроек ').place(relx=0.4, rely=0.08, anchor="c", relwidth=0.2, relheight=0.05)
ttk.Label(text='Добавление и удаление аккаунтов').place(relx=0.1, rely=0.08, anchor="c", relwidth=0.2, relheight=0.05)

#комбобоксы ----------------------------------------------------------------------------------------------------
list_Set_1 = ttk.Combobox(values=list(Id.keys()), state="readonly") # список ключей Set
list_Set = ttk.Combobox(values=list(Id.keys()), state="readonly") # список ключей Set

id_list = ttk.Combobox(values=list(set(AccInFolder.keys()) - set(list(Id.keys()))), state="readonly") #New
del_list = ttk.Combobox(values=list(Id.keys()), state="readonly") #Del


#комбобоксы place ----------------------------------------------------------------------------------------------

id_list.place(relx=0.1, rely=0.15, anchor="c", relwidth=0.2, relheight=0.07) #New
del_list.place(relx=0.1, rely=0.23, anchor="c", relwidth=0.2, relheight=0.07) #Del
list_Set.place(relx=0.4, rely=0.15, anchor="c", relwidth=0.2, relheight=0.07)
list_Set_1.place(relx=0.4, rely=0.23, anchor="c", relwidth=0.2, relheight=0.07)

ttk.Button(text='New', command=lambda: [New(),ComboUpdate()]).place(relx=0.25, rely=0.15, anchor="c", relwidth=0.1, relheight=0.07)
ttk.Button(text='Save Del', command=lambda: [Del(),ComboUpdate()]).place(relx=0.25, rely=0.23, anchor="c", relwidth=0.1, relheight=0.07)

ttk.Button(text='Set', command=lambda: [Set(),ComboUpdate()]).place(relx=0.56, rely=0.15, anchor="c", relwidth=0.1, relheight=0.07)
ttk.Button(text='Clear', command=Clear).place(relx=0.25, rely=0.45, anchor="c", relwidth=0.1, relheight=0.07)
ttk.Button(text='Print', command=pr).place(relx=0.35, rely=0.45, anchor="c", relwidth=0.1, relheight=0.07)
ttk.Button(text='Update', command=Update).place(relx=0.45, rely=0.45, anchor="c", relwidth=0.1, relheight=0.07)



tk.mainloop()

