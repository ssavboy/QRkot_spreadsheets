from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
REPORT_ROW_COUNT = 100
REPORT_COLUMN_COUNT = 3
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/%s'
SPREADSHEET_BODY = {
    'properties': {
        'title': 'QRKot. Отчет от %s',
        'locale': 'ru_RU',
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': REPORT_ROW_COUNT,
                    'columnCount': REPORT_COLUMN_COUNT,
                },
            }
        }
    ],
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] %= now_date_time
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str, closed_projects: list, wrapper_services: Aiogoogle
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    sheets_service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    for project_and_completion_rate in closed_projects:
        project, completion_rate = project_and_completion_rate
        completion_rate = timedelta(seconds=completion_rate)
        new_row = [
            project.name,
            str(completion_rate),
            project.description,
        ]
        table_values.append(new_row)

    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        sheets_service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
    return SPREADSHEET_URL % spreadsheet_id
