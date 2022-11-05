from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post, Category, Profile, Like
from .forms import CommentForm, CreatePostForm, CreateUserForm, ProfileForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.decorators import login_required


def PostHome(request):
    # Categories
    category = request.GET.get('category')
    if category is None:
        posts = Post.objects.all()  # .order_by('?')  order random
    else:
        posts = Post.objects.filter(category__name=category)

    categories = Category.objects.annotate(total_post=Count('post'))

    # Paginator
    p = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = 'a' * posts.paginator.num_pages
    context = {'posts': posts, "category_list": category, 'categories': categories, 'nums': nums}
    return render(request, 'home.html', context)




def Details(request, slug):
    # Comment Function
    post = Post.objects.get(slug=slug)
    if post:
        post.post_views = post.post_views + 1
        post.save()

    # comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.user = request.user
            obj.save()
            return redirect('details', slug=post.slug)
    else:
        form = CommentForm()
    
    #  Likes Function
    result = ''

    if request.method == 'POST':
        id = int(request.POST.get('post_id'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            post.save()

    return render(request, 'details.html', {'post': post, 'result': result, 'form': form})

@login_required(login_url='login')
def CreatePost(request):
    form = CreatePostForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('home')

    return render(request, 'new_post.html', {'form': form})


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Username or Password is incorrect')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


# user register

def UserRegister(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = user.profile
            profile.bio = request.POST['bio']
            profile.profile_image = request.FILES['profile_image']
            profile.username = request.POST['username']
            profile.email = request.POST['email']
            profile.first_name = request.POST['first_name']
            profile.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect('login')
    else:
        user_form = CreateUserForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='login')
def UpdateProfile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile', pk=user.id)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile-update.html', {'user_form': user_form, 'profile_form': profile_form})


def Query(request):
    search = request.GET.get('search')
    result = []
    error = None

    if len(search) < 3:
        error = 'Your Query its to short'
    else:
        result = Post.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search) |
            Q(category__name__icontains=search) |
            Q(comments__body=search)
        )
    return render(request, 'search.html', {
        'results': result,
        'search': search,
        'error': error
    })


def UserProfile(request, pk):
    profile = get_object_or_404(User, id=pk)
    return render(request, 'profile.html', {'profile': profile})
