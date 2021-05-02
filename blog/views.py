from django.shortcuts import render, HttpResponse
from blog.models import Post

def blogHome(request):
   allPosts= Post.objects.all()
   context={'allPosts': allPosts}
   return render(request, "blog/blogHome.htm", context)
   
    #return HttpResponse('Welcome to our bloghome here')

def blogPost(request, slug):
    post=Post.objects.filter(slug=slug).first()
    context={"post":post}
    return render(request, 'blog/blogPost.htm',context)



   