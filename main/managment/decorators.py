from django.shortcuts import render ,redirect ,HttpResponse



def unauth_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('managment_home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return render(request,"not_authorised.html")

        return wrapper_func
    return decorator
        
    