[![gitlocalized ](https://gitlocalize.com/repo/9611/whole_project/badge.svg)](https://gitlocalize.com/repo/9611?utm_source=badge)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/OpenVoiceOS/ovos-skill-display-control)

# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/smile.svg' card_color='#22a7f0' width='50' height='50' style='vertical-align:bottom'/> Display Control

OVOS Skill allowing voice and programmatic control of the OS display,
specifically putting it to sleep and waking it up

## About

OVOS doesn't seem to have a native mechanism for screen sleep based on
voice inactivity -- or anything else. This skill fills that gap by
letting you:

- Tell the screen to sleep or wake via **voice**
- Trigger screen sleep/wake via **message bus events**

Motivation: I'm running OVOS on a Raspberry Pi with a monitor attached
so I can see visual responses (I like the date/time display and
weather report). But at night I want the monitor off so I can sleep. I
could use a screensaver, but for one thing, that would react only to
keyboard/mouse input, not OVOS voice input, and for another thing, a
blank black screen still produces significant light.

## Voice Examples

- "Screen off."
- "Turn your display on."
- "Turn off the monitor."
- "Wake the screen."

---

## Message Bus API

This skill listens for the following events on the OVOS message bus:

### `ovos.display.sleep`

Turns off the configured display (via `wlr-randr`).  
**Returns:** `ovos.display.sleep.response` with `{ "success": true }`

Example use from another skill:
`self.bus.emit(Message("ovos.display.sleep"))`

### `ovos.display.wake`

Turns on the configured display (via `wlr-randr`).  
**Returns:** `ovos.display.wake.response` with `{ "success": true }`

Example use from another skill:
`self.bus.emit(Message("ovos.display.wake"))`

## Credits

- [Mycroft AI](https://github.com/MycroftAI)  
- [OpenVoiceOS](https://github.com/OpenVoiceOS)  
- T. J. Lee ([@trueflint@bsky.app](https://bsky.app/profile/trueflint.bsky.social))

## Category

**Utility**

## Tags

#displaycontrol #screen #monitor #sleep #wake #utility #automation
