# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0 (see LICENSE file for details)


from Components.config import config
from Screens.Setup import Setup
from .__init__ import _
from .Version import PLUGIN
from .Debug import logger, log_levels, setLogLevel
from .RecordingUtils import stopTimeshift, startTimeshift
from .ChannelSelection import ChannelSelection


class SetupScreen(Setup, ChannelSelection):

    def __init__(self, session):
        Setup.__init__(self, session, setup="timeshiftcockpit", plugin="Extensions/TimeshiftCockpit", PluginLanguageDomain=PLUGIN)
        ChannelSelection.__init__(self, session)
        self.setTitle(PLUGIN + " - " + _("Setup"))

    def keyOK(self):
        current = self["config"].getCurrent()
        if current:
            cfg = current[1]
            if cfg in (config.plugins.timeshiftcockpit.fixed1, config.plugins.timeshiftcockpit.fixed2):
                self.getChannel(callback=lambda service_str: self._channelSelected(cfg, service_str))
                return
        Setup.keyOK(self)

    def _channelSelected(self, cfg_entry, service_str):
        logger.info("service_str: %s", service_str)
        if service_str is not None:
            cfg_entry.value = service_str
            self["config"].invalidate(self["config"].getCurrent())

    def keySave(self):
        permanent_changed = config.plugins.timeshiftcockpit.permanent.value != config.plugins.timeshiftcockpit.permanent.saved_value
        fixed_changed = (
            config.plugins.timeshiftcockpit.fixed1.value != config.plugins.timeshiftcockpit.fixed1.saved_value or
            config.plugins.timeshiftcockpit.fixed2.value != config.plugins.timeshiftcockpit.fixed2.saved_value
        )
        setLogLevel(log_levels[config.plugins.timeshiftcockpit.debug_log_level.value])
        Setup.keySave(self)
        if permanent_changed:
            if config.plugins.timeshiftcockpit.permanent.value:
                startTimeshift()
            else:
                stopTimeshift()
        elif fixed_changed:
            stopTimeshift()
            startTimeshift()
