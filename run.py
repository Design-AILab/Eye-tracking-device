from EyeTracking import app

if __name__ == "__main__":
    context  = ('cert/server.crt', 'cert/server.key')
    app.run('0.0.0.0', port=8100, debug=True, ssl_context=context)