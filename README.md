# instamation
Automation for IG

# Currently 4 main functions
1. follow(url) - follow a single account
2. follow_all(url) - follow single account, scrape suggested accounts, follow suggested accounts
3. like_images(url) - likes random amount of images on single account
4. follow_and_like(url) - mixture of follow_all(url) and like_images(url)

# USAGE EXAMPLE
import instagram

x = instagram.start(username='user@email.com', password='password')
x.login()
x.follow('https://www.instagram.com/user_you_want_to_follow/')
