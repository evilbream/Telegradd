import random
from dataclasses import dataclass
from typing import Optional

class APP_INFO:
    def __init__(self, app: list):
        self.app = app
        self.data = random.choice (app)

    @property
    def app_hash(self):
        app_hash = self.data[1]
        return app_hash

    @property
    def app_id(self):
        app_id = int (self.data[0])
        return app_id


class Apps:
    app_data = [['14044787', '47dc1bc15685111a8c993d2c11c3222a'], ['12805420', '393b859fed913851dcbcb0b85cd6172a'],
              ['17017421', 'e944c34b019b0e8212b386004eba4131'], ['18492128', 'add2d2780adf3235b6188797e8f1c31f'],
              ['12063733', '7a9b852dbaf300be5be84b5df01fd346'], ['12846268', 'cd390fbbe4456fb346037017d2c415a0'],
              ['15797233', 'c6573a561a2df3ddeb17a75e0254508a'], ['19589229', '7d7005d0b64e9b315f9b85c1133846cb'],
              ['13676407', '41b815fcdab69a8abf4a452ef6421767'], ['18623459', '0a47b9a8fed443c753f59c26a65eefeb'],
              ['19842898', '5396634790f8b3b59002bcef65c0ce6a'], ['12403251', '9d040b41f71ea5e9cf980c885afe4ced'],
              ['11164881', '91a4d2233c6dedb87f74859aee9e6a19'], ['15930691', 'fafa0a1f547372d5f8f473aaf7c87700'],
              ['17298382', 'b2fa6762b00c0259cb5cf2fe81ebe7fb'], ['9784691', 'b6b5fcd0f4c60e1484096c3f0d832022'],
              ['14044787', '47dc1bc15685111a8c993d2c11c3222a'], ['19909411', '0eb0e5096ef1439b25701595d848a288'],
              ['10837431', '853c583677e95b428dff5094affbe472'], ['17590772', 'ac867d00ed6755af257c985436343ea4'],
              ['9744691', 'b94783678d79d500f4af61b9c2a8a39b'], ['12603452', '0ca1fc5927877733148d74d327fc05d4'],
              ['12805420', '393b859fed913851dcbcb0b85cd6172a'], ['10493156', '9bbfa3ee93b993e49dd37900da460080'],
              ['11806452', '95710967459cc453100dd617f3383bbb886e85e'], ['12846268', 'cd390fbbe4456fb346037017d2c415a0'],
              ['14613055', '059e330c41f229adf4ab7dbee9f8dd5a'], ['19302631', '56d863e84ef572e9210a0b2f65082e7c'],
              ['19984573', 'afc8547e32ae9d2fbd2e3645339f453f'], ['11680555', '38d462a4bca53120f07ff4de880bd9fd'],
              ['16614605', 'e98c6401da33803a87eba9531e895787'], ['18492128', 'add2d2780adf3235b6188797e8f1c31f'],
              ['19636479', '6c4ea5d063340a17c11116ca1de99fff'], ['14372857', 'aa65c6bebc401abe73f43be1a3a526a1'],
              ['13437507', '18cc5f152f5f5cf32fc1136cea365de0'], ['11194047', '8e827f38b128f76f917d265feadd4ae6'],
              ['25381375', '08650a0ddc3122b5ee040339afa17bdd'], ['1096745', 'd91b15bd9ad1d7cdda32345a9361586b'],
              ['1096745', 'd91b15bd9ad1d7cdda32345a9361586b'], ['1096745', 'd91b15bd9ad1d7cdda32345a9361586b']]

    def __init__(self) -> None:
        pass
    @property
    def app_info(self):
        app = APP_INFO(Apps().app_data)
        return app.app_id, app.app_hash



