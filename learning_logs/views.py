from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """Stronaa główna adla apliikacji Learning Log."""
    return render(request, r'learning_logs\index.html')

def topics(request):
    """Wyświetlanie wszystkich tematów"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, r'learning_logs\topics.html', context)

def topic(request, topic_id):
    """Wyświetlanie pojedyńczego tematu razem z wpisami, które go dotyczą"""
    topic = Topic.objects.get(id=topic_id)
    entres =  topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entres}
    return render(request, r'learning_logs\topic.html', context)

def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST':
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # przekazano dane za pomocą żądania POST, należy je przetworzyć
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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

def edit_entry(request, entry_id):
    """Dodaj nowy wpis"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
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