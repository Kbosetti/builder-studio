Mitchell Homes | The Home Portrait
Source of the production deployment on Vercel, project mitchell-home-portrait-quiz, team cea-marketing.
Deployed September 3, 2026 by CEA Marketing. Live at https://mitchell-home-portrait-quiz-cea-marketing.vercel.app

Files
  index.html         redirects to /portrait
  portrait.html      the quiz
  fullportrait.html  the personalized presentation
  dashboard.html     the same domain lead board
  api/lead.js        Builder Studio intake (needs HBS_PIT and HBS_LOCATION_ID env vars on the project)
  package.json       nodemailer for the optional Gmail send
  vercel.json        clean URLs

All images load from the Mitchell media library. No dashes in any copy.
To redeploy from a machine: vercel --prod from this folder, linked to the project above.
