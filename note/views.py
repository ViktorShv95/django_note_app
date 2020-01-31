from django.shortcuts import render, get_object_or_404
from .models import Note
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm, RegisterUserForm, NoteForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.template.loader import render_to_string


class NoteAppLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = 'notes/'

    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = 'notes/'
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid

class NoteAppLogout(LogoutView):
    next_page = 'notes/'

def note_list(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user).order_by('-created_at')
    else:
        notes = Note.objects.all()
    context = {
        'notes': notes,
    }
    return render(request, 'note_list.html', context)

def save_all(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form_com = form.save(commit=False)
            form_com.author = request.user
            form_com.save()
            data['form_is_valid'] = True
            notes = Note.objects.filter(author=request.user)
            data['note_list'] = render_to_string('note_list2.html', {'notes': notes})
        else:
            data['form_is_valid'] = False
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
    else:
        form = NoteForm()
    return save_all(request, form, 'note_create.html')
#
def update_note(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
    else:
        form = NoteForm(instance=note)
    return save_all(request, form, 'note_update.html')

def delete_note(request,id):
    data = dict()
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        note.delete()
        data['form_is_valid'] = True
        notes = Note.objects.filter(author=request.user)
        data['note_list'] = render_to_string('note_list2.html', {'notes': notes})
    else:
        context = {'note': note}
        data['html_form'] = render_to_string('note_delete.html', context, request=request)

    return JsonResponse(data)

def share_page(request, link_id):
    note = Note.objects.filter(link_id=link_id)
    context = {
        'note': note,
    }
    return render(request, 'about.html', context)
