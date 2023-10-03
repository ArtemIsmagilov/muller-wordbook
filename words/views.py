# Create your views here.
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, FormView
from .models import Fav, Word
from owner import *
from .forms import *
from .words_scripts.lingvo import get_data, parse_json
from .words_scripts.translate import run_translate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'words/contact.html'
    success_url = reverse_lazy('words:all')

    def form_valid(self, form):
        return redirect('words:all')


class WordListView(OwnerListView):
    model = Word
    template_name = 'words/word_list.html'

    def get(self, request, *args, **kwargs):
        word_list = Word.objects.all()
        favorites = []

        paginator = Paginator(word_list, 50)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if request.user.is_authenticated:
            rows = request.user.favorite_words.values('id')
            favorites = [row['id'] for row in rows]

        form = ListForm()
        ctx = {
            'form': form,
            "page_obj": page_obj,
            'favorites': favorites
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        word_list = list()
        favorites = list()
        form = ListForm(request.POST)
        if form.is_valid() and request.POST:
            data = form.cleaned_data
            count = data.get('count')
            strval = data.get('search')
            exact = data.get('exact')
            if request.user.is_authenticated:
                rows = request.user.favorite_words.values('id')
                favorites = [row['id'] for row in rows]
            filter_arg = {'eng__startswith': strval} if not exact else {'eng__exact': strval}
            if strval and count.isdigit():
                word_list = Word.objects.filter(**filter_arg)[:int(count)]
            elif strval:
                word_list = Word.objects.filter(**filter_arg)
            ctx = {
                'word_list': word_list,
                'favorites': favorites,
                'search': strval, 'form': form
            }
            return render(request, self.template_name, ctx)


class WordTranslateView(OwnerDetailView):
    template_name = 'words/word_translate.html'
    success_url = reverse_lazy('words:word_translate')

    def get(self, request, *args, **kwargs):
        form = TranslateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        translate_word = run_translate(
            request.POST['from_translate'], request.POST['from_lang'], request.POST['to_lang']
        )
        form = TranslateForm(request.POST, initial={"to_translate": translate_word})
        if form.is_valid():
            ctx = {'form': form, 'translate_word': translate_word}
            return render(request, self.template_name, ctx)


class WordDetailView(OwnerDetailView):
    model = Word
    template_name = 'words/word_detail.html'

    def get(self, request, pk, *args, **kwargs):
        word = Word.objects.get(id=pk)
        ctx = {'word': word}
        try:
            data = parse_json(get_data(word=word.eng))
        except TypeError as type_er:
            print(type_er)
            data = {}
        ctx.update(data)
        return render(request, self.template_name, ctx)


class WordFavView(OwnerListView):
    model = Word
    template_name = 'words/word_fav.html'

    def get(self, request, *args, **kwargs):
        favorites = []
        if request.user.is_authenticated:
            rows = request.user.favorite_words.values('id')
            favorites = [r['id'] for r in rows]
        word_list = [Word.objects.get(pk=pk) for pk in favorites]
        ctx = {'word_list': word_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        print("Add PK", pk)
        word = get_object_or_404(Word, id=pk)
        fav = Fav(user=request.user, word=word)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        print("Delete PK", pk)
        word = get_object_or_404(Word, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, word=word).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
