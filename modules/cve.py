import datetime, json
from src import ModuleManager, utils

URL_CVE = "https://cve.circl.lu/api/cve/%s"

class Module(ModuleManager.BaseModule):
    _name = "CVE"

    @utils.hook("received.command.cve", min_args=1)
    def cve(self, event):
        """
        :help: Get the definition of a provided term from Urban Dictionary
        :usage: <term>
        """
        page = utils.http.request(URL_CVE % event["args"].upper(), json=True)

        if page and page.data:
            cve_id = page.data["id"]

            published = "%sZ" % page.data["Published"].rsplit(".", 1)[0]
            published = datetime.datetime.strptime(published,
                utils.ISO8601_PARSE)
            published = datetime.datetime.strftime(published, "%Y-%m-%d")

            rank = page.data["cvss"]
            summary = page.data["summary"]

            event["stdout"].write("%s, %s (%s): %s" %
                (cve_id, published, rank, summary))
        else:
            raise utils.EventsResultsError()
