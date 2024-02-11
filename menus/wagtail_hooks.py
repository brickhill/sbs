# import ModelAdmin
# import decorator
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Menu
# from wagtail.snippets import ModelAdmin, modeladmin_register


@modeladmin_register
class MenuAdmin(ModelAdmin):
    model = Menu
    menu_label = "Menus"
    menu_icon = "list_ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_Explorer = False
