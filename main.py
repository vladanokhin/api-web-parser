from application import app


@app.errorhandler(404)
def not_found(e):
    return {'status': 'error', 'message': 'The requested URL was not found on the server'}, 404


if __name__ == '__main__':
    app.run()
