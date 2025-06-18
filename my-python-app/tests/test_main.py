from app.main import main
import pytest
from io import StringIO
import sys

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "My name is Mukul" in captured.out
