# CEA social rollout (CEA Marketing's own pages, not Mitchell)

Content lives on the approval page https://claude.ai/artifact/2sKyZNq1VHfUsHYxpcGVAq (captions in the `DATA` object of `index.html`, media under `media/`; download with the Artifact tool's read action and `paths`). Plan: https://claude.ai/artifact/1J6ZVefjxfZ3CbDACFjiAq.

## Kelly's call, October 12, 2026

Post and schedule through the **CEA sub-account in Home Builder Studio**, with every image and reel uploaded to that sub-account's media library. Not through Postiz going forward. Never through the Mitchell Homes location (`5o5zLlUPPizy6Ajp61oF`); the Homebuilder_Studio MCP connector only reaches Mitchell.

## Waiting on

- Nothing on access: the CEA key and location arrived October 13, and on October 14 Social Planner showed Facebook (CEA Marketing), Instagram (ceamarketing and kellyprimeauconsulting) and LinkedIn (the CEA page and Kelly) active. Google profiles and YouTube there are expired.
- Kelly's go ahead on new dates, since the schedule started October 13
- The CEA Google Business Profile reconnected in Social Planner (expired as of October 14) before the Google posts in `schedule.json` can go out

## Then

1. Done October 14: all 30 files (7 reels, 18 graphics, 5 carousel slides) are in the CEA media library as `CEA social · <file>`; URLs and file IDs in `uploaded.json`. Keys: `GHL_PIT_CEA` and `GHL_LOCATION_CEA` (see CLAUDE.md).
2. Done October 14: deleted all 22 old October 7 drafts in the CEA Social Planner (one post had been saved twice). Zero drafts remain.
3. Schedule each row of `schedule.json` at 10am Eastern via `POST /social-media-posting/{locationId}/posts`. Facebook gets the blog URL in place of "link in bio".
4. Set up the "Comment AUDIT" automatic DM in that sub-account.

## Already posted (via Postiz, October 12)

Blog post 1 (How to Choose a Homebuilder Marketing Agency With Real AI Services) to the CEA Marketing Facebook page, Kelly's LinkedIn and Kelly's Instagram (Kelly Bosetti Primeau All About Marketing). It is not in `schedule.json`. Two files were test uploaded to the ceamarketing.com Webflow asset library (`cea-social-promo1.jpg`, `cea-social-reel1-bold-ideas.mp4`); they are not on any page.

## Emails and the rest of the media (October 14)

- The six CEA emails (blog newsletter plus the five email AI Visibility Audit nurture: day 0, 2, 5, 9, 14) are drafts in the CEA sub-account folder "Fall 2026 | CEA emails (drafts, do not send until approved)" as `CEA26 · ID · subject`, from Kelly Bosetti Primeau. HTML in `emails/`, loader `upload_emails.py` (reruns update in place), IDs in `emails_created.json`.
- The blog images, promo1 and the CEA logo joined the media library too, 39 files in all (`uploaded.json`).
- CEA contacts on October 14: 13,574 total, 13,184 with an email. Builder role tags: sales managers 1,230, division managers 1,072, marketing managers 644, corporate leaders 387, top executives 355 (tags can overlap). Realtor tags: Clearwater 2,365, Palm Harbor 584, Dunedin 130, Safety Harbor 22. Also home list 444, IBS 2026 153, CEA customers 142, coaches 112, MQL leads 112. About 2% of a 9,600 contact sample were unsubscribed or on do not disturb.

## YouTube (Kelly's call, October 14)

The seven reels stay on Instagram and Facebook only. They are too busy for YouTube. The CEA YouTube channel is for Kelly talking to camera; nothing from `schedule.json` goes there. The channel is also expired in the CEA Social Planner and needs reconnecting before anything posts.

Kelly will share talking head videos she has already made, to sprinkle into the calendar, and will record new ones. Those are the YouTube content.

## Content kit and Google posts (October 16)

The working library is the public content kit https://claude.ai/artifact/Ngw9yyaJKjBfSYaDSoNSNo: posts, 20 reels (8 to 20 cut from Kelly's Drive video library), 12 scripts, 6 emails and 8 Google Business Profile posts (one per article plus the free audit offer; 4:3 images, Learn more button, no hashtags). `schedule.json` now carries the Google posts twice a week at 11am Eastern. Only reels about being found online end with Comment AUDIT; the rest use the brand end card and a topic call to action.
