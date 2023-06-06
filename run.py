import uvicorn




if __name__ == '__main__':
    uvicorn.run("app.main:app", host='0.0.0.0', port=2020, log_level="info", reload = True)
    print("running")

# if __name__ == '__main__':
#     uvicorn.run("app.main:app", host='http://dev-1.aiti-kace.com.gh', port=2020, log_level="info",workers=4, reload = True)
#     print("running")