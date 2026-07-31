import os
from ftplib import FTP
from dotenv import load_dotenv

load_dotenv()

FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_ROOT = os.getenv("FTP_ROOT")

LOCAL_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "news", "2009")
REMOTE_DIR = f"{FTP_ROOT}/testsite/2009"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


def connect():
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    return ftp


def ensure_remote_dir(ftp, remote_path):
    parts = remote_path.strip("/").split("/")
    current = ""
    for part in parts:
        current += "/" + part
        try:
            ftp.mkd(current)
            print(f"📁 Created: {current}")
        except Exception:
            pass


def upload_directory(ftp, local_dir, remote_dir):
    ensure_remote_dir(ftp, remote_dir)

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isdir(local_path):
            upload_directory(ftp, local_path, remote_path)
        else:
            ext = os.path.splitext(item)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                with open(local_path, "rb") as file:
                    ftp.storbinary(f"STOR {remote_path}", file)
                    print(f"⬆ Uploaded: {remote_path}")


def main():
    if not os.path.exists(LOCAL_DIR):
        print("Local directory not found.")
        return

    ftp = connect()
    try:
        upload_directory(ftp, LOCAL_DIR, REMOTE_DIR)
    finally:
        ftp.quit()

    print("Done.")


if __name__ == "__main__":
    main()