# -*- tab-width: 4; indent-tabs-mode: nil; py-indent-offset: 4 -*-
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from uitest.framework import UITestCase
from uitest.uihelper.common import get_url_for_data_file
from libreoffice.uno.propertyvalue import mkPropertyValues

#Bug 107494 - CRASH: LibreOffice crashes while deleting the header containing an image

class tdf107494(UITestCase):
    def test_tdf107494_delete_header_with_image(self):
        with self.ui_test.create_doc_in_start_center("writer") as document:
            xWriterDoc = self.xUITest.getTopFocusWindow()
            #insert header
            self.assertEqual(document.StyleFamilies.PageStyles.Standard.HeaderIsOn, False)
            self.xUITest.executeCommand(".uno:InsertPageHeader?PageStyle:string=Default%20Page%20Style&On:bool=true")
            self.assertEqual(document.StyleFamilies.PageStyles.Standard.HeaderIsOn, True)
            #insert image
            text = document.getText()
            cursor = text.createTextCursor()
            oStyleFamilies = document.getStyleFamilies()
            #https://forum.openoffice.org/en/forum/viewtopic.php?f=7&t=71227
            obj2 = oStyleFamilies.getByName("PageStyles")
            obj3 = obj2.getByName("Standard")
            oHeaderText = obj3.HeaderText
            oHeaderText.setString("New text for header")  #write text to header
            obj4 = oHeaderText.createTextCursor()
            text = obj4.getText()
            cursor = text.createTextCursor()

            textGraphic = document.createInstance('com.sun.star.text.TextGraphicObject')
            provider = self.xContext.ServiceManager.createInstance('com.sun.star.graphic.GraphicProvider')
            graphic = provider.queryGraphic( mkPropertyValues({"URL": get_url_for_data_file("LibreOffice_external_logo_100px.png")}))
            textGraphic.Graphic = graphic
            text.insertTextContent(cursor, textGraphic, False)
            # Delete the header
            with self.ui_test.execute_dialog_through_command(
                    ".uno:InsertPageHeader?PageStyle:string=Default%20Page%20Style&On:bool=false", close_button="yes"):
                pass

            self.assertEqual(document.StyleFamilies.PageStyles.Standard.HeaderIsOn, False)


    def test_tdf107494_delete_footer_with_image(self):
        with self.ui_test.create_doc_in_start_center("writer") as document:
            xWriterDoc = self.xUITest.getTopFocusWindow()
            #insert footer
            self.assertEqual(document.StyleFamilies.PageStyles.Standard.FooterIsOn, False)
            self.xUITest.executeCommand(".uno:InsertPageFooter?PageStyle:string=Default%20Page%20Style&On:bool=true")
            self.assertEqual(document.StyleFamilies.PageStyles.Standard.FooterIsOn, True)
            #insert image
            text = document.getText()
            cursor = text.createTextCursor()
            oStyleFamilies = document.getStyleFamilies()
            #https://forum.openoffice.org/en/forum/viewtopic.php?f=7&t=71227
            obj2 = oStyleFamilies.getByName("PageStyles")
            obj3 = obj2.getByName("Standard")
            oFooterText = obj3.FooterText
            oFooterText.setString("New text for footer")  #write text to footer
            obj4 = oFooterText.createTextCursor()
            text = obj4.getText()
            cursor = text.createTextCursor()

            textGraphic = document.createInstance('com.sun.star.text.TextGraphicObject')
            provider = self.xContext.ServiceManager.createInstance('com.sun.star.graphic.GraphicProvider')
            graphic = provider.queryGraphic( mkPropertyValues({"URL": get_url_for_data_file("LibreOffice_external_logo_100px.png")}))
            textGraphic.Graphic = graphic
            text.insertTextContent(cursor, textGraphic, False)
            # Delete the footer
            with self.ui_test.execute_dialog_through_command(
                    ".uno:InsertPageFooter?PageStyle:string=Default%20Page%20Style&On:bool=false", close_button="yes"):
                pass

            self.assertEqual(document.StyleFamilies.PageStyles.Standard.FooterIsOn, False)

# vim: set shiftwidth=4 softtabstop=4 expandtab:
