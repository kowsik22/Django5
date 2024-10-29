from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailAuthenticationForm  # Import your custom form

class CustomLoginView(View):
    def get(self, request):
        form = EmailAuthenticationForm()
        return render(request, 'your_template.html', {'form': form})  # Specify your template here

    def post(self, request):
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('your_redirect_url')  # Redirect after successful login
        return render(request, 'your_template.html', {'form': form})  # Render the form with errors
