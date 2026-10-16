# CEA social rollout (CEA Marketing's own pages, not Mitchell)

Content lives on the approval page https://claude.ai/artifact/2sKyZNq1VHfUsHYxpcGVAq (captions in the `DATA` object of `index.html`, media under `media/`; download with the Artifact tool's read action and `paths`). Plan: https://claude.ai/artifact/1J6ZVefjxfZ3CbDACFjiAq.

## Kelly's call, October 12, 2026

Post and schedule through the **CEA sub-account in Home Builder Studio**, with every image and reel uploaded to that sub-account's media library. Not through Postiz going forward. Never through the Mitchell Homes location (`5o5zLlUPPizy6Ajp61oF`); the Homebuilder_Studio MCP connector only reaches Mitchell.

## Waiting on

- CEA sub-account Location ID (env var `CEA_GHL_LOCATION_ID`)
- CEA Private Integration Token with Social Planner and Media scopes (env var `CEA_GHL_PIT`), set in the Claude environment settings
- Instagram @ceamarketing, the CEA Facebook page, LinkedIn (Kelly plus the CEA page) and the CEA Google Business Profile connected in that sub-account's Social Planner

## Then

1. Upload every file in `schedule.json` to the CEA media library (`POST /medias/upload-file`).
2. Delete the 21 old drafts in the CEA Social Planner from October 7 so nothing doubles.
3. Schedule each row of `schedule.json` at 10am Eastern via `POST /social-media-posting/{locationId}/posts`. Facebook gets the blog URL in place of "link in bio".
4. Set up the "Comment AUDIT" automatic DM in that sub-account.

## Already posted (via Postiz, October 12)

Blog post 1 (How to Choose a Homebuilder Marketing Agency With Real AI Services) to the CEA Marketing Facebook page, Kelly's LinkedIn and Kelly's Instagram (Kelly Bosetti Primeau All About Marketing). It is not in `schedule.json`. Two files were test uploaded to the ceamarketing.com Webflow asset library (`cea-social-promo1.jpg`, `cea-social-reel1-bold-ideas.mp4`); they are not on any page.

## Content kit and Google posts (October 16)

The working library is the public content kit https://claude.ai/artifact/Ngw9yyaJKjBfSYaDSoNSNo: posts, 20 reels (8 to 20 cut from Kelly's Drive video library), 12 scripts, 6 emails and 8 Google Business Profile posts (one per article plus the free audit offer; 4:3 images, Learn more button, no hashtags). `schedule.json` now carries the Google posts twice a week at 11am Eastern. Only reels about being found online end with Comment AUDIT; the rest use the brand end card and a topic call to action.
