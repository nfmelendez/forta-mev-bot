import requests
import json
import base64
# List of Ethereum addresses
addresses = [
# "0x4cadecc51feb5c1f6d9a902ecc817a1b8c2246f9",
# "0x9a0ef593dcc6a77f80699c9fa00d1e138b67d832",
# "0x3b64216ad1a58f61538b4fa1b27327675ab7ed67",
# "0xb4247d5978060387c0fe91d13a90d5711f65b7ce",
# "0xd911560979b78821d7b045c79e36e9cbfc2f6c6f",
# "0x57af10ed3469b2351ae60175d3c9b3740e1bb649",
# "0xeeaa83b2d581a3a790774d4dae7bf354fffe3376",
# "0x25d88437df70730122b73ef35462435d187c466f",
# "0x000000000dfde7deaf24138722987c9a6991e2d4",
# "0xae08c571e771f360c35f5715e36407ecc89d91ed",
# "0x6f87f1fbf96c1bb0b0cc9bf6a456566919900d3e",
# "0x1b63142628311395ceafeea5667e7c9026c862ca",
# "0x2ed5003ebb8c00002c20000d00004b3500f4398b",
# "0x3c496df419762533607f30bb2143aff77bebc36a",
# "0x0000000000590b74eb97457bf7b3ff6d63c6fde2",
# "0x3bee5122e2a2fbe11287aafb0cb918e22abb5436",
# "0x52a8aa269bea924379d08945c351232c5cc41581",
# "0x9ea3cda5c2adf0370454b9ee28786a068227b1a4",
# "0x77b285fbdb277e53ed29c9dda7c0aa6f2591b09d",
# "0x00000000000747d525e898424e8774f7eb317d00",
# "0x52ca1cb9fc6fbd1cfe5630e74de8738b517a367a",
# "0xd1a0b5843f384f92a6759015c742fc12d1d579a1",
# "0x5050e08626c499411b5d0e0b5af0e83d3fd82edf",
# "0x0c3de458b51a11da7d4616f42f66c861e3859d3e",
# "0xd8c07491caa1edf960db3ceff387426d53942ea0",
# "0x2f1d79860cf6ea3f4b3b734153b52815773c0638",
# "0xbaf6dc2e647aeb6f510f9e318856a1bcd66c5e19",
# "0x8f44e22ac221cc25a46289d1c307d4f34a4dd6c2",
# "0x775c559d9a48ce5a8444c1035c3a8921ab477b8e",
# "0xbf61595c0f53f01e92cc210663dccd7ab237b1d9",
# "0x0055ae46f700bcc53b1b00483d64000d47007200",
# "0x81153f0889ab398c4acb42cb58b565a5392bba95",
# "0x229b8325bb9ac04602898b7e8989998710235d5f",
# "0xbd3afb0bb76683ecb4225f9dbc91f998713c3b01",
# "0x3b7faec3181114a99c243608bc822c5436441fff",
# "0x1f9090aae28b8a3dceadf281b0f12828e676c326",
# "0x95222290dd7278aa3ddd389cc1e1d165cc4bafe5",
# "0xce0babc8398144aa98d9210d595e3a9714910748",
# "0xd2090025857b9c7b24387741f120538e928a3a59",
# "0x690b9a9e9aa1c9db991c7721a92d351db4fac990",
# "0xc9d945721ed37c6451e457b3c7f1e0cec42417fb",
# "0xfeebabe6b0418ec13b30aadf129f5dcdd4f70cea",
# "0x4a137fd5e7a256ef08a7de531a17d0be0cc7b6b6",
# "0xb91d9b045f8a64bca4c69625b00001109932be34",
# "0x0000000000007f150bd6f54c40a34d7c3d5e9f56",
# "0x4fce027bc57d7530b84527f4848983cece4df15e",
# "0x0000000099cb7fc48a935bceb9f05bbae54e8987",
# "0xc4595e3966e0ce6e3c46854647611940a09448d3",
# "0x98c3d3183c4b8a650614ad179a1a98be0a8d6b8e",
"0x0000000f9c4e004706afdca3b2f0c8f08838eb58",
"0x000000e1fddf4fe15db5f23ae3ee83c6a11e8dd1",
"0x0000008682fa8c3aa14b11894e90e3dcbbff715b",
"0x000000000055217587f821917562867172942189",
"0x00000000000a6d473a66abe3dbaab9e1388223bd",
"0x00000000000006b2ab6decbc6fc7ec6bd2fbc720",
"0x00000000de337b4fff5fcbe4df67a85d0bad5d16",
"0x000000000003750173a03a9055296acc36c6afb7",
"0x0074fb0000177e3a00534a0000f8f17300caf0e7",
"0x00af19b40000546f0000ca91acdb0048c1002e0a",
"0x030f11dcba56b8038c3c94f056ea68dc7668630e",
"0x09850f8f1338a0b8c7d94dcc361e965b78d0175a",
"0x14fcc715dfa45f9a2790e85d7f54cd06b5f61b07",
"0x19f241a4fa79c0be2a592bb824d2d490437c5dc9",
"0x1a6155ff9305f6e8a83f40736029b50078c187f0",
"0x1fb421310ceacd0afb2a429bbb4682e522b38ecb",
"0x2deae6ce94d65ac1de19a1fc4bb160c4e02c92ef",
"0x3caa313178b3d34f1a635203b3b4f768b41350fa",
"0x445947140f5e1b742439f6ee24a7690d077bbb89",
"0x469f63223076d1e9e6f729fed620cd47b4241912",
"0x475689d37309e829c3e646c863b1efec3734472a",
"0x49bc3cec1fb7978746f742a4e485d0d601831cea",
"0x4b4867541f6e756be4119a171b7da17a1558c463",
"0x4e69a51f24f5a46919113cc78ab262da74a4611d",
"0x54eeb92cf8ad49c2cb4dc8c9eb5dc9538836016b",
"0x5519935e51fc403f6c69894e683f268c1883e938",
"0x596d13aba9d144fd092d2fb661ff24ed40e24694",
"0x5a2227c3da137cf47a91d0b9df81570fa33cfbe2",
"0x63756a3c3bf677baab9d9e06457402ed05be8570",
"0x64e6d37c95c066c4f2401e28c2e3bdeec06e2ed8",
"0x6916d3ee3cbdd26b382309dd7a0ae160bf57d9ff",
"0x6e8d76bf316eb70d2ffe4ce5480449c65ea4b22a",
"0x6f1cdbbb4d53d226cf4b917bf768b94acbab6168",
"0x752e93ea9aa43309980b13d22d1f5541b15802bd",
"0x770e2e68000065ac970382fe3af0d500bb00a200",
"0x797a05dd6a8bfc1e1eaaa62e744d3aff197c46b1",
"0x7b577a879665ef6ad344da61de7ec2371f6ff68f",
"0x8385c093657503aebd55bac4a9bb0df5d3528835",
"0x89633a6d12200f0ad9ad2219782adf0f54e9065c",
"0x8db64ee50717a0418adf9ad99d8685318d4d4579",
"0x901996e18a3b15359a62ceb247647665fb8ade89",
"0x91a7ca5c4d7eabc7c8f878dc49eed3a4cb28ea8e",
"0xa5db73941cfd6d94821b5ce83d2aa35418bb72d6",
"0xaba28b9b82999ba782c536d545dd88e579326cf0",
"0xac682edd8729d679d6c044cf44e975d5b8fcf90f",
"0xace84676f40438cd12d6708ae5eb25ce817fc207",
"0xaed01433a5f897d7f41cb3a447b9963a65ed8514",
"0xb481c05290ee2e1528acde18e938260143c80d67",
"0xb78dfc0c14016ebb4678d7949ad6e4b8ba14e634",
"0xba3f5c056500ce033e9d74494b820d495efcf19d",
"0xbce7c64180659b4e2e541183b5e2453937b5e541",
"0xc0d1b1193032dd558fad75915813b3342e7c7b6b",
"0xc35d0251737afd7efb83e4104260e2b60b99d752",
"0xc6fecdf760af24095cded954de7d81ab49f8bae1",
"0xc758d5718147c8c5bc440098d623cf8d96b95b83",
"0xcfd4176f7975c70f800d87aeaca316270521595a",
"0xd7f3fbe8c72a961a5515203eada59750437fa762",
"0xda1ee2f81e5fc1c242343141f82ae3ac748e84aa",
"0xe0966747fa192d165414d76f016ce9aafc153bf8",
"0xe08beb8c48e71fd08560db2fbaaa0701b187c7a7",
"0xe6ae75be7c9317af842b8f2c2cd6dc7f49f17184",
"0xeaabd0e75e930f9f36b68be30202d47fd9b58b92",
"0xf095709c1bb6c2f241211506e1c2e7b7c6b6bd45",
"0xf35be9a9a0d4b67e776115fa3b6381986379894d",
"0xf592225866662817e4b5a97028223b808bcc64d2",
"0xf5bf5dcdaa83fd358b5a4eced76f3b947542175a",
"0xfb5185b7f8c61f815b57de679bbc857f510352f7",
"0xfbeedcfe378866dab6abbafd8b2986f5c1768737"
]

