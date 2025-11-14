import pytest, json
from app.models import Availability


def test_availabliity_from_dict(availability_data):
    availability = Availability.from_dict("user123", availability_data)

    assert availability.user_id == availability_data["user_id"]
    assert json.loads(availability.slot_ids) == availability_data["slot_ids"]

def test_availability_from_dict_not_list(availability_data):
    availability_data["slot_ids"] = "not_a_list"

    with pytest.raises(ValueError) as e:
        Availability.from_dict("user123", availability_data)

    assert str(e.value) == "Slot IDs must be a list."

def test_availability_to_dict(availability_data):
    availability = Availability.from_dict("user123", availability_data)
    availability_dict = availability.to_dict()

    assert availability_dict["slot_ids"] == availability_data["slot_ids"]   