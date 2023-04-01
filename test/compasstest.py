#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Compass component
:author: Thomas Calmant
:copyright: Copyright 2013, isandlaTech
:license: GPLv2
:version: 0.1
:status: Alpha
"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------------

# Local package

# PyQt5
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Requires, Provides, \
    Property, Instantiate, Invalidate, Validate
import pelix.ipopo.constants as constants
import pelix.remote
import pelix.services

# Standard library
import logging
import os

# ------------------------------------------------------------------------------

COMPASS_DETAILS_FACTORY = "compass-details-factory"

_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

@ComponentFactory("compass-details-creator-factory")
@Requires('_ipopo', constants.IPOPO_SERVICE_SPECIFICATION)
@Instantiate("compass-details-creator")
class CompassDetailsCreator(object):
    """
    Compass details creator
    """
    def __init__(self):
        """
        Sets up the component
        """
        # iPOPO service
        self._ipopo = None

        # Instances
        self._instances = {}

        # Local framework UID
        self._local_uid = None


    def __make_name(self, uid):
        """
        Sets up a component name using the given UID
        :param uid: A framework information component UID
        :return: A component name
        """
        return "compass-details-{0}".format(uid)


    def make(self, uid):
        """
        Sets up a bundles details component
        :param uid: A framework information component UID
        """
        if not uid:
            uid = None

        try:
            # Already created component
            return self._instances[uid]

        except KeyError:
            # Prepare the @Requires filter override, to select the associated
            # compass
            properties = {}

            if uid:
                probe_filter = "({0}={1})" \
                               .format(pelix.remote.PROP_ENDPOINT_FRAMEWORK_UUID, uid)

            else:
                probe_filter = "(!({0}=*))" \
                               .format(pelix.remote.PROP_ENDPOINT_FRAMEWORK_UUID)

            properties[constants.IPOPO_REQUIRES_FILTERS] = {'_compass':
                                                            probe_filter}

            # Prepare the EventAdmin handler filter
            properties[pelix.services.PROP_EVENT_FILTER] = \
                    "({0}={1})".format(pelix.services.EVENT_PROP_FRAMEWORK_UID,
                                       self._local_uid if uid is None else uid)

            # Setup the compass file name
            properties['compass.path'] = os.path.join(os.getcwd(), "ui",
                                                      "compass.png")

            # Make the component
            component = self._ipopo.instantiate(COMPASS_DETAILS_FACTORY,
                                                self.__make_name(uid),
                                                properties)
            self._instances[uid] = component
            return component


    def delete(self, uid):
        """
        Deletes a bundles details component
        :param uid: A framework information component UID
        """
        if not uid:
            uid = None

        if uid in self._instances:
            # Delete it
            del self._instances[uid]
            try:
                self._ipopo.kill(self.__make_name(uid))

            except ValueError:
                # The instance was already gone
                pass


    @Validate
    def validate(self, context):
        """
        Component validated
        :param context: Bundle context
        """
        self._local_uid = context.get_property(pelix.framework.FRAMEWORK_UID)


    @Invalidate
    def invalidate(self, context):
        """
        Component invalidated
        :param context: Bundle context
        """
        # Clear all known instances
        for framework_id in self._instances.keys():
            self.delete(framework_id)

        self._instances.clear()
        self._local_uid = None

# ------------------------------------------------------------------------------

