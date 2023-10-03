from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """


class OwnwerCreateView(CreateView):
    """
    Sub-class the DetailView to pass the request to the form.
    """
