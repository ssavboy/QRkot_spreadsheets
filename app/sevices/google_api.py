from copy import deepcopy
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_LEN = 100
COLUMN_LEN = 11
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/{spreadsheets_id}'
TABLE_VALUES = [
    ['Отчет от', '{date}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от {date}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_LEN,
            columnCount=COLUMN_LEN,
        )
    ))]
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'].format(now_date_time)
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
    copy_table = deepcopy(TABLE_VALUES)
    table_values = [
        *copy_table[0][1].format(now_date_time),
        *[list(map(str, (
            project['name'],
            timedelta(project['_no_label']),
            project['description']
        ))) for project in closed_projects]
    ]
    row_len = len(table_values)
    column_len = len(max(table_values, key=len))
    if row_len > ROW_LEN:
        raise ValueError(
            f'Максимальная допустимое значение {ROW_LEN}, передано {row_len}'
        )
    if column_len > COLUMN_LEN:
        raise ValueError(
            f'Максимальная допустимое значение {COLUMN_LEN}, '
            f'передано {column_len}'
        )
    await wrapper_services.as_service_account(
        sheets_service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_len}C{column_len}',
            valueInputOption='USER_ENTERED',
            json={'majorDimension': 'ROWS', 'values': table_values},
        )
    )
    return SPREADSHEET_URL.format(spreadsheet_id)
