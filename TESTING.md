# -INVITATIONS- - Testing Information

[Live app deployed on Heroku](https://devtog-invitations.herokuapp.com/)

[Back to main README.md file](/README.md)

## Table of Contents
- [Software Tools](#software-tools)
- [User story testing](#user-story-testing)
- [Testing elements and functionality of the project](#testing-elements-and-functionality-of-the-project)
- [Additional Testing](#additional-testing)
- [Errors and Issues Found](#errors-and-issues-found)

## Software Tools
- [JSHint - Code Analysis Tool](https://jshint.com/) - used to help detect errors and potential problems in JavaScript code.
- [W3C - Markup Validation Service](https://validator.w3.org/) - used to check the markup validity of the rendered HTML.
- [W3C - CSS Validation Service](https://jigsaw.w3.org/css-validator/) - used to check the validity of the Cascading Style Sheets (CSS).
- [Flake8 within GitPod]() - used to check Python code base against coding style (PEP8)
- [Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools) - used to help check the responsiveness of the app and also use of Audits to test for performance, accessibility, best practices & SEO

## User story testing

### Customer
The [screenshots](/docs/customer_stories/) for the customer stories are in /docs/customer_stories/

1. How do I search for products using a word or phrase?
    1. From any page click the 'Magnifying Glass' icon on the navigation-bar.
    2. Enter your search word or phrase.
    3. Click the blue 'Magnifying Glass' on the search window.
    4. The search results will then be displayed.

2. How do I find invitations by category?
    1. From any page use the category links in the centre of the navigation-bar or in the 'hamburger' menu.
    2. Choose your main category, and then from the dropdown menu select a sub-category.
    3. The products in the chosen category will then be displayed.

3. How do I find newly listed products?
    1. From any page select 'ALL PRODUCTS' on the navigation-bar / hamburger-menu.
    2. From the dropdown menu choose 'New Products'
    3. The four most recent products will be displayed.

4. How do I find featured products?
    1. From any page select 'ALL PRODUCTS' on the navigation-bar / hamburger-menu.
    2. From the dropdown menu choose 'Featured Products'
    3. Any products tagged as featured will be displayed.

5. How can I view more details about a product?
    1. From any product search results display, click on the product you are interested in.
    2. The full product details will then be displayed

6. How do I add products to my shopping cart?
    1. From a products detail page, simply select the quantity you would like to purchase (limit per product is 99).
    2. Then click the [Add to Cart] button.
    3. A message will be displayed to confirm the quantity and product you have added to your shopping cart. You can close this message or it will disappear by itself.
    4. Repeat the above steps for any other products you would like to purchase.

7. How can I view/edit my shopping cart contents?
    1. From ny page click the shopping cart icon on the top-right of the navigation-bar.
    2. The shopping cart will now be displayed.
    3. To remove an item from the shopping cart click the 'Remove item' link on the product you wish to remove. A message will be displayed to confirm the item you have removed.
    4. To change the quantity of an item use the '-' and '+' icons and then click the [Update Cart] button. A message will be displayed to confirm the shopping cart has been updated. (please note if you set the quantity to zero for an item item will be removed)

8. How can I personalise an invite?
    1. Find the invite you would like to personalise and view it's product details.
    2. Now click on the [Personalise] button. (please note you cannot add an invite to your shopping cart until it has been personalised)
    3. The invite design layout will be displayed.
    4. To edit a layout element click on it's text.
    5. From here you can change the text, it's font style, size, color and stroke.
    6. You cannot change the position of the text, so you do have to be mindful when setting font sizes as text could overlap.
    7. When you are happy and done, click [Finish].
    8. The page will remind you that you have personalised this invite, but if you don't add it to your shopping cart now, the personalisation will be lost.
    9. [Add to Cart] button is now enabled, so just click it to add it to your shopping cart.
    10. Once in your shopping cart you can make any changes to the invite by clicking the [View/Edit] button of that invite.
    11. Your shopping cart will auto-update when you click [Finish] if you edit it.

9. How do I checkout and pay?
    1. To checkout and pay, first go to your shopping cart and check you have everything you need.
    2. Then click on the [Go to checkout] button.
    3. Now review your order and check everything is ok.
    4. Fill out the order form with your details, delivery address and card details.
    5. Finally click [Pay Now] and your payment will be processed by the payment processing company Stripe.
    6. If there are any issues/errors they will be displayed, once the payment has been processed a message will appear and an order confirmation will be displayed.

10. How can I view my previous orders?
    1. To view previous orders, you must place the order after you have logged-in.
    2. If you do not have a login yet then you first need to register an account.
    3. From the navigation-bar on any page click the 'User Profile' icon and select register.
    4. Enter your details and click [Sign Up].
    5. An page will be displayed asking you to check your emails and verify, once you have done this you can then log in.
    6. Now you can view the history of any orders you place, and you can also review products you have purchased.
    7. Assuming you have placed some orders, to view old orders click on the 'User Profile' icon in the navigation-bar and select 'My Profile'.
    8. From the 'Profile' display you can now see your previous orders.
    9. Clicking on an order will display a copy of the original order confirmation.

11. How do I update my profile information?
    1. Login to your account
    2. Click on the 'User Profile' icon in the navigation-bar and select 'My Profile'.
    3. From here you can update your user details, and click the [Update] button to save them.

12. How do I review a product I have purchased?
    1. Login to your account
    2. Click on the 'User Profile' icon in the navigation-bar and select 'My Profile'.
    3. From there select a previous order.
    4. Now click on the [Review Product] button of the item you want to review.
    5. Enter your comment and select a product rating from 1-5.
    6. Finally click the [Add Review] button.
    7. Your review will be added, a confirmation message displayed and you will be returned to the previous page.

13. How can I edit a review I have made?
    1. Login to your account
    2. Click on the 'User Profile' icon in the navigation-bar and select 'My Profile'.
    3. From there select a previous review.
    4. Make your changes and click the [Update Review] button.
    5. Your review will be updated, a confirmation message will be displayed and you will be returned to your 'User Profile'

14. How can I delete a review I have made?
    1. Login to your account
    2. Click on the 'User Profile' icon in the navigation-bar and select 'My Profile'.
    3. From there select a previous review.
    4. Tick the 'Delete review' checkbox and click [Update Review] button.
    5. You will then be prompted, if you are sure? Click [Ok] to delete it.
    6. Your review will be deleted, a confirmation message will be displayed and you will be returned to your 'User Profile'


### Administrator

For all the admin functions you will need to be logged-in as a super-user. At any point if you are not sure about something you should contact the support/development team before going any further.

1. How do I maintain the products?
    1. You can quickly edit a particular product by finding it in the store and clicking the red [Edit] button displayed in product search results or on product detail pages.
    2. Here you can edit the required information and click [Save] at the bottom of the screen or you can delete the product by clicking the [Delete] button.
    3. The 'CUSTOM DETAIL LINES' are used to set the layout of fields for customisable invites, other products don't need the. These fields generally are self-explanatory, the Y_POS field is approx. the number of pixels from the top of the raw_image to position the text, The name field should only contain letters, numbers or '_' '-'.
    4. The 'View image' is the image which all products require to display as a product.
    5. The 'Raw image' is only for invites and is used to create a customers final downloadable invite, these images must be (1748px x 2480px) currently the site only supports portrait invites.
    6. The 'Customize image' is only for invites and is used to allow the user to personalise the invite on-screen, these images are the same as the 'Raw image' but water-marked and sized to (437px x 620px).
    7. If you are adding an invite you must also tick the 'Customizable' checkbox and the images mentioned in points 5 & 6 are mandatory.

2. How do I maintain the order information?
    1. If you are already in the '-INVITATIONS- Administration' you can just click 'Orders' under the 'CHECKOUT' tab on the left-side of the window. If you are on the main site then first go to 'My Profile' and click on 'Site Management'.
    2. From here you can edit/delete existing orders and order lines and also add in a new order if required.(however no card processing will take place from here)

3. How do I maintain the FAQs?
    1. If you are already in the '-INVITATIONS- Administration' you can just click 'Faqs' under the 'FAQ' tab on the left-side of the window. If you are on the main site then first go to 'My Profile' and click on 'Site Management'.
    2. From here you can edit/delete existing 'FAQs' and also add in a new FAQ.
    3. The 'Display' field dictates how high up the screen a FAQ will appear, the lower the number the closer to the top.

4. How do I maintain the product reviews?
    1. If you are already in the '-INVITATIONS- Administration' you can just click 'Reviews' under the 'PRODUCTS' tab on the left-side of the window. If you are on the main site then first go to 'My Profile' and click on 'Site Management'.
    2. From here you can edit/delete existing 'Reviews' and also add in a new Review.

5. How do I maintain the product categories?
    1. If you are already in the '-INVITATIONS- Administration' you can just click 'Categories' under the 'PRODUCTS' tab on the left-side of the window. If you are on the main site then first go to 'My Profile' and click on 'Site Management'.
    2. From here you can edit/delete existing 'Categories' and also add in a new Category.
    3. Adding / Deleting a Category is not recommended without talking to the software developers first.

6. How do I maintain the user accounts?
    1. If you are already in the '-INVITATIONS- Administration' you can just click 'Users' under the 'AUTHENTICATION AND AUTHORIZATION' tab on the left-side of the window. If you are on the main site then first go to 'My Profile' and click on 'Site Management'.
    2. From here you can edit/delete existing 'Users' and also add in a new User.
    3. You may also need to access the 'Email Addresses' option under the 'ACCOUNTS' tab if there is an issue with a users email verification.


## Testing elements and functionality of the project
(manual tests)

### General
- Make sure that all app pages display as they should.
- Ensure that the logo and navigation display correctly on different device screen sizes.
- Check that all navigation and logo links are working.
- Check that the alt/title text appears on the logo image.
- Ensure that font sizes are readable on different devices.
- Check that footer social links are working.

### Home page
1. Check the search text input works and the [Search] button functions.
2. Check expected search results.

### About page
1. Check that the text displays correctly
2. Ensure that the DB stats are correct.

### Activities (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (All, Featured, Recently Added, Animals, Attraction, Crafting, Food, Nature, Sport and Leisure) give the expected results.

### Submit/Edit an Activity
1. Confirm all the input fields work as expected and the [Add Activity] button functions and displays processing indicator.
2. Confirm that an 'admin' user can edit any activity.
3. Check client and server side form validation is working as expected.
4. Check [x] link in the top-right allows the user to abort the submit/edit.

### Login/Register
1. Check the email and password input fields work and the [Login] button functions and a user can actually be logged-in.
2. Check the [Register] button takes the user to the 'User Registration'.
3. At 'User Registration' confirm all the input fields work as expected and the [Register] button functions.
4. Check that a user actually gets registered.
5. Check the 'HERE' to login link works.

### Profile (menu)
1. Check that the menu displays as it should on all devices.
2. Ensure each menu option (View Profile, My Favourites, Submitted by Me, Logout) give the user the expected results.

### Displayed Results (from Activities or Profile menu options)
1. Check that the results are displayed in the correct format depending on the screen size.
2. Has the correct flash message been displayed.
3. Ensure that the image and [More Details] button link to the full activity view.
4. Check that the [Edit] button only displays if the user originally submitted the activity or the current user is an admin/moderator.
5. Confirm that the correct data has been displayed.

### Activity View
1. Check that the results are displayed in the correct format depending on the screen size.
2. Ensure that the 'Add to Activity Favourites' heart-icon works as expected.
3. Check the alt/title text changes on the heart-icon.
4. Ensure activity links work and only appear if the data is present.
5. Are the activity flag-icons correct.
6. Check the 'creator' info at the bottom of the view.
7. Confirm that the correct data has been displayed.

## Additional Testing
1. Asked friends and family to use the application on their phone, tablets and desktops where possible and let me know any issues. Got good feedback, with no real issues.
2. I have tested the app on a desktop using the following modern browsers: Chrome, Firefox and Edge. As well as testing on Android phone/tablet and Apple iPhone.
3. The application has not been written to work on Internet Explorer. In the real World if a client wanted an application to work on IE then that is fine, but a lot of the newer methods of coding Javascript, etc does not work on IE. IE has had it's day and I wanted to code the app using some of these newer methods.

## Errors and Issues Found
(only includes main errors/issues rather than easy to solve coding, typos, alignment, etc which caused only minor errors)

1. **Uploaded images on Heroku**
As far as user images on this project, I did not realise that we could just use a link rather than getting the users to actually upload images. So I did go down the route of image uploads, cropping, resizing, etc.  This all worked well while testing on GitPod, however when I deployed the app to Heroku the images no longer appeared. Other than the tutor led course material I had never used Heroku before, so was a little puzzled but after some research I realized that while the image is actually uploaded to Heroku it doesn't actually store the image for very long.  I had a decision to make, undo all the effort and coding I had done for the images or spend time to find a solution. After further investigation I discovered AWS S3 Bucket was a place for my app to upload the images to and serve them back to the users.  This took more time than I thought, but I feel it was well worth it in the end.

2. **Image cropping/resizing**
When resizing images occasionally a landscape image being resized/cropped ends up with black bars either side of the image.  Due to time constraints I have not yet had time to solve this issue.

3. **Additional location value**
During testing and data entry it became obvious that we really needed an additional value for the 'location' field to deal with activities which were 'Out & About' but did not have a specific venue.  So, 'At a Venue' was added for activities with a specific address.

4. **https:// changing to http://**
While testing on Heroku I have noticed that while the site starts off on a  secure 'https://' url, as soon as you do an activity/view it changes to a 'http://' url. Even though at the base of the browser window it clearly says it is linking to a 'https://' url.  In 'heroku logs --tail' you can see the protocol change to 'http'.
Due to time constraints I have not had the time to investigate this further yet, but think this issue could be related to the fact that I haven't specifically added an SSL certificate to my Heroku Dyno or the fact that I am not using a paid Dyno.
Either way this issue would need to be solved before going fully live.

5. **Image file-input field**
On an actual Android mobile and tablet the 'file-input' filename still overflowed, but in Google Dev Tools it does not. Performed an update for Chrome on both devices and now it works as expected on the tablet but the mobile still has the issue, further investigation is required.