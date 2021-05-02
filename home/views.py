from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from home.models import Post
from django.contrib import messages 
from django.contrib.auth.models import User 
from blog.models import Post
from django.contrib.auth  import authenticate,  login, logout
def home(request): 
    return render(request, "home/home.htm")

def contact(request):
    if request.method=="POST":
        title=request.POST['title']
        author=request.POST['author']
        slug=request.POST['slug']
        content =request.POST['content']
        summary =request.POST['summary']
        if len(title)<1 or len(author)<1 or len(slug)<1 or len(content)<4 or len(summary)<1:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Post(title=title, author=author, slug=slug, content=content,summary=summary)
            contact.save()
            messages.success(request, "Your Blog has been created!!")
    return render(request, "home/contact.htm")

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.htm', params)

from django.shortcuts import redirect

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def about(request): 
    return render(request, "home/about.htm")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


def about(request): 
    return render(request, "home/about.htm")