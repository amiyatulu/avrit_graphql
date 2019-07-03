from django.shortcuts import render
from django.http import HttpResponse

def deleteJWT(request):
    # print(request.COOKIES)
    response = HttpResponse("Cookies Deleted")
    response.delete_cookie("JWT", path="/")
    response.delete_cookie("sessionid", path="/")
    return response 