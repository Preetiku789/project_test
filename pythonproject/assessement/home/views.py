from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import uuid

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.type = User.TYPE_CLIENT
        user.save()
        send_verification_email(user)
        return JsonResponse({'encrypted_url': generate_encrypted_url(user)})

def email_verify_view(request, token):
    user = User.objects.get(email_token=token)
    user.email_verified = True
    user.save()
    return HttpResponse('Email verified successfully')

def file_upload_view(request):
    if request.method == 'POST':
        if request.user.type == User.TYPE_OP:
            file = request.FILES['file']
            if file.name.endswith(('.pptx', '.docx', '.xlsx')):
                file_obj = File(uploaded_by=request.user, file=file)
                file_obj.save()
                return JsonResponse({'message': 'File uploaded successfully'})
            else:
                return JsonResponse({'error': 'Only pptx, docx, and xlsx files are allowed'}, status=400)
        else:
            return JsonResponse({'error': 'Only Ops users can upload files'}, status=403)

def file_list_view(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})

def file_download_view(request, pk):
    file = File.objects.get(pk=pk)
    if request.user.type == User.TYPE_CLIENT:
        encrypted_url = generate_encrypted_url(file)
        return JsonResponse({'encrypted_url': encrypted_url})
    else:
        return JsonResponse({'error': 'Only Client users can download files'}, status=403)

def generate_encrypted_url(file):
    
    # For demonstration purposes, I'm using a simple UUID
    encrypted_url = f'https://example.com/download/{uuid.uuid4()}'
    return encrypted_url

def send_verification_email(user):

    print(f'Verification email sent to {user.email}')