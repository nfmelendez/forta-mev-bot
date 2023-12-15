
ETHEREUM_ROUTERS = [
    "0x3328f7f4a1d1c57c35df56bbf0c9dcafca309c49",
    "0x80a64c6d7f12c47b7c66c5b4e20e72bc1fcd5d9e",
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
]

POLYGON_ROUTERS= [

]

BSC_ROUTERS = [
"0x10ed43c718714eb63d5aa57b78b54704e256024e" #pankake swap
"0x27F1343F58D495C9cd62a36B27F2149033D3CBBe" # pankake swap MEME
"0x77f50d741997dbbbb112c58dec50315e2de8da58" # Furio
]

AVALANCHE_ROUTERS = [
"0xb4315e873dBcf96Ffd0acd8EA43f689D8c20fB30" # trader joe v2.1
"0x60aE616a2155Ee3d9A68541Ba4544862310933d4" # trader joe

]

OP = []

FANTOM_ROUTERS = [
    
]

ROUTERS = {
    1 : ETHEREUM_ROUTERS,
    137 : POLYGON_ROUTERS,
    56 : BSC_ROUTERS,
    43114 : AVALANCHE_ROUTERS,
    10: OP,
    250 : FANTOM_ROUTERS
}