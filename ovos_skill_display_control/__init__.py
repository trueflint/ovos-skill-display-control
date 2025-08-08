from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_workshop.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
import subprocess

DEFAULT_SETTINGS = {
    "log_level": "WARNING",
    "display_device": "HDMI-A-1"
}

class DisplayControlSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().
        """
        super().__init__(*args, **kwargs)
        # be aware that below is executed after `initialize`
        self.override = True

    @classproperty
    def runtime_requirements(self):
        # if this isn't defined the skill will
        # only load if there is internet
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )
    
    def initialize(self):
        """Performs any final setup of the Skill, for instance to register
        handlers for events that the Skill will respond to.
        This is a good place to load and pre-process any data needed by your Skill.
        """
        # This initializes a settings dictionary that the skill can use to
        # store and retrieve settings. The skill_settings.json file will be
        # created in the location referenced by self.settings_path, which
        # defaults to ~/.config/mycroft/skills/<skill_id>
        # only new keys will be added, existing keys will not be overwritten
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)
        # set a callback to be called when settings are changed
        self.settings_change_callback = self.on_settings_changed
        # below is a custom event, system event specs found at
        # https://openvoiceos.github.io/message_spec/
        self.add_event("ovos.display.sleep", self.handle_sleep_display_event)
        self.add_event("ovos.display.wake", self.handle_wake_display_event)
        self.add_event("ovos.display.status", self.handle_display_status_event)

    def on_settings_changed(self):
        """This method is called when the skill settings are changed."""
        LOG.info("Settings changed!")

    @property
    def log_level(self):
        """Dynamically get the 'log_level' value from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("log_level", "INFO")

    def is_display_awake(self):
        """Returns True if the display in
        settings.get("display_device") is awake and False if it's
        asleep. If it can't be determined, returns None.
        """
        display = self.settings.get("display_device")
        try:
            output = subprocess.check_output(["wlr-randr"], text=True)
            lines = output.splitlines()

            in_block = False
            for line in lines:
                stripped = line.strip()

                # Start of HDMI-A-1 block
                if stripped.startswith(display):
                    in_block = True
                    continue

                # Reached a new output block
                if in_block and not line.startswith(" "):
                    break

                # Inside the HDMI-A-1 block
                if in_block and stripped.lower().startswith("enabled:"):
                    status = stripped.split(":")[1].strip().lower()
                    return status == "yes"

        except Exception as e:
            LOG.error(f"Failed to check display state: {e}")

        return None  # Unknown or not found

    def sleep_display(self):
        subprocess.run(["wlr-randr", "--output", self.settings.get("display_device"), "--off"])

    def wake_display(self):
        subprocess.run(["wlr-randr", "--output", self.settings.get("display_device"), "--on"])

    def handle_sleep_display_event(self, message):
        LOG.info("ovos-skill-display-control received ovos.display.sleep event.")
        self.sleep_display()
        self.bus.emit(message.reply("ovos.display.sleep.response", {"success": True}))
        self.speak_dialog("display.off")

    def handle_wake_display_event(self, message):
        LOG.info("ovos-skill-display-control received ovos.display.wake event.")
        self.wake_display()
        self.bus.emit(message.reply("ovos.display.wake.response", {"success": True}))
        self.speak_dialog("display.on")

    def handle_display_status_event(self, message):
        LOG.info("ovos-skill-display-control received ovos.display.status event.")
        status = self.is_display_awake()
        self.bus.emit(message.reply("ovos.display.status.response", {"status": status}))

    @intent_handler("SleepDisplay.intent")
    def handle_sleep_display_intent(self, message):
        """Handle SleepDisplay intents from Padatious.

        This is done by sending an ovos.display.sleep event on the
        OVOS message bus, which handle_sleep_display_event will handle
        as the registered handler for that event. It's done this way
        rather than calling sleep_display directly from here in order
        to allow other skills or other agents to also be aware of when
        the display changes state."""
        LOG.info("ovos-skill-display-control received SleepDisplay intent.")
        self.bus.emit(message.reply("ovos.display.sleep", {"source": "intent"}))

    @intent_handler("WakeDisplay.intent")
    def handle_wake_display_intent(self, message):
        LOG.info("ovos-skill-display-control received WakeDisplay intent.")
        self.bus.emit(message.reply("ovos.display.wake", {"source": "intent"}))
