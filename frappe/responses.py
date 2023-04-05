import frappe

RESPONSE_FLAGS = {
    "ACTION_COMPLETE"       : 200,
    "SUCCESS"               : 200,
    "INVALID_ACCESS"        : 203,
    "SOME_ERROR_OCCURRED"   : 101,
    "UN_AUTHORIZED"         : 401,
    "BAD_REQUEST"           : 400,
    "SERVER_ERROR"           : 500,
    "ALREADY_REQUESTED_CHANGE_MANAGER"   : 453,
    "PARAMETER_MISSING"       :  201
}

RESPONSE_MESSAGES = {
    "ACTION_COMPLETE"                       : 'Success',
    "DATA_UPDATED_SUCCESSFULLY"             : 'Data Updated Successfully',
    "SUCCESS"                               : 'Success',
    "NO_ITEMS_SPECIFIED"                    : "No item specified for the transaction",
    "INVLID_YELO_METADATA"                  : "Invalid format of Yelo metadata.",
    "INVENTORY_NOT_ENABLED"                 : "Inventory is not enabled",
    "INVALID_ARRAY"                         : "{} should be a valid Array",
    "INVALID_OBJECT"                        : "{} should be a valid Object",
    "KEY_REQD"                              : '{} is mandatory',
    "KEYS_REQD"                             : '{} are mandatory',
    "INVALID_AGENT"                         : "Tookan Agent doesn't Exist",
    "NEGATIVE_BALANCE_NOT_ALLOWED"          : "Resulting Balance can not be negative.",
    "ZERO_QTY_NOT_ALLOWED"                  : "Item should be valid Item & Quantity can not be Zero",
    "NEED_TO_BE_EMPLOYEE"                   : "You need to be employee to access",
    "INVALID_ACCESS"                        : 'You are not authorized to access this.',
    "SOME_ERROR_OCCURRED"                   : 'Something went wrong! Please try later.',
    "NO_TIMESHEET"                          : 'No timesheet data for this month.',
    "CURRENT_TIMESHEET"                     : 'Here is your timesheet report: ',
    "NO_REPORTEES"                          : 'You do not have any reportees.',
    "TEAM_PUNCH_STATUS"                     : 'Your team\'s punch status',
    "ALREADY_REQUESTED_CHANGE_MANAGER"      : "You already have an active manager change request. You can't request one more before its completion.",
    "UN_AUTHORIZED"                         : "UN AUTHORIZED",
    "BAD_REQUEST"                           : "BAD REQUEST",
    "REQUEST_SENT_TO_MANAGERS"              : "We have sent this request for approval to your current and new manager. Once approved by both of them, I will update the records.",
    "NO_CHANGES"                            : "No Changes Found!",
    "NEW_FLEET_INSUFFICIENT_FUNDS"          : "New fleet do not have sufficient items to complete order.",
    "NO_TOOKAN_AGENTS"                      : "Tookan Agents are Mandatory .",
    "NO_INCIDENT_MENTIONED"                 : "No incidents are mentioned to update .",
    "PARAMER_MISSING"                       : "Parameter Missing",
    "USER_NOT_AUTHORIZED"                   : "User does not have valid permissions.",
    "INVALID_INCIDENT_ID"                   : "Incident ID not found.",
    "INCIDENT_CANNOT_UNPEND"                : "Incident can no longer be unpended."
}

def send_success(statusCode=None, message=None, data=None):
    response = dict()
    response['statusCode'] = statusCode or RESPONSE_FLAGS['SUCCESS']
    response['message'] = message or RESPONSE_MESSAGES['SUCCESS']
    response['data'] = data or {}
    frappe.local.response['http_status_code'] = response['statusCode']
    return response

def send_error(statusCode=None, message=None, error=None):
    response = dict()
    response['statusCode'] = statusCode or RESPONSE_FLAGS['BAD_REQUEST']
    response['message'] = message or RESPONSE_MESSAGES['BAD_REQUEST']
    if error:
        response['error'] = error
    frappe.local.response['http_status_code'] = response['statusCode']
    return response
