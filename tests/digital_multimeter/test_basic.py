from digital_multimeter.main import DigitalMultimeter


def test_default_model():
    dm = DigitalMultimeter()
    assert dm.model == "Default"


def test_default_multimeter():
    dm = DigitalMultimeter()
    assert dm.multimeter is None


def test_default_models():
    dm = DigitalMultimeter()
    assert type(dm.get_models_supported()) is dict
    assert "models" in dm.get_models_supported().keys()
    assert type(dm.get_models_supported()["models"]) is list
    assert "Default" in dm.get_models_supported()["models"]
