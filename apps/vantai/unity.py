
from django.conf import  settings
import requests, json
from .models import VantaihahaiMember, VantaihahaiMembership
def checkishasmembership(device):
    result = VantaihahaiMembership.objects.filter(device=device)
    return len(result)>0
def CreateVantaihahaiMember(device, member_id, name):
    new_memmber = VantaihahaiMember(member_id= member_id, name = name)
    new_memmber.save()

    vt_m_object = VantaihahaiMembership(device = device, member= new_memmber)
    vt_m_object.save()

    return vt_m_object


def CreatenewUser(username,password):
    url = f'https://vantaihahai.com/api/res.users'
    register_token = settings.VANTAIHAHAI_CONFIG['register_token']
    headers = {
        # 'Content-Type': 'application/json',
        # 'access_token': f'{access_token}'
    }

    print("Tao user moi ")
    data = {
            "register_token": register_token,
            "name": username,
            "email": f"{username}@vantaihahai.com",
            "password": password
        }
    response = requests.request("POST", url,  data=json.dumps(data))
    print(response)
    
    if response.status_code == 201:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

def GetToken(username,password):
    # user = order.user
    username = f'{username}@vantaihahai.com'
    url = f'https://vantaihahai.com/api/auth/get_tokens?username={username}&password={password}&access_lifetime=72000&refresh_lifetime=72000'
    # access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    # headers = {
    #     # 'Content-Type': 'application/json',
    #     'access_token': f'{access_token}'
    # }

    print("Lay thong tin tai xe: ")
   
    response = requests.request("GET", url)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

def GetThongtintaixe(driver_id):
    
    # user = order.user
    url = f'https://vantaihahai.com/api/res.users/{driver_id}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Lay thong tin tai xe: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

def tatcachuyendicuataixe(emmployeeid = None):
    # user = order.user
    if emmployeeid:
        url = f'https://vantaihahai.com/api/fleet.trip?employee_id={emmployeeid}'
    else:
        url = 'https://vantaihahai.com/api/fleet.trip'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Lay tatca chuyen tai xe: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None


def cacchuyendihomnaycuataixe(emmployeeid):
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip?date=today&employee_id={emmployeeid}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Cac chuyen di hom nay: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None



def danhsachtatcaxe():
    # user = order.user
    url = f'https://vantaihahai.com/api/maintenance.equipment'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Dan sach tat ca xe: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None



def thongtinxe(equimentid):
    # user = order.user
    url = f'https://vantaihahai.com/api/maintenance.equipment/{equimentid}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Get Thong tin xe: ", equimentid)
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None



def danhsachyeucaubaotrixe(equimentid):
    # user = order.user
    url = f'https://vantaihahai.com/api/maintenance.request?equipment_id={equimentid}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Danh sach yeu cau bao tri xe: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None




def danhsachcactinh():
    # user = order.user
    url = f'https://vantaihahai.com/api/province'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Dan sach cac tinh: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None


def danhsachcachuyentheotinh(stateid):
    # user = order.user
    url = f'https://vantaihahai.com/api/district?state_id={stateid}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Danh sach huyen theo tinh: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None


def danhsachcacphuongtheohuyen(district_id):
    # user = order.user
    url = f'https://vantaihahai.com/api/ward?district_id={district_id}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Danh sach yeu cau bao tri xe: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None


def capnhatsokmbatdauhanhtrinh(hanhtrinh, sokm, body):
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip/{hanhtrinh}/do_odometer_start?odometer_start={sokm}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Cap nhat so km bat dau ")
   
    response = requests.request("PUT", url, headers=headers, data=json.dumps(body))
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

def capnhatsokmketthuchanhtrinh(hanhtrinh, sokm, body):
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip/{hanhtrinh}/do_odometer_end?odometer_end={sokm}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Cap nhat so km ket thuc ")
   
    response = requests.request("PUT", url, headers=headers, data=json.dumps(body))
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None



def capnhatghichubaotri(equitment, ghichu, body):
    # user = order.user
    url = f'https://vantaihahai.com/api/maintenance.equipment/{equitment}/create_maintenance_request?note={ghichu}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print(f"Cap nhat ghi chu: {ghichu} cho xe: {equitment}")
   
    response = requests.request("PUT", url, headers=headers, data=json.dumps(body))
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None


def themmoichuyendi(body):
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip'
   
    print("Them moi chuyen di")
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    response = requests.request("POST", url,headers=headers, data=json.dumps(body))
    print(response)
    print(response.json())
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None



def danhsachmathang():
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.product'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Dan sach cac mat hang: ")
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

def chitiethanhtrinh(hanhtrinh):
     # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip/{hanhtrinh}'
    access_token = settings.VANTAIHAHAI_CONFIG['access_token']
    headers = {
        # 'Content-Type': 'application/json',
        'access_token': f'{access_token}'
    }

    print("Chi tiet hanh trinh: ", hanhtrinh)
   
    response = requests.request("GET", url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        # order.haravan_order = response_json['order']['name']
        # order.save() 
        response_json =  response.json()
        return response_json
    else:
        return None

