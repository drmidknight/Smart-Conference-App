def Response(status, message, data, code, error):
    return {
        "status": status,
        "message": message,
        "data": data,
        "code": code,
        "error": error     
    }