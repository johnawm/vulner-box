# TRENDNet AP buffer overflow vulnerabilities

![image-20221027101724040](./image/image-20221027101724040.png)

## Overview

* Type: buffer overflow
* Supplier: TRENDNet  (https://www.trendnet.com/)
* Product: TRENDNet TEW-820AP (Version v1.0R)
* Firmware download: https://downloads.trendnet.com/tew-820ap/firmware/tew-820apv1_(fw1.01b01).zip
* affect version: TRENDNet TEW-820AP 1.01.B01



## Description

TrendNet Wireless AC Easy-Upgrader TEW-820AP (Version v1.0R) is vulnerable to buffer overflow in handling http packet in firmware version 1.01.B01 which may result in remote code execution or denial of service. These issues are in the binary boa which resides in /bin folder which is responsible for serving http connection received by the device.

### 1. Vulnerability Details

A stack overflow vulnerability exists in processing the post request “/boafrm/formNewSchedule”. The problem arises in processing “submit-url” parameter which could be arbitrarily long. The value of this parameter is copied onto stack memory without any bounds check by "sprintf" function (as shown at line 20 of Figure B) which could lead to a buffer overflow. The attackers can construct a payload to carry out arbitrary code attacks.



 <img src="./image/image-20221027104231703.png" alt="image-20221027104231703" style="zoom:25%;" />

Figure A: The decompiled code of function which read value of parameter "submit-url" and call send_redirect_perm function with the value as a parameter.

<img src="./image/image-20221027104500584.png" alt="image-20221027104500584" style="zoom:25%;" />

Figure B: The decompiled code of function send_redirect_perm.



### 2. Reproduce and POC

To reproduce the vulnerability, the following steps can be followed:

Start frimware through QEMU system or other methods (real device)

1. Use the default username and password to login web.
2. Execute the poc script POC_for_formNewSchedule.py as follows:

```bash
python3 POC_for_formNewSchedule.py 192.168.1.1
```

