from kink import di
from app.controllers import DocumentController, QuestionController


def di_container() -> None:
    # controllers
    di[DocumentController] = lambda di: DocumentController()
    di[QuestionController] = lambda di: QuestionController()