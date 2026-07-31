# 🔇 The Silent Stakeholder — org.wordpress.android

*Roadmap snapshot T0 = 2017-01-01 · generated 2026-07-31 16:12 UTC · mode openai:gpt-5.1*

## The single most important unmet need
> **Users need publishing to be rock‑solid: when they tap Post/Update, their content must reliably publish or update without cryptic errors (403 forbidden, generic post update errors, silent failures), including on self‑hosted sites and after app updates. They want to be able to write and then confident — under-prioritized by the roadmap despite the evidence (71% confidence).**

## Ranked gaps

### 1. Users need publishing to be rock‑solid: when they tap Post/Update, their content must reliably publish or update without cryptic errors (403 forbidden, generic post update errors, silent failures), including on self‑hosted sites and after app updates. They want to be able to write and then confident  ·  **UNDER-PRIORITIZED**  ·  confidence **71%**

**Why a gap:** User signals are about a core, blocking failure to publish or update posts (403 forbidden on self‑hosted, generic post update errors, repeated failures after app updates). The nearest roadmap items only tangentially touch posting: GH-1296 is about clarifying insufficient privileges (permissions/roles UX), and GH-862 is an old, generic bug about losing posts on upload. Neither addresses the recurring, systemic inability to publish (especially 403s and post‑update regressions) as a first‑class reliability problem. There is no roadmap item that explicitly targets robust, end‑to‑end post publishin [Reclassified UNDER-PRIORITIZED by the backtest: absent from the T0 roadmap, but the team closed a matching issue post-T0.]

*Latent because:* The pain is very high because publishing is the core job‑to‑be‑done; when it fails, the entire app is useless (“can’t post since morning”, “always failed on posting”, “it does not let me post my articles”). Users express this as frustration with specific errors or with the latest update, not as a structured feature request like “please improve the reliability of the publishing pipeline” or “add be

**Confidence** = V 0.897 · D 0.667 · I 0.499 · K 0.737 · G 0.75 · X 0.079 (raw 0.708)

**Backtest:** Team later closed a matching issue GH-8300 'Blog Posts List Shows Error Message When Publishin' (2018-09-19, sim 0.58).

**Evidence (6 signals):**
- `R-b4de1674` (review ★1) — Error I cannot able to get access to my self hosted website. Error shown that could not update data at this time. When I'm publishing a post a 403 error forbidden
- `R-3f8a8eeb` (review ★1) — Can't log in after I updated my WordPress application. I can't log in again since updated my WordPress application. I hate this  can't post since morning.
- `R-8eb07a04` (review ★1) — Can't publish blog post Blog post is saved as draft but won't publish. I clicked publish multiple times and it notifies me that the post is published however I can't see it when visiting my blog site. Gets really frustrating
- `R-e078e696` (review ★1) — I can't post on my website it always left a draft what should i do ?
- `GH-1230` (gh_issue ) — XML-RPC error 405 on self-hosted blog. Hello.  Since I updated the app to the latest version, I can no longer post content to my self-hosted WP blog. The error message says that XML-RPC services are disabled on this host.  The blog configur
- `T-92811096` (ticket ) — Digital Assistance. The digital campaign occasionally fails to upload content, which might be caused by server timeout issues. Troubleshooting steps include restarting systems and verifying network connections to ensure stability and perfor

**Roadmap refs:** `GH-1296`, `GH-862`

*Adversarial check:* The evidence does point to a real reliability problem around publishing, but we should be careful not to overstate it as some newly discovered, deeply latent need.

1. **This is a very basic, explicit expectation, not a subtle latent need.**
   Users expecting “when I tap Post, it actually posts” is table‑stakes for any publishing app. The complaints are direct and literal:
   - “Error shown that could not update data at this time. When I'm publishing a post a 403 error forbidden”
   - “Can't log in after I updated my WordPress application. I hate this can't post since morning.”
   - “Blog pos

### 2. “When I add a video to my post—whether via Quick Video, from my gallery, or newly captured—it should upload successfully, stay attached to the post, and be visible to my viewers. I shouldn’t see constant upload errors, end up with empty posts, or publish a post that looks fine in the app but has no   ·  **UNDER-PRIORITIZED**  ·  confidence **67%**

**Why a gap:** The user need is about reliably getting videos into posts and having them actually appear for viewers: uploads fail with errors, posts publish without the video, quick video posts end up empty, and error messages are confusing or misleading. The roadmap items nearby are mostly tangential: GH-250 is about a specific VideoPress alert, GH-603 about using a shortcode when sharing a video, GH-375 and GH-503 are image‑related, and GH-4579 is about YouTube iframe previews. None of these represent a coherent, prioritized effort to make video upload and publishing robust and understandable end‑to‑end.  [Reclassified UNDER-PRIORITIZED by the backtest: absent from the T0 roadmap, but the team closed a matching issue post-T0.]