#addresses = ["0x57af10ed3469b2351ae60175d3c9b3740e1bb649"]
counter = 1
# Iterate over each address and perform an action
for address in addresses:
    # URL y headers de la solicitud
    url = 'https://docs.walletlabels.xyz/api/request'
    headers = {
        'authority': 'docs.walletlabels.xyz',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog=%7B%22distinct_id%22%3A%22018bb40e-f889-74a5-84e6-f55c5933e6e9%22%2C%22%24device_id%22%3A%22018bb40e-f889-74a5-84e6-f55c5933e6e9%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22%24sesid%22%3A%5B1699886949084%2C%22018bc91b-b337-73b8-9c84-d830bc7dea6c%22%2C1699886117687%5D%2C%22%24session_recording_enabled_server_side%22%3Atrue%2C%22%24console_log_recording_enabled_server_side%22%3Atrue%2C%22%24session_recording_recorder_version_server_side%22%3A%22v2%22%2C%22%24autocapture_disabled_server_side%22%3Afalse%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%7D',
        'origin': 'https://docs.walletlabels.xyz',
        'referer': 'https://docs.walletlabels.xyz/endpoint/label',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # Datos para enviar en el cuerpo de la solicitud
    data = {
        "method": "get",
        "url": "https://api-c.walletlabels.xyz/ethereum/label",
        "params": {"address": address},
        "headers": {"x-api-key": "VxCQx19ms07pBrKMxyQMO2cd0O0bE288C7eRd5Gf"}
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))
    j = json.loads(response.text)
    # texto_decodificado = base64.b64decode(texto_codificado)

    # # Convertir a una cadena si es necesario
    # texto_decodificado_str = texto_decodificado.decode('utf-8')

    # print(texto_decodificado_str)
    # Imprimir la respuesta
    #print(response.text)
    data = j["response"]["data"]
    data_decoded = base64.b64decode(data)
    ds = data_decoded.decode('utf-8')
   # print(ds)
    result = json.loads(ds)
    if result.get("data"):
        for e in result["data"]:
            print(f"{counter},{len(addresses)},{e['address']},{e['label_type']},{e['label_subtype']},{e['label']}")
            counter += 1





