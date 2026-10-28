# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_PERIOD = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False는 정수로 보지 않음)
    return type(day) is int and day >= 1


def _valid_book(book_id):
    return isinstance(book_id, str) and book_id in BOOKS


def _valid_name(name):
    try:
        hash(name)
        return True
    except TypeError:
        return False


class LibraryLoan:
    def __init__(self):
        # 책 번호 -> (빌린 사람, 빌린 날, 반납 기한)
        self.loans = {}
        # 사람 -> 대출 정지 마지막 날 (이 날까지 대출 불가)
        self.suspended_until = {}

    def borrow(self, book_id, name, day):
        # 1. 없는 책 번호
        if not _valid_book(book_id):
            return False
        # 2. 날짜가 1 이상의 정수가 아님
        if not _valid_day(day):
            return False
        if not _valid_name(name):
            return False
        # 3. 이미 누군가 빌려 간 책
        if book_id in self.loans:
            return False

        my_loans = [info for info in self.loans.values() if info[0] == name]
        # 4. 이미 3권 대출 중
        if len(my_loans) >= MAX_LOANS:
            return False
        # 5. 반납 기한이 지난 책을 아직 갖고 있음
        if any(day > due for (_, _, due) in my_loans):
            return False
        # 6. 대출 정지 기간
        if day <= self.suspended_until.get(name, 0):
            return False

        self.loans[book_id] = (name, day, day + LOAN_PERIOD)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_book(book_id):
            return -1
        if not _valid_day(day):
            return -1
        if not _valid_name(name):
            return -1
        info = self.loans.get(book_id)
        # 그 사람이 빌리고 있지 않은 책
        if info is None or info[0] != name:
            return -1
        _, borrowed_day, due = info
        # 빌린 날보다 이른 날짜
        if day < borrowed_day:
            return -1

        overdue = max(0, day - due)
        del self.loans[book_id]

        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 정지: day ~ day+overdue-1
            end = day + overdue - 1
            # 겹치면 더 늦게 끝나는 쪽 (더하지 않음)
            if end > self.suspended_until.get(name, 0):
                self.suspended_until[name] = end
        return overdue

    def get_loans(self, name):
        if not _valid_name(name):
            return []
        result = [(book_id, due) for book_id, (who, _, due) in self.loans.items() if who == name]
        result.sort(key=lambda x: (x[1], x[0]))
        return result
