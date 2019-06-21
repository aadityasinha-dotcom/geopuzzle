from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.utils.translation import get_language, ugettext as _
from django.views.generic.list import BaseListView
from django_filters import FilterSet, ModelChoiceFilter, OrderingFilter, CharFilter

from common.views import ScrollListView
from maps.models import Tag
from puzzle.models import Puzzle
from users.models import User

ORDER = {
    'title_asc': {'title': _('Title ↓'), 'query': 'translations__name'},
    'title_desc': {'title': _('Title ↑'), 'query': '-translations__name'},
    'created_asc': {'title': _('Created ↓'), 'query': 'created'},
    'created_desc': {'title': _('Created ↑'), 'query': '-created'}
}

SUGGESTION = {
    'author': {'model': User, 'field': 'username'},
    'tag': {'model': Tag, 'field': 'name'}
}


class WorkshopView(TemplateView):
    template_name = 'puzzle/list.html'

    def get_context_data(self, **kwargs):
        context = super(WorkshopView, self).get_context_data(**kwargs)
        context.update({
            'count': Puzzle.objects.get_queryset().filter(user__isnull=False, is_published=True).count(),
            'language': get_language(),
            'order': [(key, value['title']) for key, value in ORDER.items()],
        })
        return context


class WorkshopFilter(FilterSet):
    search = CharFilter(field_name="translations__name", lookup_expr='icontains')
    author = ModelChoiceFilter(field_name="user", queryset=User.objects.all())
    tag = ModelChoiceFilter(field_name="tags__name", queryset=Tag.objects.all())
    order = OrderingFilter(fields=tuple((value['query'], key) for key, value in ORDER.items()))

    class Meta:
        model = Puzzle
        fields = ('author', 'tag', 'search')


class WorkshopItems(ScrollListView):
    model = Puzzle

    def get_queryset(self):
        qs = super(WorkshopItems, self).get_queryset().\
            filter(user__isnull=False, is_published=True).\
            prefetch_related('translations')
        return WorkshopFilter(self.request.GET, qs).qs


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = ('name',)


class TagView(BaseListView):
    model = Tag

    def get_queryset(self):
        return TagFilter(self.request.GET, super(TagView, self).get_queryset()).qs

    @staticmethod
    def convert_item(item):
        return {'value': str(item.id), 'label': item.name}

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse([self.convert_item(item) for item in context['object_list']], safe=False)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseBadRequest(status=401)

        instance, _ = Tag.objects.get_or_create(name=request.POST['name'][:50])
        return JsonResponse(self.convert_item(instance))


def suggest(request):
    for key in request.GET:
        value = request.GET.get(key)
        if value is not None:
            params = SUGGESTION[key]
            qs = params['model'].objects.filter(**{f'{params["field"]}__icontains': value}).values_list('id', params['field'])
            result = [{'value': str(item[0]), 'label': item[1]} for item in qs]
            return JsonResponse(result, safe=False)
    else:
        return HttpResponseBadRequest()
