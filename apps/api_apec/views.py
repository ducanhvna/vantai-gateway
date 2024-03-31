from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
class SyncUserDevice(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        results = []
        # target_users = User.objects.filter(username=username, password=password)
        target_user = User.objects.get(username=username) 
        # this checks the plaintext password against the stored hash 
        correct = target_user.check_password(password) 
        if correct:
            # target_user= target_users[0]
            current_devices = Device.objects.filter(user=self.request.user)
            for device in current_devices:
    
            # serializer.save(user= user, name=code)
            # user_profile = UserProfile(user_id=user.id,
            #                            affiliate_code=''.join(
            #                                random.choices(string.ascii_uppercase + string.digits, k=8)))
            # user_profile.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
                device.user_owner = target_user
                device.save()
            # if len(current_devices) == 0:
            #     result = {'devices': len(current_devices), 'username': target_user.username}
            # else:
                result_item = {'device_id': device.id,'device_name': device.name, 
                        'owner': device.user_owner.username if device.user_owner else None, 
                        'username': device.user.username if device.user else None}
                results.append(result_item)
            # return Response(device)
        # else:
        #     result = {'result': None}
        # id = request.data.get('id')
        # type = request.data.get('type')
        
        return Response({'data': results})
        
