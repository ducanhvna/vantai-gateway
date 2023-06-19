url = 'https://vantaihahai.com'
# db = 'hoaanhimport'
db = 'fleet'
# username = 'tuyetciec@gmail.com'
password = 'admin'
# password = 'admin'
username = 'admin'

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid = common.authenticate(db, username, password, {})
department_ids = models.execute_kw(db, uid, password, 'hr.department','search', [[]])
location_ids = models.execute_kw(db, uid, password, 'fleet.location','search', [[]])
list_locations = models.execute_kw(db, uid, password, 'fleet.location', 'read',[location_ids],{'fields':['id','ward_id', 'district_id']})