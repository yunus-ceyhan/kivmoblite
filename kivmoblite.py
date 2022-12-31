from kivy.utils import platform
from kivy.core.window import Window
from kivy.metrics import dp
from kvdroid.tools.metrics import Metrics
screen = Metrics()

test = {
        "appId": "ca-app-pub-3940256099942544~3347511713",
        "banId": "ca-app-pub-3940256099942544/6300978111",
        "intId": "ca-app-pub-3940256099942544/1033173712",
        "testD": []
        }

if platform == "android":
    try:
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        activity = autoclass("org.kivy.android.PythonActivity")
        AdListener = autoclass("com.google.android.gms.ads.AdListener")
        AdMobAdapter = autoclass("com.google.ads.mediation.admob.AdMobAdapter")
        AdRequest = autoclass("com.google.android.gms.ads.AdRequest")
        AdRequestBuilder = autoclass(
            "com.google.android.gms.ads.AdRequest$Builder"
        )
        AdSize = autoclass("com.google.android.gms.ads.AdSize")
        AdView = autoclass("com.google.android.gms.ads.AdView")
        Bundle = autoclass("android.os.Bundle")
        Gravity = autoclass("android.view.Gravity")
        InterstitialAd = autoclass("com.google.android.gms.ads.InterstitialAd")
        LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
        LinearLayout = autoclass("android.widget.LinearLayout")
        View = autoclass("android.view.View")
        Color = autoclass('android.graphics.Color')
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    except:
        print(
            "KivMobLite: Cannot load AdMob classes. Check buildozer.spec."
        )


class Admob():
    def __init__(self, adId=test):
        self.ad = adId
        self.ad_size = 0
        self._loaded = False
        self.visiable = False
        self._test_devices = self.ad["testD"] if "testD" in self.ad.keys() and isinstance(self.ad["testD"], list) else []
        MobileAds.initialize(activity.mActivity, self.ad["appId"])

# Banner Ad

    @run_on_ui_thread
    def new_banner(self,position = None, color = None, margin = 0):
        self._adview = AdView(activity.mActivity)
        adsize = AdSize.getCurrentOrientationAnchoredAdaptiveBannerAdSize(activity.mActivity,screen.width_dp() - margin)
        self.ad_size = adsize.getHeight()
        self._adview.setAdSize(adsize)
        self._adview.setAdUnitId(self.ad["banId"])
        self._adview.setVisibility(View.GONE)
        if color:
            self._adview.setBackgroundColor(Color.parseColor(str(color)))
        else:
            self._adview.setBackgroundColor(Color.TRANSPARENT)
        adLayoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT
        )
        self._adview.setLayoutParams(adLayoutParams)
        layout = LinearLayout(activity.mActivity)
        
        if isinstance(position, list)  or isinstance(position, tuple):
            self._adview.setX(position[0])
            self._adview.setY(position[1])
        elif isinstance(position,int):
            self._adview.setY(position)
            self._adview.setX(0)
        elif isinstance(position, str):
            if position == "bottom":
                layout.setGravity(Gravity.BOTTOM)

        layout.addView(self._adview)
        layoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT
        )
        layout.setLayoutParams(layoutParams)
        activity.mActivity.addContentView(layout, layoutParams)
        
        
    @run_on_ui_thread
    def request_banner(self, options={}):
        self._adview.loadAd(self._get_builder(options).build())
        print('KivMobLite: new_banner called')

    @run_on_ui_thread
    def show_banner(self):
        self._adview.setVisibility(View.VISIBLE)
        self.visiable = True
        print('KivMobLite: show_banner called')

    @run_on_ui_thread
    def hide_banner(self):
        self._adview.setVisibility(View.GONE)
        self.visible = False
        print('KivMobLite: hide_banner called')

    @run_on_ui_thread
    def destroy_banner(self):
        self._adview.destroy()
        self.visible = False
        print('KivMobLite: destroy_banner called')
        
    @run_on_ui_thread
    def banner_pos(self, position = None):
        self.hide_banner()
        if isinstance(position, list)  or isinstance(position, tuple):
            self._adview.setX(position[0])
            self._adview.setY(position[1])
        elif isinstance(position, int) or isinstance(position, float):
            self._adview.setX(0)
            self._adview.setY(position)
        elif isinstance(position, str):
            if position == "top":
                self._adview.setX(0)
                self._adview.setY(0)
            else:
                bottom = Window.height - dp(self.ad_size)
                self._adview.setX(0)
                self._adview.setY(bottom)
        self.show_banner()

# interstitial

    @run_on_ui_thread
    def new_interstitial(self):
        self._interstitial = InterstitialAd(activity.mActivity)
        self._interstitial.setAdUnitId(self.ad["intId"])
        
    @run_on_ui_thread
    def request_interstitial(self, options={}):
        self._interstitial.loadAd(self._get_builder(options).build())
        print('KivMobLite: new_interstitial called')

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        self._loaded = self._interstitial.isLoaded()

    def is_interstitial_loaded(self):
        self._is_interstitial_loaded()
        return self._loaded

    @run_on_ui_thread
    def show_interstitial(self):
        if self.is_interstitial_loaded():
            self._interstitial.show()
            
    @run_on_ui_thread
    def destroy_interstitial(self):
        self._interstitial.destroy()

    def _get_builder(self, options):
        builder = AdRequestBuilder()
        if options is not None:
            if "children" in options:
                builder.tagForChildDirectedTreatment(options["children"])
            if "family" in options:
                extras = Bundle()
                extras.putBoolean(
                    "is_designed_for_families", options["family"]
                )
                builder.addNetworkExtrasBundle(AdMobAdapter, extras)
        if self._test_devices:
            for test_device in self._test_devices:
                builder.addTestDevice(test_device)
        return builder


if __name__ == "__main__":
    print(" AdMob support for Kivy Android\n")
