import static
import urllib.request
import regex
import os

urllib.request.urlcleanup()
data = urllib.request.urlopen(static.VERSION_URL).readlines()
data = map(lambda x: x.decode(), data)
data = "".join(data)
version = regex.findall(static.VERSION_REGEX, data)[0]
version = version[11:16]

nv1, nv2, nv3 = version.split(".")
cv1, cv2, cv3 = static.VERSION.split(".")

nv1, nv2, nv3, cv1, cv2, cv3 = int(nv1), int(nv2), int(nv3), int(cv1), int(cv2), int(cv3)

flag_update = False

if nv1 > cv1: flag_update = True
elif nv2 > cv2: flag_update = True
elif nv3 > cv3: flag_update = True

if flag_update:
    print("Updating engine, please wait...")

    for file, url in static.UPDATE_FILES.items():
        data = urllib.request.urlopen(url).readlines()
        data = map(lambda x: x.decode(), data)
        data = "".join(data)

        with open(os.path.join(os.path.split(__file__)[0], file), "w") as f:
            f.write(data)
