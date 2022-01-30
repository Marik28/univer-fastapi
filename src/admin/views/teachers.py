from .base import BaseModelView


class TeachersView(BaseModelView):
    # columns
    form_excluded_columns = ["lessons"]
    column_list = ["second_name", "first_name", "middle_name"]
    column_details_list = ["second_name", "first_name", "middle_name"]

    # customization
    column_default_sort = "second_name"
    column_searchable_list = ["second_name", "first_name", "middle_name"]