class CompassWidget(QtWidgets.QWidget):
    """
    Compass widget
    By: epifanio
    From: http://www.diotavelli.net/PyQtWiki/Compass%20widget
    """
    def __init__(self, parent=None):
        """
        Sets up members
        :param parent: UI container
        """
        QtWidgets.QWidget.__init__(self, parent)

        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}

    def paintEvent(self, event):
        """
        Widget painting event
        """
        # Start painting
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Clear the background
        painter.fillRect(event.rect(),
                         self.palette().brush(QtGui.QPalette.Window))

        # Draw the cardinal points
        self.drawMarkings(painter)

        # Draw the needle
        self.drawNeedle(painter)

        # Stop painting
        painter.end()


    def drawMarkings(self, painter):
        """
        Draws the cardinal points
        :param painter: A QPainter object
        """
        painter.save()

        # Move to the center of the compass
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        # Setup the fonts and the painter
        font = QtGui.QFont(self.font())
        font.setPixelSize(10)
        metrics = QtGui.QFontMetricsF(font)

        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))

        i = 0
        while i < 360:
            if i % 45 == 0:
                # Named direction (every 45°)
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i]) / 2.0, -52,
                                 self._pointText[i])
            else:
                # Small line
                painter.drawLine(0, -45, 0, -50)

            # Next line (+15°)
            painter.rotate(15)
            i += 15

        painter.restore()


    def drawNeedle(self, painter):
        """
        Draws a needle
        :param painter: A QPainter object
        """
        painter.save()

        # Move to the center of the compass
        painter.translate(self.width() / 2, self.height() / 2)

        # Rotate to the correct angle
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        # Setup the painter
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(self.palette().brush(QtGui.QPalette.Shadow))

        # Draw the needle
        painter.drawPolygon(
            QtGui.QPolygon([QtCore.QPoint(-10, 0),
                            QtCore.QPoint(0, -45),
                            QtCore.QPoint(10, 0),
                            QtCore.QPoint(0, 45),
                            QtCore.QPoint(-10, 0)])
            )

        # Change color
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))

        # Draw the end of the needle
        painter.drawPolygon(
            QtGui.QPolygon([QtCore.QPoint(-5, -25),
                            QtCore.QPoint(0, -45),
                            QtCore.QPoint(5, -25),
                            QtCore.QPoint(0, -30),
                            QtCore.QPoint(-5, -25)])
            )

        painter.restore()


    def sizeHint(self):
        """
        Returns the (constant) size of the compass widget: 150x150
        """
        return QtCore.QSize(150, 150)


    def angle(self):
        """
        Returns the current angle of the compass
        """
        return self._angle


    @QtCore.pyqtSlot(float)
    def setAngle(self, angle):
        """
        Sets the angle of the compass
        """
        if angle != self._angle:
            self._angle = angle
            self.angleChanged.emit(angle)
            self.update()

    angle = QtCore.pyqtProperty(float, angle, setAngle)
    angleChanged = QtCore.pyqtSignal(float)

# ------------------------------------------------------------------------------

@ComponentFactory(COMPASS_DETAILS_FACTORY)
@Property('_event_handler_topic', pelix.services.PROP_EVENT_TOPICS,
          ["pelix/demo/compass/*"])
@Property('_event_handler_filter', pelix.services.PROP_EVENT_FILTER)
@Property('_export_interface', pelix.remote.PROP_EXPORTED_INTERFACES,
          [pelix.services.SERVICE_EVENT_HANDLER])
class CompassDetails(object):
    """
    Compass details
    """
    def __init__(self):
        """
        Sets up the component
        """
        # The associated probe
        self._compass = None

        # The Qt loader
        self._qt_loader = None

        # Associated framework information component UID
        self._uid = None

        # Event handler: topic & filter
        self._event_handler_topic = None
        self._event_handler_filter = None

        # Export property
        self._export_interface = None

        # Graphic view
        self._compass_widget = None


    def handle_event(self, topic, properties):
        """
        Notification of an event by EventAdmin
        """
        if topic.endswith("angle"):
            # Angle update
            if self._compass_widget is not None:
                angle = float(properties.get('angle'))
                self._compass_widget.setAngle(angle)


    def get_uid(self):
        """
        Returns the UID of the associated information component
        :return: A UID
        """
        return self._uid


    def get_name(self):
        """
        Returns the name to show in the UI
        """
        return "Compass"


    def get_widget(self, parent):
        """
        Returns the widget to be shown in the framework information panel
        :param parent: The parent UI container
        :return: A Qt widget
        """
        # Load the compass image
        self._compass_widget = CompassWidget(parent)
        return self._compass_widget


    def clean(self):
        """
        Cleans up UI members
        """
        self._compass_widget = None