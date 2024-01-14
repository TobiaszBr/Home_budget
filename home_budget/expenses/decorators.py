from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


swagger_decorator_expense = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "id",
            in_=openapi.IN_PATH,
            description="Expense's unique id number",
            type=openapi.TYPE_INTEGER,
        )
    ])

swagger_decorator_report = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "id",
            in_=openapi.IN_PATH,
            description="Report's unique id number",
            type=openapi.TYPE_INTEGER,
        )
    ])

swagger_decorator_show_report_annual = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "year",
            in_=openapi.IN_PATH,
            description="Report's year",
            type=openapi.TYPE_INTEGER,
        ),
     ]
)

swagger_decorator_show_report_monthly = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "year",
            in_=openapi.IN_PATH,
            description="Report's year",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "month",
            in_=openapi.IN_PATH,
            description="Report's month",
            type=openapi.TYPE_INTEGER,
        ),
     ]
)


def get_swagger_parameters_expense_list() -> dict[str, list[openapi.Parameter]]:
    swagger_parameters_dict = {
        "category": "Expense's category",
        "subcategory": "Expense's subcategory",
        "amount": "Expense's amount",
        "date": "Expense's date in YYYY-MM-DD format",
        "description": "Expense's description"
    }
    manual_parameters_list = []
    for parameter_name, description in swagger_parameters_dict.items():
        if parameter_name != "id":
            field_type = openapi.TYPE_STRING
        else:
            field_type = openapi.TYPE_INTEGER

        parameter = openapi.Parameter(
            parameter_name,
            in_=openapi.IN_QUERY,
            description=f"{description}",
            type=field_type,
        )

        manual_parameters_list.append(parameter)

    swagger_auto_schema_params_dict = {"manual_parameters": manual_parameters_list}

    return swagger_auto_schema_params_dict


def get_swagger_parameters_report_list() -> dict[str, list[openapi.Parameter]]:
    swagger_parameters_dict = {
        "year": "Report's year",
        "month": "Report's month"
    }
    manual_parameters_list = []
    for parameter_name, description in swagger_parameters_dict.items():
        field_type = openapi.TYPE_STRING

        parameter = openapi.Parameter(
            parameter_name,
            in_=openapi.IN_QUERY,
            description=f"{description}",
            type=field_type,
        )

        manual_parameters_list.append(parameter)

    swagger_auto_schema_params_dict = {"manual_parameters": manual_parameters_list}

    return swagger_auto_schema_params_dict


swagger_decorator_expense_list = swagger_auto_schema(
    **get_swagger_parameters_expense_list()
)
swagger_decorator_report_list = swagger_auto_schema(
    **get_swagger_parameters_report_list()
)
