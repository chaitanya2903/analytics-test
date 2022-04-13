from app import app

if __name__ == "__main__":
    if "moody.sqlite" not in os.listdir():
        create_db()
    app.run()