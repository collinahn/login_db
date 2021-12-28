# 과제 4: 로그인 시스템 만들기
#
# Login.py
#
# 회원가입 및 로그인을 처리한다.
# 회원가입시 회원의 비밀번호를 SHA-256 알고리즘을 사용하여 해시 후 DB에 저장한다.
# 회원가입시 아이디가 이미 있으면 이미 생성된 계정임을 알리고 
# 로그인시 db에 저장된 ID/PW를 대조해 안내 메시지를 내보낸다.
# 
# 2021.11.16 created by 안태영
#

from GetPutDB import GetPutDB
import hashlib

SIGN_IN = "1"
LOG_IN  = "2"

SELECT_MSG = """
1. 회원가입
2. 로그인
메뉴를 선택하세요. """
SELECT_FAILURE = "잘못 선택하셨습니다. 다시 선택하세요."

SIGNIN_SUCCESS          = "계정이 생성되었습니다."
SIGNIN_DB_FAILURE       = "계정이 생성되지 않았습니다."
SIGNIN_CREATED_FAILURE  = "이미 생성된 계정입니다."

LOGIN_SUCCESS           = "올바른 계정입니다."
LOGIN_DB_FAILURE        = "로그인에 실패했습니다."
LOGIN_FAILURE           = "잘못된 계정입니다."

SQL_INJECTION_FILTER    = """ '"`~!@#$%^&*()-+=<>,./?;:}{[]\|"""
ID_INCORRECT            = "아이디에 언더바(_)를 제외한 공백 및 특수기호는 사용하실 수 없습니다."


class Login(object):

    def __init__(self):

        self.db = GetPutDB()

    
    @staticmethod   # SHA-256으로 문자열을 해시하여 16진수 str형태로 리턴하는 함수
    def hash_sha256(sPW: str) -> str:
        s_Ret = hashlib.sha256(sPW.encode())
        return s_Ret.hexdigest()

    @staticmethod   # id는 db에 직결되므로 sql인젝션 검사한다. 필터링되는게 있으면 True 반환
    def detect_injection(sID: str) -> bool:
        return any(c in sID for c in SQL_INJECTION_FILTER)


    def sign_in(self, sID: str, sPW: str) -> None:
        if self.db.check_exists(sID):
            print(SIGNIN_CREATED_FAILURE)
            return

        b_Ret = self.db.add_user(sID, sPW)

        if b_Ret: print(SIGNIN_SUCCESS)
        else: print(SIGNIN_DB_FAILURE)


    def log_in(self, sID: str, sPW: str) -> None:
        lst_target = self.db.get_idpw(sID)

        if len(lst_target) < 1 or len(lst_target[0]) < 2: 
            print(LOGIN_FAILURE)
            return

        if lst_target[0][1] == sPW: print(LOGIN_SUCCESS)
        else: print(LOGIN_FAILURE)

    
    def initSystem(self):

        while True:
            menuSelect = input(SELECT_MSG)
            if menuSelect not in (LOG_IN, SIGN_IN):
                print(SELECT_FAILURE)
                continue

            id = input("ID: ")
            pw = self.hash_sha256(input("PW: "))

            if self.detect_injection(id):
                print(ID_INCORRECT)
                continue

            if menuSelect == SIGN_IN: 
                self.sign_in(id, pw)
            elif menuSelect == LOG_IN: 
                self.log_in(id, pw)


if __name__ == "__main__":
    lg = Login()

    lg.initSystem()
