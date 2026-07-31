# 🔇 The Silent Stakeholder — org.wordpress.android

*Roadmap snapshot T0 = 2017-01-01 · generated 2026-07-31 14:36 UTC · mode openai:gpt-5.1*

## The single most important unmet need
> **“I just want to be able to create an account (and new blog) without mysterious errors. When something goes wrong, tell me clearly what the problem is and how to fix it, instead of failing silently or with a generic message that leaves me stuck.” — unaddressed by the roadmap despite the evidence (63% confidence).**

## Ranked gaps

### 1. “I just want to be able to create an account (and new blog) without mysterious errors. When something goes wrong, tell me clearly what the problem is and how to fix it, instead of failing silently or with a generic message that leaves me stuck.”  ·  **IGNORED**  ·  confidence **63%**

**Why a gap:** The user need is about reliably creating a new account (and/or new blog) without opaque or blocking errors, especially in normal conditions. The sample signals show users often cannot create an account at all, see generic or misleading errors, and are left stuck (“not make a account”, “error occurred… not telling what’s the error”, invalid_client, silent partial creation). The nearest roadmap items are narrow, one-off bugs: a bad password error after creation (GH-970), a crash on account creation (GH-1469), a crash on slow connection (GH-688), and a wait-indicator UI glitch (GH-715). These add

*Latent because:* This need is latent because users mostly express raw frustration (“Bad… not make a account”, “Cant able create account showing error”) rather than a structured feature request like “please overhaul the signup flow and error handling.” The pain is extremely high: account creation is a gateway action, and when it fails, users are completely blocked from using the product, reflected in 1–2 star revie

**Confidence** = V 0.388 · D 0.667 · I 0.733 · K 0.793 · G 0.7 · X 0.0 (raw 0.652)

**Backtest:** No close post-T0 issue (nearest GH-6650 'Reader: when someone following blogs too quic', sim 0.47) — consistent with IGNORED.

**Evidence (6 signals):**
- `R-4ba6b4ec` (review ★1) — Bad Its very bad not make a account
- `R-48acd729` (review ★1) — Cant able create account showing error
- `GH-671` (gh_issue ) — Creating an account with password "qwerty12345" fails. Actually, the user is created but can't be logged in at first time -> results an account without blog

- `GH-898` (gh_issue ) — NUX: Creating a new WordPress.com blog is failing. When I try to create a new blog with my existing account, it fails after 10 seconds or so.

- `GH-2544` (gh_issue ) — error invalid_client message invalid client_id. 1. Using Android emulator on Android studio.
2. Trying to create an account.

3.Keep getting this error even after creating/recreating new MyApp and hence getting a new client_id and client_se
- `R-76f42d19` (review ★2) — Error Why its saying that an error uccured when i am creating new account..nd also its not telling whats the error..plz respond me fast nd plz fix this

**Roadmap refs:** `GH-970`, `GH-1469`, `GH-688`, `GH-715`

*Adversarial check:* The claimed gap is: reliable account/blog creation plus clear, actionable error feedback instead of silent or generic failures.

