#!/usr/bin/env python3
"""E168 G2 arm A, rows 13-24. See `attempts_a.py` for the protocol.

Rows: 35, 36, 37, 38, 43, 48, 55, 60, 61, 62, 63, 64.
"""

ATTEMPTS_B = {
35: "The Anthropic model list in that dialog is a catalogue compiled into "
    "the Copilot Chat extension, not a live query against Anthropic, so a "
    "newly released model simply is not in it until the extension ships a "
    "catalogue that contains it. Update VS Code and the GitHub Copilot Chat "
    "extension to current versions, reload the window, and sign out and back "
    "in so the catalogue is re-fetched. If the extension is already current, "
    "GitHub has not yet enabled that model for API-key-managed Anthropic "
    "accounts and the entry will not appear until it does.",

36: "The warning is about the merged APK, not about the individual libraries, "
    "so updating every dependency to a 16 KB build can leave it standing: the "
    "final package still stores or aligns its native libraries the old way. In "
    "the Android Gradle Plugin set `android.bundle.useLegacyPackaging=false` "
    "(and remove `useLegacyPackaging=true` if present) so .so files stay "
    "uncompressed and are zipaligned to 16 KB, then re-run APK Analyzer on "
    "the rebuilt APK rather than on the artifact from the older "
    "architecture. Also check the packaging block for any `jniLibs` "
    "packaging override that is forcing legacy extraction.",

37: "Tailwind v4 changed the cascade, and that is the most likely reason: "
    "utilities moved into a cascade layer, so your universal selector "
    "`* { margin: 0; padding: 0 }`, which is unlayered, now wins over every "
    "padding and margin utility in the stylesheet regardless of specificity. "
    "Remove the global reset (v4's preflight already does this) or wrap it in "
    "`@layer base` so utilities outrank it. Separately, v4 renamed and "
    "reshaped some spacing and logical-property utilities, so check the class "
    "names against the v4 docs for the ones you are using.",

38: "The Language Models tab and the Copilot Chat model picker are different "
    "lists. Language Models registers the Ollama model with a provider, but "
    "Chat's picker shows only models a conversation can be routed to, and for "
    "a local provider it shows the provider's default model rather than every "
    "model the provider serves. Set the Ollama entry as the default in Manage "
    "Models, or select the Ollama provider in the picker first, and confirm "
    "the Ollama extension is installed and the model is pulled. If Copilot "
    "Chat's local-model support is not present in your version, updating the "
    "Copilot Chat extension is required.",

43: "The destination id in the error belongs to a simulator or device that no "
    "longer exists after the iOS 26 rollout - Xcode replaced the runtime set, "
    "so the id Flutter cached is stale while the available-destinations list "
    "shows only a placeholder. Delete the unavailable devices with "
    "`xcrun simctl delete unavailable`, run `flutter clean` and "
    "`pod install`, restart Xcode so it re-reads the new runtimes, and confirm "
    "the deployment target is at or above the new SDK. Then run against a "
    "simulator that actually appears in the list rather than by raw id.",

48: "These are two different conditions and the number tells you which. Error "
    "153 means the player could not determine a valid embed origin, which in a "
    "Flutter app means the WebView's origin is the app's custom scheme rather "
    "than an https origin; that only resolves by serving the page from a real "
    "https origin, or by injecting the `origin` the player expects. Error 15 "
    "means that particular video has embedding disabled by its owner, so no "
    "configuration will fix it and you must use a different video. Test with a "
    "video you know allows embedding to separate the two.",

55: "That SecurityException is a Google Play services version mismatch on the "
    "device: the play-services client library your app was built against is "
    "newer than the Play services installed on the handset or emulator, so "
    "Play services cannot map the calling package and throws while fetching "
    "the service. Update Google Play services on the device (or use a system "
    "image whose Play services are current), and raise the "
    "`play-services-base`/`play-services-maps` versions so the merged manifest "
    "declares the service requirement the libraries expect.",

60: "That line comes from AppOps in the platform, not from your code, and it "
    "means some application declared an attribution tag that its manifest "
    "does not declare through the property element, so AppOps rejects the "
    "tag. The package named after 'manifest of' in the log identifies who is "
    "emitting it - if that is your package, add the matching "
    "`android.app.PROPERTY_ATTRIBUTION_TAG` property declaration to your "
    "manifest for the API level in use; if it is another app's package, this "
    "is platform log noise in your logcat and harmless. Newer Android versions "
    "started logging this, which is why it appeared after your update.",

61: "The compile error is Flutter removing the v1 Android plugin embedding. "
    "`PluginRegistry.Registrar` and `registerWith(Registrar)` belong to the "
    "legacy embedding that Flutter 3.29 no longer ships, and "
    "flutter_barcode_scanner 2.0.0 is still written against it. Upgrade "
    "flutter_barcode_scanner to a release built on the v2 embedding "
    "(FlutterPlugin with the generated plugin registrant), or pin Flutter back "
    "to a version before 3.29 until the package is updated. Overriding the "
    "dependency will not help, because the API the package calls is gone.",

62: "In iOS 26 the bar item's tint is no longer inherited by an arbitrary "
    "custom view hierarchy the way it was for the built-in title and image "
    "paths, so setting tintColor on the UIBarButtonItem leaves a custom view "
    "rendering with its own colours. Set the tint explicitly on the custom "
    "view itself (and on any subviews that override tintColorDidChange), or "
    "wrap the custom view in a UIHostingConfiguration / configuration-based "
    "bar item so the system applies the item's tint to the content. If you "
    "rely on the tint propagating, the explicit per-view tint is the "
    "reliable route.",

63: "Two things are going on. Declining the Angular telemetry prompt during "
    "project creation aborts the Angular CLI part of the template "
    "generation, so the client project is created without its sources - answer "
    "Yes to the prompt, or generate with the Angular CLI and wire it into the "
    "solution yourself. Separately, recent Angular versions renamed the "
    "scaffolded default component from `app.component.ts` to `app.ts`, so a "
    "template that expects the old filename can reference a file the new CLI "
    "never writes; pin the CLI to the major the template targets if you need "
    "the old layout.",

64: "The documentation you read is for the latest androidx.core, and that is "
    "why the source at cs.android.com shows the function while your build "
    "does not have it. `WindowCompat.enableEdgeToEdge` only exists from a "
    "recent androidx.core release; an older app is resolving an older core "
    "artifact, so raise the `androidx.core:core` dependency (and "
    "`androidx.activity` for `ComponentActivity.enableEdgeToEdge`) to a "
    "version that ships the method, then sync Gradle. Confirm which version "
    "is actually resolved with `gradle dependencies` rather than reading the "
    "reference docs.",
}