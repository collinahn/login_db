# 과제 4: 로그인 시스템 만들기
# 
# GetPutDB.py
#
# 로그인을 위한 아이디와 비밀번호를 저장하고 DB파일을 관리한다.
# GetPutDB 인스턴스가 생성될 때마다 자동으로 DB파일을 생성한다.
# GetPutDB 인스턴스는 싱글턴으로 관리된다.
# DB파일이 생성되는 경로는 본 파일이 위치한 경로를 기준으로 ./db/login.db에 위치한다.
#
# 2021.11.15 created by 안태영
#

import os
from sqlite3 import Error
import sqlite3
from sqlite3.dbapi2 import Connection

DB_FOLDER_PATH  = "./db/"
DB_FILE         = "login.db"
DB_FILE_PATH    = DB_FOLDER_PATH + DB_FILE

class GetPutDB(object):

  def __new__(cls):
      if not hasattr(cls, "_instance"):
          cls._instance = super().__new__(cls)

          #폴더가 없는 경우
          if os.path.exists(DB_FOLDER_PATH) == False:
              os.mkdir(DB_FOLDER_PATH)
          #파일이 없는 경우
          if os.path.exists(DB_FILE_PATH) == False:
              conn: Connection = None

              try:
                conn = sqlite3.connect(DB_FILE_PATH)
                print(f"{DB_FILE} sqlite3 {sqlite3.version} created")
              except Error as e: print(e)
              finally:
                if conn: conn.close()

      return cls._instance


  def __init__(self):
      cls = type(self)
      if not hasattr(cls, "_init"):
          conn: Connection = None

          try:
            conn = sqlite3.connect(DB_FILE_PATH)
            curs = conn.cursor()

            #테이블 세팅
            curs.execute("CREATE TABLE tUser (id TEXT PRIMARY KEY NOT NULL, pw TEXT NOT NULL);")

            cls._init = True

          except Error as e: print(e)
          finally:
            if conn: conn.close()

  def add_user(self, sID: str, sPW: str) -> bool:
    b_Ret: bool = False
    conn: Connection = None

    try:
      conn = sqlite3.connect(DB_FILE_PATH)
      curs = conn.cursor()

      #유저 정보 삽입
      curs.execute("INSERT INTO tUser Values(?, ?)", (sID, sPW))
      conn.commit()
      b_Ret = True
    except Error as e: print(e)
    finally:
      if conn: conn.close()
      return b_Ret

  #id로 테이블을 참조해 이미 있는 유저인지 확인한다
  def check_exists(self, sID: str) -> bool or None:
    conn: Connection = None
    n_Ret: int = None

    try:
      conn = sqlite3.connect(DB_FILE_PATH)
      curs = conn.cursor()

      query_CheckExists = f"""SELECT EXISTS(SELECT * FROM tUser WHERE id="{sID}")"""
      curs.execute(query_CheckExists)
      n_Ret, = curs.fetchone()

    except Error as e: print(e)
    finally:
      if conn: conn.close()

    return n_Ret

  #id에 해당하는 비밀번호를 가져온다
  def get_idpw(self, sID: str) -> list or None:
    conn: Connection = None
    rows: list = None

    try:
      conn = sqlite3.connect(DB_FILE_PATH)
      curs = conn.cursor()

      #유저 정보 삽입
      curs.execute("SELECT * FROM tUSER WHERE `id`=?", (sID, ))
      rows = curs.fetchall()

    except Error as e: print(e)
    finally:
      if conn: conn.close()

    return rows
