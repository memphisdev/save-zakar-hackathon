from streamlit.connections import ExperimentalBaseConnection

from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError

class MemphisConnection(ExperimentalBaseConnection[Memphis]):

    async def _connect(self, **kwargs) -> Memphis:
        host = self._secrets['host']
        username = self._secrets['username']
        password = self._secrets['password']
        account_id = self._secrets['account_id']

        memphis = Memphis()
        await memphis.connect(host=host,
                              username=username,
                              password=password,
                              account_id=account_id)
        return memphis
