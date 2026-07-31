# 🔇 The Silent Stakeholder — org.wordpress.android

*Roadmap snapshot T0 = 2017-01-01 · generated 2026-07-31 11:04 UTC · mode openai:gpt-4.1-mini*

## The single most important unmet need
> **Users need a reliable, fast, and user-friendly way to upload multiple images or media files without failures, delays, or merging errors, including multi-select functionality and minimal loading steps — under-prioritized by the roadmap despite the evidence (50% confidence).**

## Ranked gaps

### 1. Users need a reliable, fast, and user-friendly way to upload multiple images or media files without failures, delays, or merging errors, including multi-select functionality and minimal loading steps.  ·  **UNDER-PRIORITIZED**  ·  confidence **50%**

**Why a gap:** The roadmap includes several items addressing media upload issues, such as bugs with multiple image uploads (GH-3445), allowing any file upload (GH-4842), and inability to upload posts with pictures (GH-375). However, many user complaints highlight persistent problems with upload failures, slow or repeated upload attempts, lack of multi-select for uploads, and merging of multiple photos into one file. While some bugs are closed, the high pain rate and ongoing user frustration suggest these issues are not fully resolved or prioritized at a high enough level to meet user needs effectively. Other

*Latent because:* Despite high pain and frequent complaints about media upload problems, explicit requests are relatively low, possibly because users have become resigned to the issues or do not expect improvements. This latent dissatisfaction signals a critical need that is not strongly voiced but significantly impacts user experience.

**Confidence** = V 1.0 · D 0.667 · I 0.434 · K 0.729 · G 0.4 · X 0.126 (raw 0.583)

**Backtest:** Team later shipped GH-5434 'Media browser fails to load images' (closed 2017-03-22, sim 0.57).

**Evidence (6 signals):**
- `R-d5ccafcd` (review ★1) — Disastrous Update Used to love this app but now just problem after problem. The whole thing is really clunky and seems to have a mind of its own Now pictures refuse to load. I'm not interested in doing anything fancy. I just want to be able
- `R-0a1edb96` (review ★1) — One problem Please we liked it when if we wanted to up load a photo it just comes up  now just to up upload a photo it now has to load which takes time. Pls we do not like the idea of our photos loading.
- `R-de632d51` (review ★1) — Upload fails Text or Image  nothing can be uploaded with this version. I will change my rating once it is fixed.
- `R-6500f1be` (review ★1) — Not Able To Upload Images and Not Able to Add Website What The Hell This App Does ????
- `R-310c35e4` (review ★1) — Garbage It would be worth 99 cents for an app that works. This one does. Totally unable to upload media. Why not build that feature in rather than just having the app sit and spin.
- `GH-1983` (gh_issue ) — Upload fails unless connected to a charger. If my mobile is not on a charger, upload will stall for hours (and never resumes). This happens 100% of the time, I can effectively only use the app while charging - but then why use the app?

Thi

**Roadmap refs:** `GH-3445`, `GH-4842`, `GH-375`

*Adversarial check:* The evidence strongly indicates frequent and severe user complaints about uploading multiple images or media files, including failures, delays, and usability issues. Multiple 1-star reviews explicitly mention upload failures, long loading times, and inability to upload media, which aligns closely with the claimed need. The latency score of 0.809 suggests this is a persistent issue, and although the max roadmap similarity is 0.623, it is not sufficiently high to confirm that the problem is fully addressed or prioritized. The confidence features show moderate to high relevance in some dimensions

### 2. Users need reliable and consistent text formatting behavior in the editor, including correct application and removal of formatting, preservation of formatting when typing or pasting, and proper handling of formatting tags.  ·  **UNDER-PRIORITIZED**  ·  confidence **48%**

**Why a gap:** The user need centers on issues with text formatting in the editor, such as formatting tags being misplaced, formatting lost after typing, and improper handling of pasted formatted text. The roadmap includes some related items addressing editor bugs and formatting around images or HTML escaping, but these do not comprehensively address the core formatting and editor behavior problems raised. The related items are mostly closed bugs or minor enhancements, indicating some attention but not a prioritized, broad fix for the formatting experience.

*Latent because:* Although users experience high pain from formatting issues, explicit requests are low likely because users may accept workarounds or consider these issues as minor annoyances rather than urgent feature requests, making the need latent despite its impact.

**Confidence** = V 0.388 · D 0.333 · I 0.45 · K 0.811 · G 0.7 · X 0.0 (raw 0.562)

**Backtest:** Team later shipped GH-5685 'Changes in HTML mode not saved' (closed 2017-04-21, sim 0.56).

**Evidence (6 signals):**
- `GH-3863` (gh_issue ) — Visual Editor: Formatting applied before typing is lost. ### Steps to reproduce the behavior

