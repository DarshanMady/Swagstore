from .models import Category

def menu_links(self):
    links = Category.objects.all()
    return dict(links=links)