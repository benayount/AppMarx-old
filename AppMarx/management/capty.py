#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This tries to do more or less the same thing as CutyCapt, but as a
python module.

This is a derived work from CutyCapt: http://cutycapt.sourceforge.net/

////////////////////////////////////////////////////////////////////
//
// CutyCapt - A Qt WebKit Web Page Rendering Capture Utility
//
// Copyright (C) 2003-2010 Bjoern Hoehrmann <bjoern@hoehrmann.de>
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// $Id$
//
////////////////////////////////////////////////////////////////////

"""

import sys
from PyQt4 import QtCore, QtGui, QtWebKit, Qt


class Capturer(object):
    """A class to capture webpages as images"""

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.saw_initial_layout = False
        self.saw_document_complete = False

    def loadFinishedSlot(self):
        self.saw_document_complete = True
        if self.saw_initial_layout and self.saw_document_complete:
            self.doCapture()

    def initialLayoutSlot(self):
        self.saw_initial_layout = True
        if self.saw_initial_layout and self.saw_document_complete:
            self.doCapture()

    def capture(self):
        """Captures url as an image to the file specified"""
        self.wb = QtWebKit.QWebPage()
        self.wb.mainFrame().setScrollBarPolicy(
            QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.wb.mainFrame().setScrollBarPolicy(
            QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

        self.wb.loadFinished.connect(self.loadFinishedSlot)
        self.wb.mainFrame().initialLayoutCompleted.connect(
            self.initialLayoutSlot)

        self.wb.mainFrame().load(QtCore.QUrl(self.url))

    def doCapture(self):
        # print "Capturando"
        self.wb.setViewportSize(Qt.QSize(self.wb.mainFrame().contentsSize().width(), self.wb.mainFrame().contentsSize().width()*194/302))
        img = QtGui.QImage(self.wb.viewportSize(), QtGui.QImage.Format_ARGB32)
        print self.wb.viewportSize()
        painter = QtGui.QPainter(img)
        self.wb.mainFrame().render(painter)
        painter.end()
        img.save(self.filename)
        QtCore.QCoreApplication.instance().quit()

def take_screenshot(url, img_path):
    app = QtGui.QApplication(['capty.py', url, img_path])
    c = Capturer(url, img_path)
    c.capture()
    app.exec_()
