from EyeTracking import app

if __name__ == "__main__":
    context  = ('cert/server.crt', 'cert/server.key')
    app.run(debug=True, ssl_context=context)