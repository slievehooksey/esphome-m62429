from esphome import automation, pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_CHANNEL, CONF_CLK_PIN, CONF_DIO_PIN, CONF_ID, CONF_VOLUME

m62429_ns = cg.esphome_ns.namespace("m62429")
m62429Controller = m62429_ns.class_("m62429Controller", cg.Component)

SetChannelLevelAction = m62429_ns.class_("SetChannelLevelAction", automation.Action)
IncreaseAction = m62429_ns.class_("MuteAction", automation.Action)
DecreaseAction = m62429_ns.class_("MuteAction", automation.Action)
MuteAction = m62429_ns.class_("MuteAction", automation.Action)
UnmuteAction = m62429_ns.class_("UnmuteAction", automation.Action)
ToggleMuteAction = m62429_ns.class_("ToggleMuteAction", automation.Action)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(m62429Controller),
            cv.Required(CONF_CLK_PIN): pins.internal_gpio_output_pin_schema,
            cv.Required(CONF_DIO_PIN): pins.internal_gpio_output_pin_schema,
        }
    )
)

validate_level_percent = cv.All(cv.int_range(min=0, max=100))
validate_channel = cv.All(cv.int_range(min=0, max=2))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    clk_pin = await cg.gpio_pin_expression(config[CONF_CLK_PIN])
    cg.add(var.set_clk_pin(clk_pin))
    dio_pin = await cg.gpio_pin_expression(config[CONF_DIO_PIN])
    cg.add(var.set_dio_pin(dio_pin))

    cg.add_library("robtillaart/M62429", "0.3.7")


@automation.register_action(
    "m62429.set_level",
    SetChannelLevelAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
            cv.Required(CONF_VOLUME): cv.templatable(validate_level_percent),
            cv.Required(CONF_CHANNEL): cv.templatable(validate_channel),
        },
    ),
    synchronous=True,
)
async def m62492_set_level_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    vol = await cg.templatable(config[CONF_VOLUME], args, cg.uint8)
    cg.add(var.set_level(vol))
    chan = await cg.templatable(config[CONF_CHANNEL], args, cg.uint8)
    cg.add(var.set_channel(chan))
    return var


@automation.register_action(
    "m62429.increase",
    IncreaseAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
            cv.Required(CONF_CHANNEL): cv.templatable(validate_channel),
        },
    ),
    synchronous=True,
)
async def m62492_increase_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    chan = await cg.templatable(config[CONF_CHANNEL], args, cg.uint8)
    cg.add(var.increase_channel(chan))
    return var


@automation.register_action(
    "m62429.decrease",
    DecreaseAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
            cv.Required(CONF_CHANNEL): cv.templatable(validate_channel),
        },
    ),
    synchronous=True,
)
async def m62492_decrease_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    chan = await cg.templatable(config[CONF_CHANNEL], args, cg.uint8)
    cg.add(var.decrease_channel(chan))
    return var


@automation.register_action(
    "m62429.mute",
    MuteAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
        },
    ),
    synchronous=True,
)
async def m62492_mute_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    return var


@automation.register_action(
    "m62429.unmute",
    UnmuteAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
        },
    ),
    synchronous=True,
)
async def m62492_unmute_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    return var


@automation.register_action(
    "m62429.toggle_mute",
    ToggleMuteAction,
    cv.Schema(
        {
            cv.GenerateID(): cv.use_id(m62429Controller),
        },
    ),
    synchronous=True,
)
async def m62492_toggle_mute_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    return var
