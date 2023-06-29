
from django.conf import  settings
import requests, json
from .models import VantaihahaiMember, VantaihahaiMembership
import xmlrpc.client
class VanTaiHaHai():
    def __init__(self):
        print('init hahai')
        try:
            self.url = settings.VANTAIHAHAI_CONFIG['url']
            self.db = settings.VANTAIHAHAI_CONFIG['db'] 
            self.username = settings.VANTAIHAHAI_CONFIG['username']
            self.password = settings.VANTAIHAHAI_CONFIG['password']
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = common.authenticate(self.db, self.username, self.password, {})
        except Exception as ex:
            print("day la: ", ex)
    def themmoichuyendi(self, body):
        print("Bat dau them moi chuyen di")
        # Get list chuyen di
       
        location_ids = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.location',  'search', [[]], {})
        list_locations = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.location', 'read',
                [location_ids],{'fields':['id','ward_id', 'district_id','state_id']})
    
        print("danh sach dia chir", list_locations)
      
        location_id = body['location_id']
        location_dest_id = body['location_dest_id']
        location_start = None
        location_dest = None
        for location in list_locations:
            try:
                if location['id'] == int(location_id):
                    print('tim thay: bat dau', location_id)
                    location_start = location
                if location['id'] == int(location_dest_id):
                    print('tim thay: kt', location_id)
                    location_dest = location
            except Exception as ex:
                print("except tao xe", ex)
        if location_start != None:
            body['ward_id'] = location_start['ward_id'][0]
            body['district_id'] = location_start['district_id'][0]
            body['state_id'] = location_start['state_id'][0]
        if location_dest != None:
            body['ward_dest_id'] = location_dest['ward_id'][0]
            body['district_dest_id'] = location_dest['district_id'][0]
            body['state_dest_id'] = location_dest['state_id'][0]
        print('chot ha: ', body)
        id_trip = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'create', [body])
       
        return id_trip
    def capnhatsokmketthuchanhtrinh(self, hanhtrinh, sokm, body, attackements=None):
        result = None
        try:
            fleet_trip_object = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'read',
                    [[hanhtrinh]],{'fields':['id','equipment_id', 'odometer_start','odometer_dest']})
            print('cap nhat file dinh kem')
            if attackements:
                # url = url + '&attachments={}'.format(attackements)
                for attachment in attackements:
                    id_trip = self.models.execute_kw(self.db, self.uid, self.password, 'ir.attachment', 'create', [{
                            'name': fleet_trip_object[0]['equipment_id'][1],
                            'type': 'url',
                            'url': attachment,
                            'res_model': 'fleet.trip',
                            'res_id': hanhtrinh,
                        }])
        
            print("Cap nhat so km ket thuc ")
        
            self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'write', [[hanhtrinh], {'odometer_dest': sokm}])
            # get record name after having changed it
            result =  self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'name_get', [[hanhtrinh]])
            print('result: ', result)
        except Exception as ex:
            print(ex)
        return result
        
    
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
    try:
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
            return {'data':{'results':[]}}
    except Exception as ex:
        return {'data':{'results':[]}}

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


def capnhatsokmbatdauhanhtrinh(hanhtrinh, sokm, body, attackements=None):
    # user = order.user
    url = f'https://vantaihahai.com/api/fleet.trip/{hanhtrinh}/do_odometer_start?odometer_start={sokm}'
    if attackements:
        url = url + '&attachments={}'.format(attackements)
    print("call: ",url)
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

def capnhatsokmketthuchanhtrinh(hanhtrinh, sokm, body, attackements=None):
    # user = order.user
    print('update: ',hanhtrinh)
    url = f'https://vantaihahai.com/api/fleet.trip/{hanhtrinh}/do_odometer_end?odometer_end={sokm}'
    if attackements:
        url = url + '&attachments={}'.format(attackements)
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


def tatcadiadiem():
    try:
       
        url = 'https://vantaihahai.com/api/fleet.location'
        access_token = settings.VANTAIHAHAI_CONFIG['access_token']
        headers = {
            # 'Content-Type': 'application/json',
            'access_token': f'{access_token}'
        }

        print("Lay tat ca dia diem cua xe: ")
    
        response = requests.request("GET", url, headers=headers)
        print(response)
        
        if response.status_code == 200:
            # order.haravan_order = response_json['order']['name']
            # order.save() 
            response_json =  response.json()
            return response_json
        else:
            return {'data':{'results':[]}}
    except Exception as ex:
        return {'data':{'results':[]}}


def tatcamathang():
    try:
       
        url = 'https://vantaihahai.com/api/fleet.product'
        access_token = settings.VANTAIHAHAI_CONFIG['access_token']
        headers = {
            # 'Content-Type': 'application/json',
            'access_token': f'{access_token}'
        }

        print("Lay tat ca dia diem cua xe: ")
    
        response = requests.request("GET", url, headers=headers)
        print(response)
        
        if response.status_code == 200:
            # order.haravan_order = response_json['order']['name']
            # order.save() 
            response_json =  response.json()
            return response_json
        else:
            return {'data':{'results':[]}}
    except Exception as ex:
        return {'data':{'results':[]}}