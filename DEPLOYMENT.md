# -INVITATIONS- - Deployment Information

[Live app deployed on Heroku](https://devtog-invitations.herokuapp.com/)

[Back to main README.md file](/README.md)

## Table of Contents
- [Running this project locally](#running-this-project-locally)
- [Deploying to Heroku](#deploying-to-heroku)

## Running this project locally
This app has been built using the GitPod IDE and GitHub for version control.

### The following is required:
- Github account
- Python (version 3.8)
- [Stripe](https://www.stripe.com) - for card payment processing
- [Amazon S3 Bucket](https://aws.amazon.com/s3/) account - for image storage and access (only for deployment)
- [Heroku](https://signup.heroku.com/) account (only for deployment)

### Clone the repository
1. Login to GitHub.
2. Navigate to the projects repository “milestone-4-INVITATIONS”
3. Click Clone or Download under the repository name.
4. To clone the repository using HTTPS, under “Clone with HTTPS”, click the [copy to clipboard] icon next to the URL field.
5. Open Git Bash on your local IDE.
6. Change the current working directory to the location where you want the cloned directory to be made.
7. Type ‘git clone’ and then paste the URL from the step above.
  ```
      git clone https://github.com/username/repository
  ```
8. Press Enter. Your clone will now be created.

For more information and troubleshooting on cloning a repository from GitHub click [here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

### Install the Requirements
1. Go to the workspace for your local copy.
2. In a terminal window enter
  ```
    pip3 install -r requirements.txt
  ```

### Setup local environment variables in your for development IDE

| Key | Value |
  | --- | ---- |
  | SECRET_KEY | <your_secret_key_here> |
  | STRIPE_SECRET_KEY | <your_stripe_secret_key> testing key! |
  | STRIPE_WEBHOOK_SECRET | <your_stripe_webhook_secret> |
  | DEVELOPMENT | True |

Documentation on getting your Stripe keys is available when you sign-up for your free Stripe account.

### Other settings required

In the settings.py file update the DEV_BASE_URL setting to reflect your own local testing URL.

### Running the app

Run the App
- Open a terminal window in your IDE
- Type in:
  ```
  python3 manage.py runserver
  ```

## Deploying to Heroku
Use the steps below to deploy this app on Heroku:

### Setup Heroku
1. Create a Heroku account
2. Create a new app and select your local region
3. Next on the 'Resources' tab provision a new Postgres database
4. In Add-ons, type 'Postgres' and choose 'Heroku Postgres'
5. Click [Submit Order Form]
6. Setup the environment variables in  Heroku

### Add Heroku environment variables
1. Go to your Heroku account and select your app.
2. From the app menu select 'Settings'.
3. Click [Reveal Config Vars] to show the keys and the values.
4. Set the keys and values as below, replacing the <> entries with your values:

  | Key | Value |
  | --- | ---- |
  | DATABASE_URL | <your_database_url> from when you setup Postgres earlier |
  | STRIPE_SECRET_KEY | <your_stripe_secret_key> |
  | STRIPE_WEBHOOK_SECRET | <your_stripe_webhook_secret> |
  | AWS_ACCESS_KEY_ID | <your_aws_access_key_id_here> |
  | AWS_SECRET_ACCESS_KEY | <your_aws_secret_access_key_here> |
<br>

### Setup databases
1. Stop the server, if running (ctrl-c).
2. Temporarily delete the 'DEVELOPMENT' environment variable.
3. Run the migrations
- Open a terminal window in your IDE
- Stop the server, if running (ctrl-c)
- Run the migrations
- Type in:
  ```
  python3 manage.py showmigrations
  ```
- then if no issues
- Type in:
  ```
  python3 manage.py migrate
  ```

### Configure Heroku
1. At the terminal login to heroku and temporarily disable collect static
```
heroku login -i
heroku config:set DISABLE_COLLECTSTATIC=1 --app <your_app_name_here>
```
2. In settings.py edit the ALLOWED_HOSTS and add the hostname of your Heroku app i.e. ALLOWED_HOSTS = ['<your_app_name_here></your_app_name_here>.herokuapp.com', 'localhost']
3. Add heroku as git remote if you used dashboard to create the Heroku App and push to heroku:
```
heroku git:remote -a <your_app_name_here>
git push heroku master
```
4. In Heroku go to your app and select 'Deploy'
5. On the 'Deployment method' set it to 'Connect to GitHub'
6. In 'Connect to Git Hub, search for your repository and click [Connect]
7. In 'Automatic deploys'  click [Enable Automatic Deploys] 
8. Push to Heroku
```
git add .
git commit -m
git push
```
9. Check Heroku activity, to see build progress.


### Create AWS S3 Image Bucket
1. Login to your AWS Console.
2. From 'All services' select 'Storage' then 'S3'.
3. Create a new S3 bucket for image storage, choose local region.
4. Click the bucket you created.
5. In the list of 'Buckets' Click the new bucket you just created.								
6. On the properties tab, go to Static website hosting and click [Edit]							
7. Click 'Enable'							
8. Choose 'Host a static website' for the Index and Error document just enter default values as we won't use them.
9. Click [Save changes]							
10. On the 'Permissions' tab, under 'Cross-origin resource sharing (CORS)' click [Edit] and copy in the entry below, and click [Save Changes]
```
"[
  {
      ""AllowedHeaders"": [
          ""Authorization""
      ],
      ""AllowedMethods"": [
          ""GET""
      ],
      ""AllowedOrigins"": [
          ""*""
      ],
      ""ExposeHeaders"": []
  }
]"
```						
11.	Under 'Bucket policy' click [Edit]							
12.	Click on policy generator						
13. Set 'Select Type of Policy' to 'S3 Bucket Policy'						
14. Set 'Effect' to Allow						
15. Allow all principals by setting 'Principal' to *						
16.	Set Actions to 'Get Object'						
17. Copy ARN (Amazon Resource Name) from the other browser tab.						
18. Click [Add statement], then click [Generate Policy]						
19. Copy the policy shown.						
20. Go to the other browser tab and paste into the Bucket policy.						
21. Before saving add  /*  onto the end of the "Resource" ARN value. Now click [Save changes]						
22. Go to the 'Access Control List' and click [Edit]							
23. Under 'Everyone (public access)' select the 'List' option						
24. Tick the 'I understand the effects of these changes on my objects and buckets.'						
25. Now click [Save changes]						
								
### Creating AWS Groups, Policies And Users								
1. Create a user to access the S3 Bucket, do this through service called IAM
2. In AWS select the services menu, and choose IAM							
3. Create a group, click 'Groups' then [Create New Group]						
4. Choose sensible meaningful name for the group.
5. Click [Next Step] and then [Next Step] again, finally click [Create Group]						
6. Now click 'Policies' and then [Create Policy], Click on the 'JSON' tab.
7. Then click 'Import managed policy', search for S3 and select policy 'AmazonS3FullAccess' and click [Import]						
8. Now change the "Resource" section to a list and add the following:-
```				
"Resource"": [
    ""arn:aws:s3:::devtog-boutique-ado"",
    ""arn:aws:s3:::devtog-boutique-ado/*""
]"
```				
9. Note: first item is the bucket itself, the second indicates everything in that bucket					
10. Click [Next Tags], [Next: Review]		
11. Click [Review policy]						
12. Give the policy a name and description
13. Click [Create policy]						
14.	Now attach the policy to your new group, click on 'Groups'						
15. Click on the group you created						
16. Choose the 'Permissions' tab and click [Attach Policy]						
17. Search for the policy we just created, select it and click [Attach Policy]						
18.	Create a user to put in our group, click on 'Users', click [Add user]						
19. Enter a descriptive user name.
20. In 'Select AWS access type' select the 'Programmatic access' access type.						
21. Click [Next:Permissions]						
22. Select the group we created and click [Next: Tags]						
23. Click [Next:  Review], click [Create user]						
24. Click [Download .csv] to download the csv file which will contain the users access key and secret access key which we will use to authenticate them from our django app.
								

For more information and troubleshooting on creating an AWS S3 Bucket click [here](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)

