from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_workshop.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
import subprocess

DEFAULT_SETTINGS = {
    "log_level": "WARNING"
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
        # (custom) event handler setup example
        # below is a custom event, system event specs found at
        # https://openvoiceos.github.io/message_spec/
        # this can be tested using `mana` (https://github.com/NeonGeckoCom/neon-mana-utils)
        # `mana send-message hello.world`
#        self.add_event("hello.world", self.handle_hello_world_intent)
#        self.my_var = "hello world"

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

    @intent_handler("SleepDisplay.intent")
    def handle_sleep_display(self, message):
        """This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        subprocess.run(["wlr-randr", "--output", "HDMI-A-1", "--off"])
        self.speak_dialog("display.off")

    @intent_handler("WakeDisplay.intent")
    def handle_wake_display(self, message):
        subprocess.run(["wlr-randr", "--output", "HDMI-A-1", "--on"])
        self.speak_dialog("display.on")
