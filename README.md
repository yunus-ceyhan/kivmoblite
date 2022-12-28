That's a customized version of KivMob. It only supports Banner and Interstitial ads.

Requirements `kivy, kvdroid`


```python

# Buildozer

#android.gradle_dependencies = com.google.firebase:firebase-ads:19.6.0

#android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

#android.permissions = INTERNET

from kivmoblite import Admob

# Test ad

test = {
        "appId": "ca-app-pub-3940256099942544~3347511713",
        "banId": "ca-app-pub-3940256099942544/6300978111",
        "intId": "ca-app-pub-3940256099942544/1033173712",
        "testD": []
        }

# Banner

ads = Admob(test)
ads.new_banner(position = "bottom", color = "#ffffff", margin = 0) # Adaptive banner
ads.request_banner()
ads.show_banner()

#ads.hide_banner()
#ads.destroy_banner(
#ads.banner_pos([0,60])
#ads.banner_pos("top") 


# Interstitial

ads.new_interstitial()
ads.request_interstitial()
ads.show_interstitial()

#ads.destroy_intersitital()




