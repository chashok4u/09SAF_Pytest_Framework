from utilities.file_handles.file_util import Files

fso = Files()

class Filterjson:

    def getvalue(self, json_input , input_key):
        """
        Description: This method helps to get value from json file (environment details file)\n
        :param input_key: value which needs to be retrieve \n
        :return: return retrieved value from json\n
        """
        jsoninfo = None
        try:
            jsoninfo = next(self.getpath(json_input, input_key))
        except Exception as e:
            print(e)
        finally:
            return jsoninfo

    def getpath(self, json_input, lookup_key):
        """
        Description: This method helps to get value from json file (environment details file)\n
        :param json_input: json file \n
        :param lookup_key: value which needs to be retrieve \n
        :return: return retrieved value from json\n
        """
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    yield v
                else:
                    yield from self.getpath(v, lookup_key)
        elif isinstance(json_input, list):
            for item in json_input:
                yield from self.getpath(item, lookup_key)