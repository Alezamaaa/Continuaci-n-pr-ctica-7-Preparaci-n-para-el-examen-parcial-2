import book
import library
import pytest
import user

@pytest.mark.unit
def test_borrow_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch', 2026, 'ISBN001')

    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True

@pytest.mark.unit
def test_borrow_book_two_times():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch', 2026, 'ISBN001')

    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()

@pytest.mark.unit
def test_resturn_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch', 2026, 'ISBN001')

    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    book1.return_book()
    assert book1.borrowed == False

@pytest.mark.unit
def test_borrow_book_error_with_try_except():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch', 2026, 'ISBN001')
    book1.borrow()
    error_message = None

    try:
        book1.borrow()
    except ValueError as error:
        error_message = str(error)

    assert error_message == "The book is already borrowed"

@pytest.fixture
def lib_init():
    lib = library.Library()
    book_tenoch = book.Book('Orgullo y prejuicio', 'Tenoch', 2026, 'ISBN001')
    lib.add_book(book_tenoch)
    Tenoch = user.User('Tenoch', 'ID0001')
    lib.add_user(Tenoch)
    return lib

@pytest.mark.system
def test_library_init(lib_init):
    lib = lib_init
    lib.borrow_book('ID0001', 'ISBN001')
    assert lib.books[0].borrowed == True

@pytest.mark.system
def test_library_init_ID_Not_Registered(lib_init):
    lib = lib_init

    with pytest.raises(ValueError,match="User not found"):
        lib.borrow_book('ID0003', 'ISBN001')


####################

@pytest.mark.wip
def test_library_init_Book_Not_Registered(lib_init):
    lib = lib_init

    with pytest.raises(ValueError,match="Book not found"):
        lib.borrow_book('ID0001', 'ISBN002')

@pytest.mark.parametrize("name,user_id", [
    ("Ana", "ID0002"),
    ("Juan", "ID0003"),
    ("Marta", "ID0004"),
])
@pytest.mark.system
def test_find_users_parametrize(lib_init, name, user_id):
    lib = lib_init
    new_user = user.User(name, user_id)
    lib.add_user(new_user)

    assert lib._find_user(user_id) is new_user

@pytest.mark.system
def test_monkeypatch_setattr(lib_init, monkeypatch):
    monkeypatch.setattr(lib_init, "books", [])
    assert lib_init.books == []

@pytest.mark.system
def test_monkeypatch_delattr(lib_init, monkeypatch):
    lib_init.test_value = "temporary"
    monkeypatch.delattr(lib_init, "test_value")
    assert not hasattr(lib_init, "test_value")

@pytest.mark.system
def test_monkeypatch_setitem(lib_init, monkeypatch):
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    lib_init.borrow_book("ID0001", "ISBN001")
    assert lib_init.books[0].borrowed == False

@pytest.mark.examen
def test_capsys(lib_init, capsys):
    lib_init._find_user("ID0001")
    assert capsys.readouterr().out == "User not found\n"


#para try except es en el. código orignal, se pone el try antes del código
#y el except despues del código junto con el "tipo de error" e imprimes algo :b