import sqlite3

# 굳이 sqlite3이 아닌 다른 MySQL와 같은 DB의 connect를 이뤄도 상관없습니다.
# 여기서는 파이썬 파일과 같은 위치에 blog.sqlite3 파일이 있다고 가정합니다.

class Command(BaseCommand):




    # ============================================
    # -- Get TFIDF
    # ============================================

    def _initialize(self):
        conn = sqlite3.connect("blog.sqlite3")
        cur = conn.cursor()
        cur.execute("select * from post where id < 10;")




    def handle(self, *args, **kwargs):
        self._initialize()

