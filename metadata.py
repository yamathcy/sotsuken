import pygn
import json


c= '14742784-696183B35476B91443B0E2BC457FDF29'
u=pygn.register(c)

def beautiful(gn_obj):
    print(gn_obj)
    data= json.dumps(gn_obj, sort_keys=True, indent=4, ensure_ascii=False)
    print(data)

    return data

res = beautiful(pygn.search(clientID=c, userID=u,
                            artist='Beatles'))
print(res)
