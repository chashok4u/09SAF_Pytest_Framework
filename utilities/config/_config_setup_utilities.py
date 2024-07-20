import configparser
sysconfiginfo = configparser.RawConfigParser()


class PyRAFTConfig ():
    def __init__(
        self,
        property_path,
    ):
        if property_path is None:
            raise Exception("Provide Property file path")
        elif property_path:
            sysconfiginfo.read(property_path)

    def get_property (self,selection_tag,inproperty):
        if sysconfiginfo.has_option(selection_tag, inproperty) :
             returnproperty= sysconfiginfo.get(selection_tag,inproperty)
             return returnproperty

        return None




