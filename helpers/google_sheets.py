import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SCOPE, CREDS_PATH, SHEET
from helpers.error_handler import handle_api_error, send_log_message

# Setup Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
client = gspread.authorize(creds)


@handle_api_error
async def get_high_priority_support_units(sheet, bot):
    worksheet = sheet.worksheet("High Priority Support Units for CB")
    columns = ["B", "D", "F"]
    zero_set_names = []

    for col in columns:
        col_index = ord(col) - ord("A") + 1
        col_values = worksheet.col_values(col_index)

        for row_index, cell_value in enumerate(col_values):
            cell_value_cleaned = cell_value.strip().lower()

            if "0 set" in cell_value_cleaned:
                if row_index > 0:
                    name = col_values[row_index - 1].strip()
                    if name:
                        zero_set_names.append(name)

    zero_set_names = list(filter(None, zero_set_names))
    return zero_set_names


# Function to get the Google Sheets client
def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET)  # Ensure this returns a Spreadsheet object


# Function to store emote usage statistics in Google Sheets
@handle_api_error
async def store_emote_usage_statistics(emote_usage, bot):
    emotes_sheet = client.open(SHEET).worksheet("Emotes")
    emote_data = [["Emote", "Usage Count"]]
    for emote, count in emote_usage.items():
        emote_data.append([emote, count])
    emotes_sheet.clear()
    emotes_sheet.update("A1", emote_data)
    await send_log_message(
        bot, "Emote Usage Statistics", "Emote statistics have been updated."
    )


# Helper function to get the current month's sheet
@handle_api_error
async def get_current_month_sheet(bot):
    now = datetime.datetime.now()
    month_name = now.strftime("%B")
    start_cb_number = 71
    current_month = now.month
    cb_number = start_cb_number + (current_month - 1)
    sheet_name = f"{month_name} CB (CB{cb_number:02d})"
    await send_log_message(
        bot, "Sheet Access Attempt", f"Attempting to access sheet: {sheet_name}"
    )
    sheet = client.open(SHEET)
    return sheet.worksheet(sheet_name)


# Helper function to get the player name from the Friend IDs sheet
@handle_api_error
async def get_player_name(user_id, bot):
    friend_ids_sheet = client.open(SHEET).worksheet("Friend IDs")
    discord_id_cells = friend_ids_sheet.findall(user_id, in_column=4)
    if not discord_id_cells:
        return None
    player_row = discord_id_cells[0].row
    player_name = friend_ids_sheet.cell(player_row, 2).value
    await send_log_message(
        bot, "Player Name Found", f"Player name found: {player_name}"
    )
    return player_name


# Helper function to validate unit name in the "Unit Icons" sheet
@handle_api_error
async def validate_unit_name(unit_name, bot):
    unit_icons_sheet = client.open(SHEET).worksheet("Unit Icons")
    try:
        unit_icons_sheet.find(unit_name, in_column=10)
        return True
    except gspread.exceptions.CellNotFound:
        return False

# Helper function to get the date and time from the B1 cell
@handle_api_error
async def get_scheduled_time(bot):
    ppkn_sheet = client.open(SHEET).worksheet("ppkn")
    date_str = ppkn_sheet.cell(1, 2).value  # B1 cell
<<<<<<< HEAD
    await send_log_message(
        bot, "Scheduled Time Retrieved", f"Scheduled time retrieved: {date_str}"
    )
    return datetime.datetime.strptime(date_str, "%m/%d/%Y %H:%M")
=======
    return datetime.strptime(date_str, "%m/%d/%Y %H:%M")
>>>>>>> parent of bb100f4 (cb sheet)
