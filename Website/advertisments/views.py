from django.shortcuts import render , HttpResponse , redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm , EditProfile , ChangePassword , UserPicture , LocationForm , AdForm , ReviewForm , ContactForm
from datetime import datetime
from .models import Ad, Profile, Category,  Location , sub_category , Review , Contact
from .templatetags import extras
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def index(request):
    all_ads = Ad.objects.all().order_by('post_date').filter(ad_status=True)
    cat = Category.objects.all()
    print(cat , all_ads)
    return render(request,'advertisments/index.html' , {'Ads': all_ads , 'cat':cat})


def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            messages.success(request , "{}, Your account has been created. Now you can Login".format(username))
            user.save()
            return redirect('/login')
    else:
        form = RegistrationForm()
    return render(request,'advertisments/register.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect("/user_profile")
        else:
            print("Not  logged in")
            messages.info(request, ' You have entered wrong Username or Password!')
            return render(request, 'advertisments/login.html')
    else:
        form = AuthenticationForm()
    return render(request, 'advertisments/login.html',{'form':form})


def user_profile(request):

    if request.method == 'POST':
        form = EditProfile(request.POST , instance= request.user)
        if form.is_valid():
            form.save()
            messages.success(request ,"Profile Updated")
            return redirect('/user_profile')
    else:
        form = EditProfile(instance= request.user)
    return render(request , 'advertisments/user_profile.html' , {'form' : form})


def user_profile2(request):
    if request.method == 'POST':
        print("Post")
        form = UserPicture(request.POST , request.FILES)
        if form.is_valid():
            pic = form.save(commit=False)
            pic.user_name = request.user
            pic.save()
            messages.success(request, "Your Profile Picture is updated")
            return redirect('/user_profile')
        else:
            messages.error("You have not entered a correct Phone No.")
    else:
        form = UserPicture()
    return render(request,'advertisments/user_profile2.html',{'form':form})


def update_profile_pic(request , id):
    if request.method == 'POST':
        profile = Profile.objects.get(id=id)
        print(profile)
        form = UserPicture(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_name = request.user
            profile.save()
            messages.success(request, "Your Profile Picture is updated")
            return redirect('/user_profile')
        else:
            messages.error(request , "Please, enter Correct Phone No")
    else:
        form = UserPicture()
    return render(request,'advertisments/user_profile2.html',{'form':form})


def location_update(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.user_name = request.user
            loc.save()
            messages.success(request, "Your Location is updated")
            return redirect('/user_profile')
        else:
            print(form.is_valid())
            print(form.errors)
    else:
        form = LocationForm()
    return render(request,'advertisments/location_update.html',{'form':form})


def location_update_again(request , id):
    if request.method == 'POST':
        loc = Location.objects.get(pk=id)
        form = LocationForm(request.POST or None, instance=loc)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.user_name = request.user
            loc.save()
            messages.success(request, "Your Location is updated")
            return redirect('/user_profile')
        else:
            print(form.is_valid())
            print(form.errors)
    else:
        form = LocationForm()
    return render(request, 'advertisments/location_update.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(data = request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request , form.user)
            messages.success(request, "Password Changed")
            return redirect('/user_profile')
        else:
            return render(request, 'advertisments/change_password.html')
    else:
        form = ChangePassword(user = request.user)
        return render(request, 'advertisments/change_password.html', {'form': form})


def about_us(request):
    return render(request,'advertisments/about_us.html')


def ad_listing(request):
    if request.method == 'POST':
        print("Post")
        form = AdForm(request.POST , request.FILES )
        if form.is_valid():
            print("save")
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.post_date = datetime.now()
            ad.save()
            messages.success(request, "Ad posted successfully!!")
            return redirect('/')
        else:
            print(form.is_valid())
            messages.info(request, ' Please Enter Valid Details!!')
            print(form.errors)
            return render(request, 'advertisments/ad_listing.html', {'form': form})
    else:
        form = AdForm()
    return render(request, 'advertisments/ad_listing.html', {'form': form})


@login_required(login_url="/login/")
def my_ads(request):
    user_posts = Ad.objects.order_by('-post_date').filter(owner=request.user)
    # loc = Location.objects.filter(user_name = request.user)
    context = {
        'user_posts': user_posts
              }
    print(context)
    return render(request, 'advertisments/my_ads.html', context)


@login_required(login_url="/login/")
def update(request , id):
   product = Ad.objects.get(pk = id)
   print(product)
   form = AdForm(request.POST or None, request.FILES or None , instance=product )
   if form.is_valid():
       product.post_date = datetime.now()
       product.save()
       return redirect('/my_ads')
   return render(request, 'advertisments/ad_listing.html' , {'form': form ,'product':product})

@login_required(login_url='/login/')
def pending_ads(request):
    user_posts = Ad.objects.order_by('-post_date').filter(owner=request.user, ad_status = False)
    context = {
        'user_posts': user_posts,
    }
    print(context)
    return render(request, 'advertisments/pending_ads.html', context)

def details(request , pk):
    post = get_object_or_404(Ad, pk=pk)
    try:
        pro = Profile.objects.get(user_name=post.owner)
    except Exception as e:
        pro = None
    reviews = Review.objects.filter(review_of_ad=pk)
    reviews = Review.objects.filter(review_of_ad=pk, review_parent=None)
    replies = Review.objects.order_by('post_date_review').filter(review_of_ad=pk).exclude(review_parent=None)
    replydict = {}
    for reply in replies:
        if reply.review_parent.id not in replydict.keys():
            replydict[reply.review_parent.id] = [reply]
        else:
            replydict[reply.review_parent.id].append(reply)
    print(replydict)
    form = ReviewForm(request.POST or None)
    return render(request , 'advertisments/details.html',{'post' : post , 'pro':pro, 'reviews':reviews
                 , 'form':form , 'replydict':replydict} )


def delete(request , id):
    product = Ad.objects.get(id = id)
    if request.method == 'POST':
        product.delete()
        return redirect('/my_ads')
    return render(request , 'advertisments/delete.html',{'product':product})


def ad_details(request , pk):
    post = get_object_or_404(Ad , pk = pk)
    try:
        pro = Profile.objects.filter(user_name=post.owner)
    except Exception as e:
        pro = None
    cat = Category.objects.all()
    reviews = Review.objects.filter(review_of_ad=pk, review_parent=None)
    replies = Review.objects.order_by('post_date_review').filter(review_of_ad=pk).exclude(review_parent=None)
    replydict = {}
    for reply in replies:
        if reply.review_parent.id not in replydict.keys():
            replydict[reply.review_parent.id] =[reply]
        else:
            replydict[reply.review_parent.id].append(reply)
    print(replydict)
    form = ReviewForm(request.POST or None)
    return render(request , 'advertisments/ad_details.html',{'post':post, 'pro':pro[0] ,'form': form,
        'reviews' : reviews , 'replydict':replydict , 'cat': cat })


def store(request , id):
    sub = sub_category.objects.filter(category_name_id = id)
    return render(request, 'advertisments/store.html' , {'sub':sub , 'c':sub[0]})


def ad_list_view(request , id):
    ad_list = Ad.objects.all().order_by('-post_date').filter(ad_subcat_id = id , ad_status = True)
    cate = Category.objects.all()
    # print(ad_list)
    if len(ad_list)!=0:
        cat = ad_list[0].ad_cat
        subcat = ad_list[0].ad_subcat
        context = {
            'ad_list': ad_list,
            'cat': cat,
            'subcat': subcat,
            'cate': cate,
        }
        return render(request , 'advertisments/ad_list_view.html' , context)
    else:
        context = {
            'cate': cate,
        }
        return render(request, 'advertisments/ad_list_view.html', context)


def terms_condition(request):
    return render(request,"advertisments/terms_condition.html")


def category(request):
    all_ads = Paginator(Ad.objects.all().order_by('-post_date').filter(ad_status = True) , 8)
    page = request.GET.get('page')
    try:
        ads = all_ads.page(page)
    except PageNotAnInteger :
        ads = all_ads.page(1)
    except EmptyPage:
        ads = all_ads.page(all_ads.num_pages)
    cat = Category.objects.all()
    loc = Location.objects.all()
    print( all_ads )
    return render(request, 'advertisments/category.html', {'Ads': ads, 'cat' : cat, 'loc': loc})

def search(request):
    ad_list = Ad.objects.order_by('post_date')
    cate = Category.objects.all()
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            ad_list = ad_list.filter(ad_title__icontains=title)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            ad_list = ad_list.filter(ad_cat__category_name__icontains=category)
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            ad_list = ad_list.filter(Q(ad_city__icontains=location) | Q(ad_state__icontains=location) | Q(ad_location__icontains = location))
    context = {
        'cate': cate,
        'ad_list': ad_list,
    }
    return render(request, 'advertisments/search.html', context)

def review(request , id):
    if request.method == 'POST':
        print("Post")
        form = ReviewForm(request.POST or None)
        product = Ad.objects.get(id = id)
        if form.is_valid():
            print("save")
            data = form.save(commit=False)
            data.name_of_customer = request.user
            data.post_date_review = datetime.now()
            data.review_of_ad = product
            if request.POST.get('r_id') != None:
                r = Review.objects.get(id = request.POST.get("r_id"))
                data.review_parent = r
                data.save()
                messages.success(request, "Reply posted successfully!!")
                return redirect('advertisements:ad_details',id)
            else:
                data.save()
                messages.success(request, "Review posted successfully!!")
                return redirect('advertisements:ad_details', id)

        else:
            messages.info(request, ' Please Enter Valid Details!!')
            print(form.errors)
            return render(request, 'advertisments/ad_details.html', {'form': form , 'id': id})
    else:
        form = ReviewForm()
    return render(request, 'advertisments/ad_details.html', {'form': form , 'id': id})

@login_required(login_url='/login/')
def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("save")
            contact = form.save(commit=False)
            contact.user = request.user
            contact.post_date_contact = datetime.now()
            contact.save()
            messages.success(request, "Message Sent Successfully!!")
            return redirect('/contact_us')
    else:
        form = ContactForm()
    return render(request, 'advertisments/contact_us.html', {'form': form})

def reply_contact(request):
    con_reply = Contact.objects.order_by('-post_date_contact').filter(user=request.user)
    print(con_reply)
    return render(request , 'advertisments/reply_contact.html' , {'con_reply':con_reply} )

def ad_list(request):
    all_ads = Paginator(Ad.objects.all().order_by('-post_date').filter(ad_status=True), 8)
    page = request.GET.get('page')
    try:
        ads = all_ads.page(page)
    except PageNotAnInteger:
        ads = all_ads.page(1)
    except EmptyPage:
        ads = all_ads.page(all_ads.num_pages)
    cat = Category.objects.all()
    loc = Location.objects.all()
    print(all_ads)
    return render(request, 'advertisments/ad_list.html', {'Ads': ads, 'cat': cat, 'loc': loc})

def outbox(request):
    message = Paginator(Review.objects.filter(Q(name_of_customer = request.user) & Q(review_parent = None)) , 6)
    page = request.GET.get('page')
    try:
        message = message.page(page)
    except PageNotAnInteger:
        message = message.page(1)
    except EmptyPage:
        message = message.page(message.num_pages)
    return render(request , 'advertisments/outbox.html' , {'message' : message })


def delete_user(request):
    user = User.objects.get(username = request.user )
    user.delete()
    form = RegistrationForm
    return render(request , 'advertisments/register.html' , {'form' : form})