*Latent because:* This need is highly painful (videos not uploading or disappearing undermines entire posts and frustrates both authors and viewers) but only weakly expressed as a single, clear feature request. Users describe symptoms—“videos won’t upload,” “error every time,” “viewers can’t see my videos,” “posts are empty,” “invalid file type,” “post uploaded without the video”—rather than articulating a unified 

**Confidence** = V 0.459 · D 0.667 · I 0.533 · K 0.767 · G 0.8 · X 0.0 (raw 0.667)

**Backtest:** Team later closed a matching issue GH-6654 'Async media: broken reattachment identification' (2017-09-22, sim 0.63).

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

*Adversarial check:* The claimed gap is that adding a video to a post should reliably result in a published post where the video is actually present and viewable, without confusing errors or silent failures. The evidence set is fairly consistent with that, and it’s not easily dismissed as mere noise or sarcasm.

1. **Is this just a frequent, generic complaint?**  
The 1‑star reviews are broad but specific about video:
- R-a293a934: “Videos won't upload…” is bundled with other glitches, but video upload failure is explicitly called out as a pain point.
- R-3327b693: “always error when uploading videos… every time” 

### 3. “I just want to be able to create an account (and new blog) without mysterious errors. When something goes wrong, tell me clearly what the problem is and how to fix it, instead of failing silently or with a generic message that leaves me stuck.”  ·  **UNDER-PRIORITIZED**  ·  confidence **65%**

**Why a gap:** The user need is about reliably creating a new account (and/or new blog) without opaque or blocking errors, especially in normal conditions. The sample signals show users often cannot create an account at all, see generic or misleading errors, and are left stuck (“not make a account”, “error occurred… not telling what’s the error”, invalid_client, silent partial creation). The nearest roadmap items are narrow, one-off bugs: a bad password error after creation (GH-970), a crash on account creation (GH-1469), a crash on slow connection (GH-688), and a wait-indicator UI glitch (GH-715). These add [Reclassified UNDER-PRIORITIZED by the backtest: absent from the T0 roadmap, but the team closed a matching issue post-T0.]

*Latent because:* This need is latent because users mostly express raw frustration (“Bad… not make a account”, “Cant able create account showing error”) rather than a structured feature request like “please overhaul the signup flow and error handling.” The pain is extremely high: account creation is a gateway action, and when it fails, users are completely blocked from using the product, reflected in 1–2 star revie

**Confidence** = V 0.388 · D 0.667 · I 0.733 · K 0.793 · G 0.7 · X 0.0 (raw 0.652)

**Backtest:** Team later closed a matching issue GH-8460 'Better Error Messaging for Invalid URLs' (2019-04-17, sim 0.51).

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

*Adversarial check:* The core claimed gap is: account/blog creation frequently fails with unclear or misleading error handling, leaving users stuck.

1. **Is this just a frequent, surface-level complaint?**  
The evidence is tightly clustered around the same flow and the same failure mode:
- R-4ba6b4ec (1★): "not make a account" – generic but clearly about account creation failure.
- R-48acd729 (1★): "Cant able create account showing error" – again, account creation failing.
- R-76f42d19 (2★): explicitly calls out that an error occurs during account creation *and* that the app "not telling whats the error".

These

### 4. Users need the app to reliably load, refresh, and display their blog posts inside the app over time—without intermittent failures, vague connection errors, or crashes—so that they can actually read and manage their blogs on mobile instead of being forced into an external browser or uninstalling the   ·  **UNDER-PRIORITIZED**  ·  confidence **64%**

**Why a gap:** User reports consistently describe a core failure to view or refresh blog posts after initial use: posts lists not loading, connection errors, crashes on Android 7, and the app becoming effectively unusable for reading or managing posts. The nearest roadmap items are individual, narrow bugs: role-based weirdness (GH-3418), a specific AuthenticatedWebView failure (GH-1751), an NPE in PostsListAdapter (GH-3370), list not updating after delete (GH-181), and live site view breaking with plain permalinks (GH-4873). These address isolated technical defects but do not frame or prioritize the broader, [Reclassified UNDER-PRIORITIZED by the backtest: absent from the T0 roadmap, but the team closed a matching issue post-T0.]

*Latent because:* The pain is very high because this is a fundamental use case: if posts don’t load or refresh, the app fails at its primary purpose. Users express this through 1–2 star reviews, uninstalls, and phrases like “pointless having app,” “I cannot operate this,” and “Just plain doesn’t work.” However, explicit feature-style requests are low: users rarely say “please improve post list reliability” or “add 

**Confidence** = V 0.754 · D 0.333 · I 0.57 · K 0.714 · G 0.75 · X 0.07 (raw 0.638)

**Backtest:** Team later closed a matching issue GH-8384 'Pull to refresh does not work on Blog Posts page i' (2018-10-04, sim 0.63).

