# -INVITATIONS- - Testing Information

[Live app deployed on Heroku](https://devtog-invitations.herokuapp.com/)

[Back to main README.md file](/README.md)

## Table of Contents
- [Software Tools](#software-tools)
- [User story testing](#user-story-testing)
- [Customer - user story testing](#customer)
- [Administrator - user story testing](#administrator)
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
- Check that footer links are working and the information pages display correctly.
- Check that the alt/title text appears on the logo image.
- Ensure that font sizes are readable on different devices.
- Check that footer social links are working.
- Make sure user messages are displaying when & where they should.
- Check all pages display properly on different screen sizes.

### Home page
1. Check the [Shop Now] button link.
2. Check hero-image displays correctly.

### Text Search
1. Check that the text search is working as expected.
2. Check the [X] button closes the search.
3. Check the clear text button works.

### Product Search Results
1. Check that the title is correct for different categories and search options.
2. Ensure we get the expected search results.
3. Make sure the products display correctly on different devices.
4. Check the [Edit] button works as expected.
5. Make sure the 'Category' link displays products from same category.
6. Check the 'page-top' arrow icon on the right-side is working.

### Product Details
1. Check that all product details are correctly displayed.
2. Make sure the quantity buttons and [Update Cart] button work as expected

### Shopping Cart
1. Check that the cart is displaying correctly on different screen sizes.
2. Confirm all buttons and inputs are working correctly and as expected.
3. Double-check that values are correct.

### Checkout
1. Check that the checkout is displaying correctly on different screen sizes.
2. Confirm all buttons and inputs are working correctly and as expected.
3. Double-check that values are correct.
4. Ensure the form is working as expected.
5. Check that order confirmation is correct.
6. Confirm that user emails for confirmation and download links have been received and are formatted as expected.
7. Check the database has been updated with the order/user information.

### Login/Register
1. Confirm all buttons and inputs are working correctly and as expected.
2. Check that new a user can register, confirm and login.
3. Check the database has been updated with user information.

### Profile
1. Confirm all buttons and inputs are working correctly and as expected.
2. Check order history and reviews are showing the correct data.

### Reviews
1. Confirm all buttons and inputs are working correctly and as expected.
2. Check the database to make sure any changes the user makes are updated.

## Additional Testing
1. Asked friends and family to use the application on their phone, tablets and desktops where possible and let me know any issues. Got good feedback, with no real issues.
2. I have tested the app on a desktop using the following modern browsers: Chrome, Firefox and Edge. As well as testing on Android phone/tablet and Apple iPhone.
3. The application has not been written to work on Internet Explorer. In the real World if a client wanted an application to work on IE then that is fine, but a lot of the newer methods of coding Javascript, etc does not work on IE. IE has had it's day and I wanted to code the app using some of these newer methods.

## Errors and Issues Found
(only includes main errors/issues rather than easy to solve coding, typos, alignment, etc which caused only minor errors)

**Generating Invite Images after deployment**

Before deployment, generating the invites was perfectly fine, I always had a feeling that there would be a little issue to sort once deployed, but it wasn't so little.  Once all the storage was being handled by the 'S3 Bucket' generating invites didn't work! 

At first it could find the 'Raw' image file, solved that, but then the problem was deeper, it couldn't load the fonts.  Found a way to temporary by-pass the font issue with a default system font, that way I could crack on to getting it to save the invite. However the existing save method which worked fine in development on GitPod just didn't work. 

After much searching, eventually I found a different way of saving the image file using 'default_storage' imported from 'django.core.files.storage', which after reading seemed a very logical/django way of doing it.  I applied this method into my code and it worked, and then once applied to the font issue as well I could then correctly generate the invites! The stackoverflow answer I found was by 'minism' and is shown below:

[Django - Getting PIL Image save method to work with Amazon s3boto Storage](https://stackoverflow.com/questions/14680323/django-getting-pil-image-save-method-to-work-with-amazon-s3boto-storage)

<br>

**Personalising Invites on very small device screens**

Personalising invites works ok on all screens sizes apart from really small 320px wide screens.  Functionality wise it works fine but some of the fields push down the screen and don't align correctly.  However the final version emailed to a customer is properly aligned.
I still need to resolve this but just don't have the time before project sub-mission.

