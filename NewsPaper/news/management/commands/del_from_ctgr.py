from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех публикаций в выбранной категории.'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь код, который выполнится при вызове вашей команды
        self.stdout.readable()
        category_list = []
        all_categories = Category.objects.all()
        for ctgr in all_categories:
            category_list.append(ctgr.name)
        self.stdout.write(f'Available categories: {category_list}')
        chosen_category = input('Type the name of category which posts to delete: ')
        confirmation = input(f'Do you really want to delete all posts in the category "{chosen_category}"? yes/no: ')
        if confirmation == 'yes':
            to_delete = Post.objects.filter(category__name=chosen_category)
            was_deleted = to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'{was_deleted[0]} posts in category "{chosen_category}" deleted.'))
            #return
        else:
            self.stdout.write(self.style.ERROR('Access denied'))
        return
