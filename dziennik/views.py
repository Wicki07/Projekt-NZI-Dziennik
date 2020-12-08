from django.shortcuts import render

def main(request):
    return render(request, 'main/main.html')

def singup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = UserCreationForm()
    return render(request, 'singup/singup.html')