1. **Is this just a frequent, surface-level complaint?**  
The evidence is tightly clustered around the same core failure mode, not a grab bag of generic frustration:
- R-4ba6b4ec: "not make a account" (account creation failure)
- R-48acd729: "Cant able create account showing error" (creation blocked by an error)
- R-76f42d19: explicitly: "its saying that an error uccured when i am creating new account..nd also its not telling whats the error" (generic, non-informati

### 2. “When I add a video to my post—whether via Quick Video, from my gallery, or newly captured—it should upload successfully, stay attached to the post, and be visible to my viewers. I shouldn’t see constant upload errors, end up with empty posts, or publish a post that looks fine in the app but has no   ·  **IGNORED**  ·  confidence **63%**

**Why a gap:** The user need is about reliably getting videos into posts and having them actually appear for viewers: uploads fail with errors, posts publish without the video, quick video posts end up empty, and error messages are confusing or misleading. The roadmap items nearby are mostly tangential: GH-250 is about a specific VideoPress alert, GH-603 about using a shortcode when sharing a video, GH-375 and GH-503 are image‑related, and GH-4579 is about YouTube iframe previews. None of these represent a coherent, prioritized effort to make video upload and publishing robust and understandable end‑to‑end. 

*Latent because:* This need is highly painful (videos not uploading or disappearing undermines entire posts and frustrates both authors and viewers) but only weakly expressed as a single, clear feature request. Users describe symptoms—“videos won’t upload,” “error every time,” “viewers can’t see my videos,” “posts are empty,” “invalid file type,” “post uploaded without the video”—rather than articulating a unified 

**Confidence** = V 0.459 · D 0.667 · I 0.533 · K 0.767 · G 0.8 · X 0.0 (raw 0.667)

**Backtest:** Team later shipped GH-6654 'Async media: broken reattachment identification' (closed 2017-09-22, sim 0.63).

**Evidence (6 signals):**
- `R-a293a934` (review ★1) — So many glitches! Videos won't upload  the keyboard glitches. The mobile app sucks  the follow blog widget isn't working. It keeps sending my users to have to log in when they try to like or follow my blog. And I have tried to fix this over
- `R-3327b693` (review ★1) — Why is it that there's always error when uploading videos? I have videopress but it has this error everytime
- `GH-74` (gh_issue ) — Quick Video posts are empty. Went back to look at my quick video posts in a browser and noticed that they were all empty. 
Tried another post via the app and it was empty too. 
The blog I was testing with does not use video press if that ma
- `GH-190` (gh_issue ) — Quick Vid: Error uploading. Invalid File Type. Not sure if this is a server issue or app issue. 
When publishing a quick video the following error appears. 
"Error: An error occurred while uploading media: Could not write file wpid-VID_2013
- `GH-929` (gh_issue ) — Submitting post before video downloads results in no video. - Create a new post
- Insert a video from your gallery
- Submit the post as soon as the "Downloading media" toast appears

Post will be uploaded without the video.

- `GH-3758` (gh_issue ) — Getting a media error if VideoPress is not enabled. Publishing a post with a video ends up in a Android notification stating:

> Media Error
> Get the VideoPress upgrade to upload video!

We should improve this UX. Perhaps let the user know

**Roadmap refs:** `GH-250`, `GH-603`, `GH-375`, `GH-503`, `GH-4579`

*Adversarial check:* The claimed gap is: *"When I add a video to my post… it should upload successfully, stay attached, and be visible. I shouldn’t see constant upload errors, end up with empty posts, or publish a post that looks fine in the app but has no video."*

Trying to knock this down as just noise or already-covered:

1. **Is this just a generic, frequent complaint (not a coherent gap)?**  
   The evidence is tightly clustered around the same failure mode: user believes they’ve attached a video to a post, but the final result is errors, empty posts, or missing video.
   - R-a293a934: “Videos won't upload… 

### 3. Users need the app to reliably load and refresh their blog posts and in-app blog view after installation and login, without crashes, generic connection errors, or being forced into an external browser. They expect that opening the app will consistently show their latest posts and content, and that t  ·  **IGNORED**  ·  confidence **63%**

**Why a gap:** User reports center on a core, high-pain failure: after install or login, blog posts and feeds often do not load, do not refresh, or the in-app blog view stops working entirely, sometimes with generic connection errors or silent failures. This is experienced as “the app just doesn’t work” for its primary purpose (viewing posts) and leads directly to uninstalls. The nearest roadmap items are only tangentially related: GH-3370 fixes a specific NPE in PostsListAdapter (one crash mode, not the broader reliability of loading/refreshing posts); GH-181 addresses list not updating after deleting the l

*Latent because:* The pain is very high because this is the primary job of the app—if posts don’t load or refresh, the app is effectively useless, which is why users explicitly mention uninstalling and calling it “awful” or “pointless.” However, the explicit request rate is lower because users rarely articulate this as a structured feature or systemic reliability requirement; they just say “not working,” “posts fai

**Confidence** = V 0.759 · D 0.667 · I 0.58 · K 0.713 · G 0.75 · X 0.068 (raw 0.691)

**Backtest:** Team later shipped GH-5874 'Unable to retrieve posts in Reader after relogin' (closed 2017-11-13, sim 0.54).

**Evidence (6 signals):**
- `R-239bff1f` (review ★1) — Just plain doesn't work 'Posts couldn't be refreshed at this time'. No error message  no indication of what the problem is. Uninstalled.
- `R-d469928d` (review ★1) — Disappointing It works really fine whenever I newly install it but after that it doesn't refresh the content and all other stuff anymore
- `R-44ea902e` (review ★1) — Not working
- `R-9264cbca` (review ★1) — Does the website and app has a problem today? Yesterday I was still editing so many stuff on my blog. But roday I can't even open the website! The app doesn't even work properly. pls send me a feedback on what's happening. :(
- `R-27a70f72` (review ★1) — Please help I'm using samsung mega mobile device and after updating to new version  I can not edit even blog or pages. Cause on the screen  the write section appear and close half of the blog/pages which I want to edit and doesn't respond. 
- `GH-905` (gh_issue ) — ArrayIndexOutOfBoundsException in notification settings. - Open the preferences view.
- Enter to the “Show/hide WordPress.com blogs” view. Go back.
- Enter to the “Manage notifications”, go the Blogs section and try to check/uncheck any of 

**Roadmap refs:** `GH-3418`, `GH-1751`, `GH-3370`, `GH-181`, `GH-4873`

*Adversarial check:* The claimed gap is that users need the app to reliably load and refresh their blog posts and in‑app blog view after installation and login, without crashes, generic connection errors, or being forced into an external browser.

Looking at the evidence:
- R-239bff1f: "Posts couldn't be refreshed at this time" with no explanation, leading to uninstall. This directly supports unreliable post refresh and poor error handling.
- R-d469928d: Works on fresh install but then "doesn't refresh the content and all other stuff anymore". This is a clear, repeated-refresh failure pattern, not a one‑off connec

### 4. Users want to be able to reliably reply to, like, and comment on blog comments directly from the app—especially from notifications—on their self‑hosted/Jetpack sites, without cryptic errors like “reply failed” or “answer not possible,” and with clear behavior when a thread is closed or permissions a  ·  **UNDER-PRIORITIZED**  ·  confidence **57%**

**Why a gap:** The user need is about reliably replying/liking/commenting from notifications (and generally in-app) on self‑hosted/Jetpack sites, where users frequently see generic failures like “reply failed” or “answer not possible.” The nearest roadmap items are mostly individual bug tickets: crashes when replying to comment notifications (GH-1553), moderation/permission edge cases (GH-1654, GH-3418), a specific moderation error when commenting on non-member sites (GH-4933), and a missing comment button in Reader for Jetpack sites (GH-3276). These show the team has addressed some related defects, but only

*Latent because:* This need is latent because users mostly report it as isolated failures (“reply failed,” 403 errors, can’t answer comments in the app but can in the browser) rather than as a broad feature request. They assume replying from notifications should already work and only complain when it breaks, often framing it as a bug on their specific site or device. The pain is high: replying to comments is a core

**Confidence** = V 0.478 · D 0.667 · I 0.41 · K 0.752 · G 0.4 · X 0.1 (raw 0.485)

**Backtest:** Team later shipped GH-6769 'Enable Jetpack Comments on Reader for Internal Aut' (closed 2017-10-24, sim 0.60).

**Evidence (6 signals):**
- `GH-2039` (gh_issue ) — Can't comment . Hello on my Blog I can't answer to comments with the Android App. It shows me "Answer not possible". With the browser it works. 

Here the error log from my phone. 

```
11-30 19:23:44.674 I/ActivityManager(3856): START u0 {
- `GH-1167` (gh_issue ) — Error 403 on Comment Details View for a Jetpack site. I see the following error when I open the comment detail view for a comment on eritreo.it/wp37 (Jetpacked site)

```
03-27 18:53:26.345: E/WordPress(8910): [2711] BasicNetwork.performReq
- `GH-4342` (gh_issue ) — Error 404 when replying to comments with device language set to Arabic or Farsi (Persian). ### Expected behavior

Users should be able to reply to comments (e.g. from the notifications comment detail view) no matter what device language the
- `R-00b6f637` (review ★2) — I'm not able to reply to comments on a self hosted site. It keeps saying """"""""""""""""reply failed"""""""""""""""".""
- `GH-382` (gh_issue ) — User can't reply to comment notifications via Jetpack and HTTPS. See: http://android.forums.wordpress.org/topic/comment-replies-fail-on-https-sites?replies=5

- `GH-3977` (gh_issue ) — Obscur error message when replying to a closed thread. ### Steps to reproduce the behavior
1. Go to the site Comments section
2. Select a comment from a closed thread
3. Try to reply and get a "Reply failed" toast

XMLRPC response is pretty

**Roadmap refs:** `GH-3276`, `GH-1654`, `GH-4933`, `GH-1553`, `GH-3418`

*Adversarial check:* The claim is that users want to reliably reply to, like, and comment on blog comments directly from the app—especially from notifications—on self‑hosted/Jetpack sites, without cryptic errors, and with clear behavior when threads are closed or permissions apply.

First, check whether this is just a noisy, generic complaint about comments, or a coherent product gap:
- GH-2039: "I can't answer to comments with the Android App. It shows me 'Answer not possible'. With the browser it works." This is not a vague UX gripe; it’s a clear app‑only failure on a core action (replying) that works on the web

### 5. Users need self‑hosted and regular account logins to "just work" reliably, without cryptic errors, repeated registration loops, IP/firewall blocks, or unexplained failures. When login does fail, they need clear, actionable feedback so they can fix the problem themselves instead of being locked out o  ·  **UNDER-PRIORITIZED**  ·  confidence **57%**

**Why a gap:** Multiple roadmap items directly touch login issues, including self‑hosted login bugs (GH-962, GH-1343) and improving failure messaging (GH-4762). However, the user signals show a broad, recurring, high‑pain pattern: users frequently cannot log in or stay logged in to self‑hosted sites, encounter vague errors, firewall/IP blocking, and repeated failed sign‑ins. The roadmap items are narrow, one‑off bug fixes or UX tweaks rather than a systematic, high‑priority effort to make self‑hosted login robust, diagnosable, and forgiving. Given the very high pain rate and only moderate explicit request ra

*Latent because:* This need is latent because users mostly express it as acute frustration with specific incidents ("can't log in," "error after first login," "blocks my IP," "always telling me error") rather than as a structured feature request like "please overhaul the self‑hosted login architecture." The pain is very high: 1‑ and 2‑star reviews, repeated attempts to log in, password resets, and even hosting/fire

**Confidence** = V 0.988 · D 0.667 · I 0.699 · K 0.717 · G 0.4 · X 0.043 (raw 0.639)

**Backtest:** Team later shipped GH-5843 'Not able to login to self hosted site account' (closed 2017-11-08, sim 0.55).

**Evidence (6 signals):**
- `R-7f0a2162` (review ★1) — Login Problem Not able to login by this app. Please fix it.
- `R-fb110b4a` (review ★1) — Software problem It's been two time since i had to register with same password and both the the times i was able to register.. got confirmation of registration .. but when i try to open it again with same link ot says""""""""""""""""email n
- `R-2c52cbd8` (review ★1) — Not working It just showing me error after I tried logging in for d first time
- `R-54f76e35` (review ★1) — Blocks my IP This app sets off my firewall each time I login - and causes my hosting to block my IP  even though it's my home IP.
- `R-bb78da17` (review ★1) — Frankie Ifop I can't log into my self-hosted site. Always telling me error plus application log.
- `GH-2012` (gh_issue ) — unable to login from China mainland. unable to login from China mainland, though setup  a vpn proxy. 


**Roadmap refs:** `GH-962`, `GH-1343`, `GH-4762`

*Adversarial check:* The evidence does point to a real login‑reliability problem, but we should be careful not to overgeneralize.

1) **Is this just generic “login is broken” noise?**  
Most apps get a steady trickle of 1★ reviews saying “can’t log in.” On its own, that’s often just user error, forgotten passwords, or transient outages. However, the pattern here is more specific:
- Repeated registration loops: user can register multiple times with the same password and gets confirmation, but then can’t log in with the same link (R-fb110b4a). That suggests a flow or state bug, not just user confusion.
- First‑time 
