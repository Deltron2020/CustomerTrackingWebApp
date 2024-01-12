from app import app

print(__name__)
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)