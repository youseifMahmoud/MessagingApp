from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q  
from .models import Message
from .forms import SignUpForm

def home(request):
    return render(request, 'users/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('communicating_with_others')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def chat_with_user(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | 
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
    
    return render(request, 'users/chat.html', {'receiver': receiver, 'messages': messages})

@login_required
def communicating_with_others(request):
    search_query = request.POST.get('search', '')  # Get the search query from the form

    # Filter users excluding the logged-in user and applying the search query
    users = User.objects.exclude(id=request.user.id)
    
    if search_query:
        users = users.filter(Q(username__icontains=search_query))  # Case-insensitive search
    
    receiver_id = request.POST.get('receiver_id', '')  # Maintain the receiver ID across submissions
    messages = []

    if receiver_id:  # Check if there's a receiver selected
        receiver = get_object_or_404(User, id=receiver_id)  # Ensure the receiver exists

        # Fetch messages for the selected conversation between the logged-in user and the receiver
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | 
            Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')  # Assuming you have a timestamp field in your Message model

    # Handle message sending logic
    if request.method == 'POST' and 'content' in request.POST and receiver_id:
        content = request.POST['content'].strip()
        
        if content:  # Ensure the content is not empty
            Message.objects.create(sender=request.user, receiver=receiver, content=content)

    return render(request, 'users/communicating_with_others.html', {
        'users': users,
        'messages': messages,
        'search_query': search_query,
        'receiver_id': receiver_id  # Pass the receiver_id to the template to maintain the conversation
    })
