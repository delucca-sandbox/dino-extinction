"""Dinossaurs Handlers Unit Tests.

This test file will ensure that the most important logic of our Dinossaur
blueprint handlers are working as we are expecting.

"""
from mock import patch
from faker import Faker
from dino_extinction.blueprints.dinossaurs import handlers


@patch('dino_extinction.blueprints.dinossaurs.handlers.models')
def test_called_model(mocked_models):
    """Call our model.

    This test will ensure that our handler is calling our model during the
    creation of a new dinossaur.

    ...

    Parameters
    ----------
    mocked_models : magic mock
        The mock of our dinossaur models module.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    board_position = fake.word()
    mocked_instance = mocked_models.DinossaurSchema.return_value

    # when
    handlers.new_dinossaur(battle_id, board_position)

    # then
    expected_load = dict()
    expected_load.update({'battle_id': battle_id})
    expected_load.update({'position': board_position})

    assert mocked_models.DinossaurSchema.call_count == 1
    mocked_instance.load.assert_called_once_with(expected_load)