**Evidence (6 signals):**
- `R-239bff1f` (review ★1) — Just plain doesn't work 'Posts couldn't be refreshed at this time'. No error message  no indication of what the problem is. Uninstalled.
- `R-d469928d` (review ★1) — Disappointing It works really fine whenever I newly install it but after that it doesn't refresh the content and all other stuff anymore
- `R-44ea902e` (review ★1) — Not working
- `R-9264cbca` (review ★1) — Does the website and app has a problem today? Yesterday I was still editing so many stuff on my blog. But roday I can't even open the website! The app doesn't even work properly. pls send me a feedback on what's happening. :(
- `R-d493b2a7` (review ★1) — Lost my posts!! :'( Today morning when checked it it says nothing found!!! All my posts pages cmnts tags everythng is gone. Soo broke 💔💔
- `GH-905` (gh_issue ) — ArrayIndexOutOfBoundsException in notification settings. - Open the preferences view.
- Enter to the “Show/hide WordPress.com blogs” view. Go back.
- Enter to the “Manage notifications”, go the Blogs section and try to check/uncheck any of 

**Roadmap refs:** `GH-3418`, `GH-1751`, `GH-3370`, `GH-181`, `GH-4873`

*Adversarial check:* The claimed gap is that users need the app to reliably load, refresh, and display their blog posts over time, without intermittent failures, vague connection errors, or crashes, so they can actually read/manage blogs on mobile instead of being forced into a browser or uninstalling.

Trying to knock this down:

1. **Could this just be generic "app is buggy" complaining?**  
   The reviews are all 1-star and all about core content not loading or disappearing:
   - "Posts couldn't be refreshed at this time" with no explanation, leading to uninstall.
   - Works only right after install, then "does

### 5. Users want the comments experience to be easy to navigate and read, especially in long threads: they need a way to jump to the latest comments without endless scrolling, keep their place and selected comment when the list refreshes, have the view scroll to a sensible position (e.g., top of the comme  ·  **MISUNDERSTOOD**  ·  confidence **50%**

**Why a gap:** The roadmap clearly invests in the technical stability and mechanics of the comments feature (crashes, rotation bugs, list performance, infinite scroll, and even a broader 'rewrite comments'). However, the core user need expressed in the samples is about *navigating and viewing comments in a usable way*—quickly reaching the latest comments, preserving context/selection when refreshing, sensible scrolling behavior when replying, and making links usable. The roadmap items focus on backend/structural fixes and generic list improvements rather than the specific UX flows that are causing pain. For 

*Latent because:* This need is latent because users mostly complain about specific annoyances (having to scroll through 500+ comments, losing their place after refresh, odd scrolling when replying, links not clickable) rather than explicitly asking for a redesigned comment navigation system. The pain is high—people are frustrated enough to describe the experience as tedious and to report multiple edge-case bugs—but

**Confidence** = V 0.597 · D 0.333 · I 0.389 · K 0.739 · G 0.45 · X 0.0 (raw 0.496)

**Backtest:** Team later closed a matching issue GH-6717 'Crash selecting multiple comments' (2017-10-18, sim 0.66).

**Evidence (6 signals):**
- `GH-526` (gh_issue ) — Crash in CommentDetailFragment. I was in the notification list, and tapped on a comment and then immediately pressed the back button.

```
12-18 07:18:50.947      558-558/? E/AndroidRuntime﹕ FATAL EXCEPTION: main
    Process: org.wordpress.
- `GH-747` (gh_issue ) — NPE in comment list fragment. Found while monkey testing the app:

<pre><code>
// java.lang.RuntimeException: An error occured while executing doInBackground()
//  at android.os.AsyncTask$3.done(AsyncTask.java:299)
//  at java.util.concurre
- `GH-453` (gh_issue ) — CommentListFragment's ViewSwitcher should be revisited. During development for Issue #333 I had to contend with the following:

(Note: I removed the crashes when working on #333 but the behaviors are still broken)

The mechanism for display
- `GH-1617` (gh_issue ) — Reader loses place in comment adapter. From @aerych: "when i scroll the comment list, and it loads more comments, when it refreshes the list the scroll position changes and I've lost my place."

- `GH-660` (gh_issue ) — Comment detail doesn't show URLs as links. ![device-2014-01-09-081357](https://f.cloud.github.com/assets/3903757/1877841/08a117ba-7930-11e3-8f08-3f4a49c55627.png)

- `R-99018386` (review ★3) — Comments There needs to be a way for us to get to the latest comments. I'm of scrolling down 500+ comments after I close the app!!! 😬 めんどくせえええ!!! P.S. I meant the comments on a blog I follow. There should be a tab that allows me to skip to 

**Roadmap refs:** `GH-754`, `GH-770`, `GH-1447`, `GH-1681`, `GH-757`

*Adversarial check:* The claimed need is: better navigability and readability in long comment threads (jump to latest, preserve scroll position/selection on refresh, sensible scroll positioning). The verdict given is MISUNDERSTOOD, so we need to see if this is really just a misread of other issues (e.g., crashes) or if there is a genuine UX/navigation gap.

1. **Evidence breakdown**
- GH-526, GH-747: crash reports in CommentDetailFragment / comment list fragment. These are stability issues, not UX requests. They don’t support the specific need, but they also don’t contradict it; they’re just orthogonal.
- GH-453: 
