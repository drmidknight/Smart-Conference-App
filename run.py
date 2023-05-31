import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=4)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host='localhost', port=8008, log_level="info",workers=4, reload = True)
    print("running")