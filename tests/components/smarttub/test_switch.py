"""Test the SmartTub switch platform."""

from smarttub import SpaPump


async def test_pumps(spa, setup_entry, hass, smarttub_api):
    """Test pump entities."""

    for pump in spa.get_pumps.return_value:
        if pump.type == SpaPump.PumpType.CIRCULATION:
            entity_id = f"switch.{spa.brand}_{spa.model}_circulation_pump"
        elif pump.type == SpaPump.PumpType.JET:
            entity_id = f"switch.{spa.brand}_{spa.model}_jet_p1"
        else:
            raise NotImplementedError("Unknown pump type")

        state = hass.states.get(entity_id)
        assert state is not None
        assert state.state == "off"

        await hass.services.async_call(
            "switch",
            "toggle",
            {"entity_id": entity_id},
            blocking=True,
        )
        pump.toggle.assert_called()

        pump.reset_mock()
        await hass.services.async_call(
            "switch",
            "turn_off",
            {"entity_id": entity_id},
            blocking=True,
        )
        # it's already off
        pump.toggle.assert_not_called()

        pump.reset_mock()
        await hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": entity_id},
            blocking=True,
        )
        pump.toggle.assert_called()
