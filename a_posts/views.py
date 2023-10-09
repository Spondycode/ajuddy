from django.shortcuts import render

def home_view(request):
    title = 'Welcome To The Pleasure Dome'
    context = {'title' :title}
    return render(request, 'a_posts/home.html', context)
