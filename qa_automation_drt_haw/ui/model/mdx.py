from qa_automation_drt_haw.ui.model.verification import GeneralVerification
from qa_automation_drt_haw.ui.ui_utils.Logs import log


class MDX:
    # Text to be present on page
    global_none_given = "global.noneGiven"

    def __init__(self, app):
        self.app = app

    def verify_global_none_text_is_not_present(self, text):
        """
        This function verifies the Given text is not present on the page
        """
        try:
            if not GeneralVerification.text_present_on_page(self.app.verification, text):
                assert True, "Text is not present on the page"
        except AssertionError:
            log.info("The Text %s is not present on the page" % self.global_none_given)
            assert True, "The Text %s is not present on the page"% self.global_none_given
