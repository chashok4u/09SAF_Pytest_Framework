import pandas as pd

class PyRAFTMapper(object):
    def __init__(self,**kwargs):
        self.input_val = kwargs.get("input_val", {})
        self._tool = kwargs.get('tool', None)
        self._build_id = self.input_val.get('build_id', None)  # build_id
        self._build_url = self.input_val.get("build_url", None)  # build_url
        self._pipeline_name = self.input_val.get('pipeline_name', None)  # pipeline_name
        self._tags = self.input_val.get('tags', "LocalRun")  # tags
        self._environment = self.input_val.get('environment', "LocalRun/Default")  # environment
        self._automation_tool = self.input_val.get('tool', None)  # tool

    @property
    def comments_with_out_build(self):
        cm_out_build_info= dict(
            {
                "Invalid Markers": [self._tags],
                "Automation Tool": [self._automation_tool],
                "Pipeline Name ": [self._pipeline_name],
                "Test Environment": [self._environment]
            }
        )

        return pd.DataFrame(cm_out_build_info)

    @property
    def build_url_tb_format(self):
        return pd.DataFrame({"Build URL": [self._build_url]})

    @property
    def tbl_html(self):
        return self.comments_with_out_build.to_html(index=False)+self.build_url_tb_format.to_html(index=False)


