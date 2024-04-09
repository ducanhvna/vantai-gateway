from django.conf import  settings
import requests, json
import xmlrpc.client
import datetime
class Apec():
    def __init__(self, url, db, username, password):
        print('init APEC')
        try:
            self.url = url
            self.db = db
            self.username = username
            self.password = password
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = common.authenticate(self.db, self.username, self.password, {})
        except Exception as ex:
            print("day la: ", ex)
            
    def getlistemployee(self):
        domain = ['&',('active', '=', True), ('user_id', '=', self.uid)]
        employees = self.models.execute_kw(self.db, self.uid,  self.password, 'hr.employee', 'search_read', [domain], 
        {'fields': ['id', 'name', 'user_id','employee_ho',
                        'company_id', 'code', 'department_id', 'time_keeping_code', 'job_title',
                        'probationary_contract_termination_date', 'severance_day', 'workingday',
                        'contract_ids',
                        'probationary_salary_rate', 'resource_calendar_id', 'date_sign', 'level']})
        return employees

    def getattendcereport(self, date_str == None, employee_code = None):
        LIMIT_SIZE = 10
        if not date_str:
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            
        if not employee_code:
            employees = self.getlistemployee()
            employee_code = employees[0]
            
        domain = [("employee_code", '=', employee_code)
                  ("date", "=", date_str)]
        
        ids = self.models.execute_kw(self.db, self.uid, self.password, 'hr.apec.attendance.report', 'search', [domain], {'offset': 0, 'limit': LIMIT_SIZE})
        list_scheduling_ver = self.models.execute_kw(self.db, self.uid, self.password, 'hr.apec.attendance.report', 'read', [ids],
                                                     {'fields': ['id', 'employee_name', 'date', 'shift_name', 'employee_code', 'company','additional_company',
                                                                 'shift_start', 'shift_end', 'rest_start', 'rest_end', 'rest_shift', 'probation_completion_wage',
                                                                 'total_shift_work_time', 'total_work_time', 'time_keeping_code', 'kid_time',
                                                                 'department', 'attendance_attempt_1', 'attendance_attempt_2',
                                                                 'attendance_attempt_3', 'attendance_attempt_4', 'attendance_attempt_5',
                                                                 'attendance_attempt_6', 'attendance_attempt_7', 'attendance_attempt_8',
                                                                 'attendance_attempt_9', 'attendance_attempt_10', 'attendance_attempt_11',
                                                                 'attendance_attempt_12', 'attendance_attempt_13', 'attendance_attempt_14',
                                                                 'attendance_inout_1','attendance_inout_2','attendance_inout_3',
                                                                 'attendance_inout_4','attendance_inout_5','attendance_inout_6',
                                                                 'attendance_inout_7','attendance_inout_8','attendance_inout_9',
                                                                 'attendance_inout_10','attendance_inout_11','attendance_inout_12', 
                                                                 'attendance_inout_13','attendance_inout_14','attendance_inout_15','actual_total_work_time', 'standard_working_day',
                                                                 'attendance_attempt_15', 'last_attendance_attempt', 'night_hours_normal', 'night_hours_holiday', 'probation_wage_rate', 
                                                                 'split_shift', 'missing_checkin_break', 'leave_early', 'attendance_late', 'night_shift', 'minute_worked_day_holiday', 
                                                                 'total_attendance']})
        return list_scheduling_ver
    
    
    
    def authenticate(self, username, password):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.db, username, password, {})
        return uid
    def GetListCompany(self):
        result = self.models.execute_kw(self.db, self.uid, self.password, 'res.users', 'read', 
                [[self.uid]], {'fields': ['id', 'company_ids']})
        company_ids = self.models.execute_kw(self.db, self.uid, self.password, 'res.company', 'name_get',
                [result[0]['company_ids']])
        return company_ids
       
    def tatcachuyendicuataixe(self, employee_id):
        results = []
        if employee_id>0:
            results = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'search_read', 
                [[('employee_id','=', employee_id)]], {'fields': ['id', 'company_id', "currency_id", "equipment_id", "location_name",
                        "location_dest_name", "location_id", "location_dest_id", 'eating_fee', 'note', 'odometer_start', 'odometer_dest',
                        'odometer_end', 'employee_id', 'schedule_date', 'start_date', 'end_date', 'attachment_ids']})
        return {'data':{'results': results}}
    
    def tatcachuyendihomnay(self):
        today_str = datetime.datetime.now().strftime('%Y-%m-%d') 
        last_week_str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') 
        results = self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'search_read', 
                [[('schedule_date','<=', today_str), ('schedule_date','>=', last_week_str)]], {'fields': ['id', 'company_id', "currency_id", "equipment_id", "location_name",
                        "location_dest_name", "location_id", "location_dest_id", 'eating_fee', 'note', 'odometer_start', 'odometer_dest',
                        'odometer_end', 'employee_id', 'schedule_date', 'start_date', 'end_date', 'attachment_ids']})
        for item in results:
            item['company_id'] ={'id':  item['company_id'][0] , 'name':item['company_id'][1]} \
                                    if item['company_id'] else None
            item['location_id'] ={'id':  item['location_id'][0], 'name':item['location_id'][1]} \
                                    if item['location_id'] else None
            item['location_dest_id'] ={'id':  item['location_dest_id'][0], 'name':item['location_dest_id'][1]} \
                                    if item['location_dest_id'] else None
            item['equipment_id'] = {'id': item['equipment_id'][0], 'name':item['equipment_id'][1]} \
                                    if item['equipment_id'] else None
            item['location_name'] = item['location_name'] if item['location_name'] else None
            item['schedule_date'] = item['schedule_date'] if item['schedule_date'] else None
            item['location_dest_name'] = item['location_dest_name'] if item['location_dest_name'] else None
            
            
        return {'data':{'results': results,'today':today_str}}
        
    def danhsachtatcaxe(self):
        result = self.models.execute_kw(self.db, self.uid, self.password, 'maintenance.equipment', 'search_read', 
                [[]], {'fields': ['id', 'name', "owner_user_id", "last_request", "license_plate",
                        "trip_count", "note", "message_ids"]})
        for item in result:
            try:
                item['owner_user_id'] = {'name':item['owner_user_id'][1], 'id':item['owner_user_id'][0]}
            except:
                print('item: ', item)
        return result

    def create_free_user(self, code):
        user_id= self.models.execute_kw(self.db, self.uid, self.password, 'res.users', 'create', [{'name':f"free{code}", 'login':f'free_{code}@free.com',
                'company_ids':[2], 'company_id':2, 'new_password':code}])
        
        return user_id

    def create_fist_car(self, member):
        update_data = {'name': member.name, "owner_user_id":member.member_id, "license_plate": member.name}
        car_id= self.models.execute_kw(self.db, self.uid, self.password, 'maintenance.equipment', 'create', [update_data])
        return car_id
    def create_employee(self, code, member_id):
        update_data = {
                'user_id': member_id,
                'name': code,
                'company_id': 2
            }
        id_employee = self.models.execute_kw(self.db, self.uid, self.password, 'hr.employee', 'create',
                                                  [update_data])
        return id_employee
    def chitietxe(self, xe_id):
     # user = order.user
        [result] = self.models.execute_kw(self.db, self.uid, self.password, 'maintenance.equipment', 'read',
                [xe_id],{'fields':['id', 'name', "owner_user_id", "last_request", "license_plate",
                        "trip_count", "note", "message_ids"]})
        try:
            result['owner_user_id'] = {'name':result['owner_user_id'][1], 'id':result['owner_user_id'][0]}
        except:
            print('item: ', result)
        print(result)
        return result
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
            try:
                body['ward_id'] = location_start['ward_id'][0]
                body['district_id'] = location_start['district_id'][0]
                body['state_id'] = location_start['state_id'][0]
            except Exception as ex:
                print('start errr', ex)
        if location_dest != None:
            try:
                body['ward_dest_id'] = location_dest['ward_id'][0]
                body['district_dest_id'] = location_dest['district_id'][0]
                body['state_dest_id'] = location_dest['state_id'][0]
            except Exception as ex:
                print('des errr', ex)
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
    def capnhatsokmbatdauhanhtrinh(self, hanhtrinh, sokm, body, attackements=None):
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
        
            self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'write', [[hanhtrinh], {'odometer_start': sokm}])
            # get record name after having changed it
            result =  self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'name_get', [[hanhtrinh]])
            print('result: ', result)
        except Exception as ex:
            print(ex)
        return result
    def capnhatlocationbatdauhanhtrinh(self, hanhtrinh, location_id):
        result = None
        try:
            self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'write', [[hanhtrinh], {'location_id': location_id}])
            # get record name after having changed it
            result =  self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'name_get', [[hanhtrinh]])
            print('result: ', result)
        except Exception as ex:
            print(ex)
        return result
    def capnhatlocationketthuchanhtrinh(self, hanhtrinh, location_id):
        result = None
        try:
            self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'write', [[hanhtrinh], {'location_id': location_id}])
            # get record name after having changed it
            result =  self.models.execute_kw(self.db, self.uid, self.password, 'fleet.trip', 'name_get', [[hanhtrinh]])
            print('result: ', result)
        except Exception as ex:
            print(ex)
        return result
        
        