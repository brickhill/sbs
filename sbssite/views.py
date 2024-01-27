from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages


def loginx(request):
    # messages.success(request, "Success")
    messages.error(request, 'Error')
    messages.debug(request, 'Debug')
    messages.info(request, 'Info')
    messages.warning(request, 'Warning')

    return redirect('/')
