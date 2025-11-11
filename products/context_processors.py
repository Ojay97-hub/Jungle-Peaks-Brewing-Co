from .models import Category


def categories(request):
    """
    Context processor to make all categories available globally.
    """
    return {
        'all_categories': Category.objects.all().order_by('name'),
    }

