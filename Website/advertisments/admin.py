from django.contrib import admin

from .models import Category ,Ad , Review , sub_category , Profile ,Location , Contact

class AdAdmin(admin.ModelAdmin):
    list_display = ('owner','ad_title','ad_brand','ad_model',)
    list_filter = ('ad_cat' , 'owner',)
    list_per_page = 20


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name','Phone',)
    list_filter = ( 'user_name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'location','city','state',)
    list_filter = ( 'user_name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_of_ad' , 'name_of_customer' ,'subject',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ( 'user' , 'subject')


admin.site.register(Location , LocationAdmin)
admin.site.register(Profile , ProfileAdmin)
admin.site.register(Category)
admin.site.register(sub_category)
admin.site.register(Ad , AdAdmin)
admin.site.register(Review , ReviewAdmin)
admin.site.register(Contact , ContactAdmin)



