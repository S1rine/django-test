from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
  """The home page for Learning Log."""
  return render(request, 'learning_logs/index.html')


def topics(request):
  """Show all topics."""
  topics_list = Topic.objects.order_by('date_added')
  context = {'topics': topics_list}
  return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
  """Show a single topic and all its entries."""
  topic_item = Topic.objects.get(id=topic_id)
  entries = topic_item.entry_set.order_by('-date_added')
  context = {'topic': topic_item, 'entries': entries}
  return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
  """Add a new topic."""
  if request.method != 'POST':
    # No data submitted; create a blank form.
    form = TopicForm()
  else:
    # POST data submitted; process data.
    form = TopicForm(data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('learning_logs:topics')

  # Display a blank or invalid form.
  context = {'form': form}
  return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
  """Add a new entry for a particular topic."""
  topic_item = Topic.objects.get(id=topic_id)

  if request.method != 'POST':
    # No data submitted; create a blank form.
    form = EntryForm()
  else:
    # POST data submitted; process data.
    form = EntryForm(data=request.POST)
    if form.is_valid():
      new_entry_item = form.save(commit=False)
      new_entry_item.topic = topic_item
      new_entry_item.save()
      return redirect('learning_logs:topic', topic_id=topic_id)

  # Display a blank or invalid form:
  context = {'topic': topic_item, 'form': form}
  return render(request, 'learning_logs/new_entry.html', context)
