from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    """Stronaa główna adla apliikacji Learning Log."""
    return render(request, r'learning_logs\index.html')

@login_required
def topics(request):
    """Wyświetlanie wszystkich tematów"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, r'learning_logs\topics.html', context)

@login_required
def topic(request, topic_id):
    """Wyświetlanie pojedyńczego tematu razem z wpisami, które go dotyczą"""
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if topic.owner != request.user:
        raise Http404
    entres =  topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entres}
    return render(request, r'learning_logs\topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Dodaj nowy wpis"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = EntryForm()
    else:
        # przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Dodaj nowy wpis"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = EntryForm(instance=entry)
    else:
        # przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            new_entry = form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