Open a new post.  Select formatting (bold, or italic).  Start typing.  The format button is deselected, and plain text is added.
### Expected beha
- `GH-4067` (gh_issue ) — Visual editor: Removed bold/italic formatting re-applies after removal in 5.4-RC-1. ### Expected behavior
1. Select bold or italic in visual editor
2. Type word(s) in formatted text
3. Select bold/italic again to clear selection
4. Press sp
- `GH-3865` (gh_issue ) — Visual Editor: Pasting formatted text into the title field yields HTML code. ### Steps to reproduce the behavior

Write, highlight, and copy formatted text.  Paste that text into the title bar of the post from the visual editor.  It appears
- `GH-3864` (gh_issue ) — Visual Editor: Pasting formatted text into the HTML editor pseudo-retains formatting. ### Steps to reproduce the behavior

Write formatted text, copy it to the clipboard, switch to the HTML editor, paste the text in.  It looks formatted, bu
- `GH-4963` (gh_issue ) — Removing bold/italic removes it from the previously applied word(s). ### Expected behavior
While writing a post, I apply bold or italic to a word. I move the cursor to the next position. Since bold(or italic) is still selected, it will be 
- `GH-491` (gh_issue ) — Editor: End tag can be set before starting tag. . In the editor tap to edit the content. 

Somewhere in the middle of the content, tap one of the formatting options.  I chose bold. 
Notice the opening bold tag is set, and the bold option is

**Roadmap refs:** `GH-138`, `GH-721`, `GH-450`

*Adversarial check:* The evidence consists of multiple distinct user reports describing inconsistent and unreliable text formatting behavior in the editor, such as formatting being lost when typing, formatting reapplying after removal, and improper handling of pasted formatted text. These issues are documented in recent GitHub issues with detailed reproduction steps, indicating they are not isolated or sarcastic complaints. The maximum roadmap similarity score of 0.612 suggests that while some related work may be planned, the problem is not fully addressed or prioritized. The confidence features show moderate to h

### 3. Users need a reliable and user-friendly media library experience within the post editor, including the ability to search images by name, see recently uploaded images immediately, prevent images from disappearing, and have videos visible in the media library.  ·  **UNDER-PRIORITIZED**  ·  confidence **45%**

**Why a gap:** The roadmap includes several closed issues addressing bugs related to media library image display and handling in the post editor, such as missing thumbnails, broken images, and loading status. However, many user signals highlight ongoing problems like inability to search images by name, images disappearing after upload, media library not updating automatically, blank images, and missing videos in the media library. These issues indicate broader and more persistent usability problems that are not fully addressed or prioritized in the roadmap, which mostly focuses on bug fixes rather than featu

*Latent because:* Although users experience high pain from media library issues (e.g., images disappearing, no search, missing videos), explicit requests for these features or fixes are low, possibly because users have adapted workarounds or do not expect these capabilities, making the need latent despite its impact on usability.

**Confidence** = V 0.438 · D 0.667 · I 0.375 · K 0.75 · G 0.5 · X 0.0 (raw 0.531)

**Backtest:** Team later shipped GH-6955 'Editor: Media picker allows adding videos to galle' (closed 2017-12-20, sim 0.66).

**Evidence (6 signals):**
- `GH-4593` (gh_issue ) — No videos in media library when trying to add to a post. ### Expected behavior

When using the `Select from media library" media option in the post editor, I'd expect to see videos there as well if library has some.
### Actual behavior

Onl
- `R-b5b7369c` (review ★2) — Does not update automatically Like when I added an image from my desktop computer and make a post using this app adding the image on the post  the recently uploaded image does not display. I have to go back to home  click on media and refre
- `GH-4363` (gh_issue ) — Media: Media library does not load media for sites with basic HTTP auth. ### Expected behavior

I expect to be able to view media in the site's media library (My Site > Media or in the Editor > Add media > Select from media library).
### Ac
- `GH-1314` (gh_issue ) — Disappearing images in post editor after activity is closed. 1. Enable `Don't keep activities` option in device settings.
2. Open app, tap new post button.
3. Add an image from the device gallery. Observe it is added to the post.
4. Add ano
- `GH-3321` (gh_issue ) — Media Library: Image disappears from view shortly after upload - 4.6-rc-3. When uploading a picture to the media library I see it show up in the view momentarily, and then it disappears.  After leaving and going back in it shows up just fin
- `GH-2456` (gh_issue ) — Featured images not working when selected from WP Media Library. 1. Create a new post with the app.
2. Tap the image icon and choose “Select from media library” or choose an image from the "Site images" tab with the media picker (for 3.9+)


**Roadmap refs:** `GH-1317`, `GH-503`, `GH-230`

*Adversarial check:* The evidence consistently highlights multiple user complaints about the media library experience within the post editor, including missing videos, disappearing images, and lack of immediate update for recently uploaded images. These issues are reported across different tickets without indication that they are resolved or planned imminently, and the maximum roadmap similarity score of 0.691 suggests partial but incomplete alignment with current priorities. The confidence features show moderate to low confidence in existing features addressing these needs. While some complaints might be isolated
