# NesPaper_Django_email-tasks

 Проект NewsPaper, новое в проекте: e-mail - с помощью send_mail и EmailMultiAlternatives (письма при регистрации пользователя,
 при новых постах и т.п.), периодические задачи Django-apscheduler (например о новых постах за истекший период в категориях из подписок пользователя).
 Осуществлено кэширование, как high-level(FileBasedCached как пример, template cache), иак и 
 low-level (key-value cache).
 В админ-панель добавлены удобные табличные представления моделей, поиск и фильтры (admin.ModelAdmin, list_display, list_filter, search_fields).
 
===========================================================================

Using email notifications by send_mail and  EmailMultiAlternatives.
Repated tasks triggered by signals - Django-apscheduler (pip install django-apscheduler reqired).
Particularly subscribers are receiving weekly email notifications wis list of new posts in the intrested categories with list of links.
Cache facility added: high-level(FileBasedCached, template cache) and low-level (key-value cache in views and models).

Admin-panel changed to show best model table views, search and filters added
(admin.ModelAdmin, list_display, list_filter, search_fields are used here).