# Jungle Peaks Brewing & Co.

## Table of Contents

- [Introduction](#introduction)
- [Marketing Plan](#marketing-plan)
  - [E-commerce Business Model](#e-commerce-business-model)
  - [Facebook](#facebook)
  - [Newsletter](#newsletter)
  - [SEO Content](#seo-content)
- [Technologies](#technologies)
  - [Robots.txt](#robotstxt)
  - [sitemap.xml](#sitemapxml)
- [Site Flow](#site-flow)
- [Wireframes](#wireframes)
- [Custom Models](#custom-models)
  - [ERD](#erd)
- [Agile Methodology](#agile-methodology)
  - [User Stories](#user-stories)
- [Features](#features)
- [Testing](#testing)
  - [Manual](#manual)
  - [Automated](#automated)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Future Features](#future-features)
- [Credits](#credits)


![alt text]( /static/images/screenshot-responsive.png)
 - https://ui.dev/amiresponsive?url=https://jungle-peaks-brewing-29d2cf7236c2.herokuapp.com/ 


## Introduction  

Welcome to **Jungle Peaks Brewing & Co.** – where adventure meets craft beer! 🍻🏔️  

Inspired by the untamed wilderness, **Jungle Peaks Brewing & Co.** is more than just a brewery—it’s a **bold expedition into flavoUr**. Every sip is crafted with locally sourced ingredients and a commitment to sustainability, delivering unique brews that capture the essence of adventure. Whether you’re a **seasoned craft beer enthusiast** or a newcomer looking for something wild, we’ve got the perfect pint for you!  

### **About the Project**  
This is a **full-stack e-commerce web application** built to bring Jungle Peaks Brewing & Co. online. It provides customers with an **immersive shopping experience**, allowing them to **browse products, make secure purchases, and book brewery tours and taproom experiences**. The site seamlessly integrates **frontend and backend technologies**, ensuring smooth navigation and reliable performance.  

From a **technical standpoint**, the project is built using **Django (Python) for backend functionality**, coupled with **HTML, CSS, JavaScript, and Bootstrap** for a responsive frontend. Payments are securely handled using **Stripe**, while **AWS S3** and **Imgix** are used for efficient static and media file storage and optimisation, ensuring **fast and scalable file serving**.  

### **🔹 Key Features & Functionality**  
✔️ **Full E-Commerce System** – Browse and buy craft beers and merchandise with a streamlined checkout process.  
✔️ **Brewery Tour Bookings** – Customers can easily book and manage brewery tours and taproom visits.  
✔️ **User Accounts & Order History** – Users can create accounts, track orders, and manage past bookings.  
✔️ **Secure Payments** – Integrated **Stripe** payment gateway for safe and seamless transactions.  
✔️ **Reviews & Community Engagement** – Customers can leave product reviews and interact with the brand.  
✔️ **Optimised Media Handling** – **AWS S3 & Imgix** are utilised for fast, efficient image processing and storage.  
✔️ **Admin Dashboard** – Business owners can manage products, orders, and customer interactions.  

### **Technology Stack**  
🔹 **Backend:** Django, Python, PostgreSQL  
🔹 **Frontend:** HTML, CSS, JavaScript, Bootstrap  
🔹 **Payments:** Stripe API  
🔹 **File Storage:** AWS S3 & Imgix for static and media file hosting  
🔹 **Deployment:** Hosted on **Heroku** with a PostgreSQL database  

Whether you’re here for a **smooth stout, a hoppy IPA, or an exclusive brewery tour**, **Jungle Peaks Brewing & Co.** is your **ultimate craft beer adventure**. 🌿🍺  

Let’s raise a glass to bold flavours, seamless technology, and the perfect pint.  
**Welcome to Jungle Peaks Brewing & Co.!** 🍻✨  

## 🛠️ Technologies Used  

This project leverages a range of modern technologies to ensure a **robust, scalable, and efficient e-commerce platform**.  

---

### **🌐 Frontend Technologies**  
The frontend provides a **responsive** and **user-friendly** experience using the following technologies:  

| Technology   | Description |  
|-------------|------------|  
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | **HTML5** - Provides the structure and markup for the website. |  
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | **CSS3** - Styles the website for a visually appealing UI. |  
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | **JavaScript** - Enables interactive elements and enhances UX. |  
| ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white) | **Bootstrap** - Ensures a responsive and mobile-friendly design. |  

---

### **⚙️ Backend Technologies**  
The backend is powered by **Django**, ensuring smooth database interactions, authentication, and business logic handling.  

| Technology   | Description |  
|-------------|------------|  
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | **Python** - The core programming language for backend logic. |  
| ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) | **Django** - A powerful Python framework for managing models, views, and authentication. |  
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white) | **PostgreSQL** - A reliable relational database for storing user and order data. |  
| ![Stripe](https://img.shields.io/badge/Stripe-008CDD?style=for-the-badge&logo=stripe&logoColor=white) | **Stripe API** - Handles secure payment processing for online purchases. |  

---

### **🗄️ Storage & File Handling**  
Handling **static and media files** efficiently with cloud-based storage solutions.  

| Technology   | Description |  
|-------------|------------|  
| ![AWS S3](https://img.shields.io/badge/AWS_S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) | **AWS S3** - Secure and scalable cloud storage for media files. |  
| ![Imgix](https://img.shields.io/badge/Imgix-1478FF?style=for-the-badge&logo=imgix&logoColor=white) | **Imgix** - Optimises and serves images efficiently to improve performance. |  

---

### **🚀 Deployment & Hosting**  
Ensuring smooth deployment and scalability for production.  

| Technology   | Description |  
|-------------|------------|  
| ![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white) | **Heroku** - Cloud platform used to deploy and manage the live site. |  
| ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white) | **Gunicorn** - A WSGI HTTP server for handling Django requests efficiently. |  
| ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) | **GitHub** - Version control and collaborative code management. |  

---

### **🔗 Additional Integrations**  
- **Django Allauth** – Handles user authentication and social logins.  
- **Whitenoise** – Manages static file handling for better performance.  
- **Cloudinary (Optional)** – Alternative media storage for image optimisation.  

---

This combination of technologies ensures **Jungle Peaks Brewing & Co.** delivers a **fast, secure, and scalable** shopping and booking experience! 🚀🍻  


# 📢 The Marketing Plan that would be set for implementation   

This marketing plan outlines a **strategic approach** for promoting Jungle Peaks Brewing & Co. in an **online marketplace**. While this is a **hypothetical plan**, it presents key considerations for **customer engagement, digital marketing strategies, and brand awareness**. These ideas could be implemented in reality to **strengthen the brand’s online presence, attract loyal customers, and drive sales**.  

Jungle Peaks Brewing & Co. is positioned as an **adventurous craft brewery**, drawing inspiration from **untamed landscapes and wild flavours**. The marketing approach would focus on **storytelling, experience-driven branding, and social engagement** to build a community around craft beer lovers and outdoor enthusiasts.  

---

## 🎯 1. Identifying the Target Audience  

### 🌍 Who Would Be Our Customers?
Jungle Peaks Brewing & Co. would appeal to:  
- **Craft beer enthusiasts (ages 25-45)** who appreciate **premium, small-batch brewing**.  
- **Adventurers & nature lovers** looking for a brand that aligns with their **explorative spirit**.  
- **Foodies & experience-seekers** interested in **beer pairings, events, and tastings**.  
- **Casual drinkers** who want something beyond mass-market beers.  
- **Subscription seekers** interested in **monthly beer deliveries**.  

### 📱 Where Would We Find Them?  
- **Instagram** – Highly visual platform for showcasing beer styles & brand identity.  
- **Facebook** – Building a local & online **community**, promoting events, and offering customer service.  
- **Twitter/X** – Quick updates, beer discussions, and engagement with industry trends.  
- **Reddit** – Subreddits like r/craftbeer & r/homebrewing for organic word-of-mouth marketing.  
- **YouTube** – Brewing tutorials, behind-the-scenes content, and beer tasting videos.  
- **Untappd** – Leveraging reviews and beer ratings to build credibility and discoverability.  

> **Marketing Insight**: The **strongest brand awareness strategy** would include a mix of **social engagement, content marketing, and experiential promotions** to ensure the brewery is perceived as an **adventurous, high-quality craft beer brand**.  

---

## 📢 2. Understanding & Meeting Consumer Needs  

### 🔎 What Would Our Customers Want?  
To develop an **effective marketing strategy**, we must identify **key customer motivations**:  
✅ **Access to unique, high-quality craft beers** with bold, adventurous branding.  
✅ **Education on beer styles & pairing recommendations** for casual & experienced drinkers.  
✅ **Exclusive offers, discounts, and early access** to seasonal or limited-edition brews.  
✅ **Engagement in a like-minded community** of beer lovers, foodies, and adventurers.  

### 📬 How Would We Deliver Value to Customers?  
- **📱 Social Media Storytelling** – Creating immersive Instagram & Facebook content to showcase the **brewing process, wild ingredients, and customer experiences**.  
- **📖 Blog Content** – Articles on **beer styles, food pairings, brewing techniques, and behind-the-scenes stories**.  
- **🎥 Video Marketing** – Brewery tour videos, tasting sessions, and interactive Q&A on platforms like YouTube.  
- **📩 Email Marketing** – A **well-segmented newsletter** offering **exclusive promotions, educational content, and early access to new beers**.  

> **Marketing Insight**: To position the brand as a **premium craft beer experience**, the focus should be on **educational and lifestyle-driven content**, paired with an **interactive and engaging social media strategy**.  

---

## 💰 3. Promotions & Sales Strategies  

### 🎟️ Types of Promotions to Consider  
✅ **Seasonal & Themed Sales** – “Tropical Tuesdays” (discounts on fruit-infused beers), **Winter Stout Specials**, or **Limited-Edition Small Batches**.  
✅ **First-Time Buyer Discounts** – A strategy to **convert new visitors into long-term customers**.  
✅ **Loyalty Rewards** – Customers earn points for **repeat purchases, referrals, and engagement**.  
✅ **Limited-Time Offers** – Flash sales on **subscription packages or exclusive beer launches**.  

### 📣 How Would We Announce These Offers?  
- **📩 Email Marketing** – Personalized discount campaigns & subscriber-only deals.  
- **📱 Social Media Promotions** – Eye-catching posts, countdown timers, and influencer collaborations.  
- **🌍 Website Pop-ups** – Non-intrusive reminders for **exclusive online-only discounts**.  
- **🔔 Push Notifications** – Instant alerts for **new beer releases & limited-time sales**.  

> **Marketing Insight**: The key to successful promotions would be **creating urgency** while maintaining a **sense of exclusivity and adventure**.  

---

## 🚀 4. Business Goals & Marketing Strategies  

### 🎯 Defining the Brewery’s Goals  
1. **Increase brand awareness** and position Jungle Peaks Brewing as an **adventurous craft beer brand**.  
2. **Drive online sales** through an engaging website, seamless e-commerce functionality, and unique product offerings.  
3. **Foster a loyal community** through consistent, engaging, and high-value content.  
4. **Expand reach via digital marketing efforts**, including **SEO, content marketing, and paid advertising**.  

### 🔥 Potential Marketing Strategies  
- **SEO-Focused Content**: Targeting niche **beer-related searches** (e.g., *adventurous IPA blends, best seasonal craft beers*).  
- **Social Media Engagement**: Encouraging **user-generated content & interactive beer experiences**.  
- **Content Marketing**: Blogs, videos & **collaborations with influencers** in food, travel, and craft beer.  
- **Email Marketing**: Well-segmented campaigns **tailored to different audience interests**.  

---

## 📊 5. Marketing Breakdown  

### 🔍 SEO Strategy  
- **Keyword Optimisation** – Targeting **craft beer-related search terms** that align with the brand’s theme.  
- **Evergreen Blog Content** – **Beer pairing guides, tasting notes, and brewing techniques**.  
- **Image & Meta Optimisation** – High-quality visuals & descriptions to improve **search engine rankings**.  

### 📱 Social Media Strategy  
- **Instagram:** Visual storytelling through **high-quality product photography & branded content**.  
- **Facebook:** Community-building with **exclusive group discussions, beer challenges, and events**.  
- **YouTube:** Educational brewing videos, behind-the-scenes footage, and product spotlights.  

### 📩 Email Marketing Strategy  
- **Segmented Email Lists** – Ensuring **personalised content based on customer preferences**.  
- **Exclusive Monthly Newsletter** – “Jungle Dispatch” featuring **beer launches, discounts, and adventure-themed articles**.  
- **Automated Campaigns** – Welcome sequences, abandoned cart reminders, and **VIP loyalty rewards**.  

---

## 💸 6. Advertising Budget Considerations  

### 📈 Where Would the Budget Go?  
1. **Highly-Targeted Social Media Ads** – Using Facebook & Instagram to **target beer lovers & adventure enthusiasts**.  
2. **Google Ads** – Optimising ads for searches like *best craft beer delivery* and *unique IPA subscriptions*.  
3. **Low-Cost, High-Impact Alternatives** – Content marketing, influencer collaborations, and **email campaigns**.  

---

## 🎨 Potential Branded Offerings  

### 🍺 Subscription Box Ideas  
- **Jungle Peaks Passport Box** – A **monthly subscription featuring a curated selection** of craft beers.  
- **Wild Brew Explorers Club** – Exclusive **early access to new releases and limited-edition batches**.  

### 🏷️ Taglines & Brand Messaging  
- *"Brewed at the Edge of Adventure."*  
- *"Where the Jungle Meets the Peaks."*  
- *"Crafting Nature's Boldest Flavours."*  

### 🍻 Seasonal Beer Line Concepts  
- **Banana Hop IPA** – A tropical IPA with **subtle banana and citrus notes**.  
- **Silverback Stout** – A **bold, roasted stout with rich chocolate tones**.  
- **Canopy Citrus Wheat** – A bright, hazy wheat beer with **hints of citrus zest**.  

---

## 📝 Final Thoughts  
This **hypothetical marketing plan** showcases how **Jungle Peaks Brewing & Co.** could establish a **strong brand identity** in the craft beer industry. By implementing **targeted digital marketing strategies, engaging content, and experiential branding**, this concept could thrive in an **online and physical marketplace**.  

The success of this approach would depend on **community engagement, customer experience, and storytelling**, reinforcing the brand as **not just a beer company—but an adventure waiting to be explored**.  

---

## **E-Commerce Business Model**  

The **Jungle Peaks Brewing & Co.** website follows a **B2C (Business-to-Consumer)** e-commerce model, selling directly to individual customers. The platform provides a seamless shopping and booking experience for both **physical products** and **services**.  

### ✅ **Key Aspects of the Business Model:**  
- **B2C (Business to Consumer):** Directly selling to craft beer enthusiasts, adventurers, and social drinkers.  
- **Physical Products:** Includes a wide range of **craft beers, merchandise, and curated gift sets**.  
- **Services:** Customers can book **brewery tours, beer tastings, and table reservations** online.  
- **Single Payment System:** Payments are made **per order or booking**, ensuring a straightforward checkout experience using **Stripe payment integration**.  

This model is **ideal for breweries** looking to expand their **customer base, increase brand awareness, and drive sales through digital channels**.  

---

## **Facebook Integration**  

![alt text]( /static/images/mock-facebook-page.png)  

Facebook plays a **vital role** in the marketing strategy for **Jungle Peaks Brewing & Co.**, providing **customer engagement, brand promotion, and event marketing**.  

### ✅ **How Facebook Benefits the Business:**  
- **Community Building:** Creates an **interactive space** where customers can **engage with posts, leave reviews, and share experiences**.  
- **Product Promotion:** Showcases new **beer releases, merchandise, and special offers** with engaging visual content.  
- **Event Awareness:** Promotes **brewery tours, taproom events, and limited-edition releases**.  
- **Targeted Ads:** Facebook Ads allow **precise audience targeting** to reach potential customers interested in **craft beer, brewery experiences, and online beer purchases**.  

A **strong social media presence** enhances **brand visibility and customer loyalty**, making Facebook a **key marketing tool** for the business.  

---

## **Newsletter Marketing**  

A **newsletter subscription** system is implemented to keep customers **informed, engaged, and returning for more**.  

### ✅ **Why Email Marketing Matters:**  
- **Exclusive Offers & Discounts:** Subscribers receive **early access** to deals, limited releases, and special promotions.  
- **New Beer Launches:** Customers stay updated on **new craft beer varieties** and seasonal brews.  
- **Event Reminders:** Automated emails notify users about their **upcoming brewery tours or taproom bookings**.  
- **Content Marketing:** Newsletters feature **brewing tips, beer pairings, and behind-the-scenes stories**, increasing brand engagement.  

#### 🔹 **Technology Used:**  
- **Django Email Backend** – Sends automated emails.  
- **Mailchimp API (Future Feature)** – For advanced email automation and segmentation.  

A **well-crafted email marketing strategy** helps retain customers and **boosts repeat sales** by keeping the brand **top of mind**.  

---

## **SEO Content Strategy**  

A **well-optimized SEO strategy** ensures **Jungle Peaks Brewing & Co.** ranks highly in **search engines**, driving **organic traffic** to the website.  

### ✅ **SEO Tactics Implemented:**  
- **Keyword Optimisation:** Targeting key search terms related to **craft beer, brewery tours, and beer delivery services**.  
- **Meta Tags & Open Graph Data:** Implementing **structured meta descriptions and social media preview tags** for improved visibility.  
- **High-Quality Content:** Blog posts and product descriptions are written **with SEO best practices** to rank for relevant queries.  
- **Image Optimisation:** Using **Imgix** for **fast-loading and SEO-friendly images**.  

### SEO Keywords

![alt text]( meta-seo-tags.png)

### Keyword Strategy for Jungle Peaks Brewing & Co.

The **SEO keyword selection** for Jungle Peaks Brewing & Co. was carefully crafted to enhance **search visibility**, attract the **right audience**, and improve **organic traffic**. Below is a breakdown of the strategy behind the chosen keywords:

#### 1️⃣ Targeting Niche & Industry-Specific Keywords  
- **"Amazon craft brewery"** – Targets users looking for unique, high-quality craft breweries in the Amazon theme.  
- **"Jungle Peaks Brewing"** – Ensures brand recognition and direct searches for the company.  
- **"IPA beer, Lager beer, Stout beer, Wheat Beer, Pale Ale, Sour beer, Seasonal Ale, Light Beer"** – Covers a wide range of **specific beer styles** to attract beer enthusiasts searching for their favourite brew types.  

#### 2️⃣ Capturing Search Intent (Transactional & Informational)  
- **"Buy beer online, beer delivery, beer store"** – Targets users with high **purchase intent** searching for online beer retailers.  
- **"Craft beer gifts"** – Appeals to gift buyers looking for unique beer-related products.  
- **"Best craft beer in Amazon"** – Optimises for **"best of"** search queries, which are often used by users looking for recommendations.  

#### 3️⃣ Expanding to Experience-Based Keywords  
- **"Amazon brewery tours, Amazon beer tastings, beer education, beer experiences, taproom"** – Focuses on **experience-driven searches**, attracting users interested in brewery visits, tastings, and educational events.  

#### 4️⃣ Strengthening Authority & Credibility  
- **"Jungle Peaks Brewing"** – Reinforces brand authority in the industry.  
- **"Beer education"** – Positions the business as a knowledge hub for craft beer enthusiasts.  
- **"Beer experiences"** – Highlights unique activities beyond just purchasing beer, appealing to experience seekers.  

### Overall Strategy:
- **Balanced approach** between **product, experience, and brand-related keywords**.  
- Targets **both commercial and informational search intent**.  
- Optimised for **highly searched beer styles, online purchases, and brewery visits**.  

This **SEO keyword strategy** ensures Jungle Peaks Brewing & Co. ranks for **valuable search terms**, reaching both **craft beer enthusiasts** and **potential customers** effectively.




## Robots.txt & Sitemap.xml
This project features both a robots.txt and sitemap.xml files for reasons outlined below:

### **robots.txt**
The `robots.txt` file is used to guide search engine crawlers on which pages or sections of the site they are allowed to index. It helps manage the crawling process to prevent unnecessary indexing of admin pages, private areas, or duplicate content.

- Allows search engines to crawl essential pages.
- Blocks access to sensitive areas (e.g., admin panel).
- Helps optimize crawl budget for better SEO.

### **sitemap.xml**
The `sitemap.xml` file is an essential component for SEO, as it provides search engines with a structured list of all important pages on the website. This ensures that pages are efficiently indexed and helps improve discoverability.

- Lists URLs for search engines to crawl efficiently.
- Includes metadata like last modified dates to prioritize updates.
- Improves site visibility and indexing speed for search engines.

Both files are crucial for **SEO optimisation** and ensuring that the **website structure is efficiently navigated by search engines**.


## Agile Methodology

![alt text]( /static/images/completed-agile.png)

KANBAN on github projects will be used and include 4 iterations:

| Iteration | Focus Areas                     | Key Deliverables                                    |
|-----------|----------------------------------|----------------------------------------------------|
| 1         | Foundational Features           | Product management, browsing, basic checkout.      |
| 2         | Enhanced Browsing and Deals     | Filtering, categorization, and deals functionality.|
| 3         | Events and Bookings             | Event booking, reviews, and taproom pages.         |
| 4         | Final Enhancements and Testing  | Newsletter, QR codes, order history, polish.       |



### User stories outlined
In the initial planning these were the user stories to complete:

| ID   | User Role       | Epic                    | User Story                                                                                               | MoSCoW Criteria |
|------|-----------------|-------------------------|---------------------------------------------------------------------------------------------------------|-----------------|
| ES1a | Business Owner  | Manage Products         | As a business owner, I want to add, edit, and delete products so that I can keep the inventory up-to-date. | Must Have       |
| ES1b | Business Owner  | Manage Products         | As a business owner, I want to upload images for products so that they are visually appealing to customers. | Must Have       |
| ES1c | Business Owner  | Manage Products         | As a business owner, I want to categorize products (e.g., beers, merchandise) so that customers can browse easily. | Should Have     |
| ES1d | Business Owner  | Manage Products         | As a business owner, I want to create seasonal collections or bundles (e.g., gift sets) so that I can offer unique promotions. | Could Have      |
| ES3a | Business Owner  | Taproom & Brewery Pages | As a business owner, I want to separate taproom events from brewery tours and tastings so that customers can easily find the type of event they want. | Must Have       |
| ES3b | Business Owner  | Taproom & Brewery Pages | As a business owner, I want to provide downloadable guides or maps for taproom and brewery tours so that customers have a seamless experience. | Could Have      |
| ES4a | Business Owner  | Deals & Promotions      | As a business owner, I want to highlight deals in the header navigation so that customers can easily find ongoing promotions. | Must Have       |
| ES4b | Business Owner  | Deals & Promotions      | As a business owner, I want to add a countdown timer for limited-time deals so that customers feel a sense of urgency to purchase. | Could Have      |
| ES5a | Business Owner  | FAQs                    | As a business owner, I want to leave FAQs on the website so that customers can quickly find answers to common questions. | Should Have     |
| ES6a | Business Owner  | Footer Links            | As a business owner, I want to display social media links in the footer so that customers can connect with us online. | Must Have       |
| ES6b | Business Owner  | Footer Links            | As a business owner, I want to include signup, privacy policy, and terms links in the footer so that I meet legal and compliance requirements. | Must Have       |
| ES6c | Business Owner  | Footer Links            | As a business owner, I want to include a “Contact Us” link in the footer so that customers can easily get in touch for inquiries or support. | Could Have      |
| ES7a | Customer        | Browse Products         | As a customer, I want to view all products so that I can browse beers and merchandise.                  | Must Have       |
| ES7b | Customer        | Browse Products         | As a customer, I want to see detailed product information, including images, prices, and descriptions, so that I can make informed purchase decisions. | Must Have       |
| ES7c | Customer        | Browse Products         | As a customer, I want to filter products by price, type, or popularity so that I can quickly find what I’m looking for. | Could Have      |
| ES8a | Customer        | Purchase Products       | As a customer, I want to purchase products online so that I can enjoy Jungle Peaks Brewing & Co. merchandise. | Must Have       |
| ES8b | Customer        | Purchase Products       | As a customer, I want to apply discount codes during checkout so that I can save money.                  | Could Have      |
| ES9a | Customer        | Order History           | As a customer, I want to see my order history so that I can track past purchases and reorder items.      | Should Have     |
| ES10a| Customer        | Book Tours & Tastings   | As a customer, I want to book brewery tours and tastings so that I can experience the brand firsthand.   | Must Have       |
| ES10b| Customer        | Book Tours & Tastings   | As a customer, I want to see my tour and tasting booking history so that I can keep track of my reservations. | Should Have     |
| ES10c| Customer        | Book Tours & Tastings   | As a customer, I want to receive a QR code for my event bookings so that I can check in easily.          | Could Have      |
| ES11a| Customer        | Customer Reviews        | As a customer, I want to leave reviews for products and events so that I can share my feedback and experiences. | Must Have       |
| ES11b| Customer        | Customer Reviews        | As a customer, I want to upvote helpful reviews so that others can see the most relevant feedback.       | Could Have      |
| ES12a| Customer        | Newsletter Signup       | As a customer, I want to sign up for the newsletter so that I can receive updates, deals, and event notifications. | Must Have       |
| ES12b| Business Owner  | Newsletter Signup       | As a business owner, I want to segment subscribers by interests (e.g., deals, events) so that I can send targeted campaigns. | Should Have     |
| ES12c| Customer        | Newsletter Signup       | As a customer, I want to receive exclusive discount codes as part of the newsletter signup so that I feel rewarded for subscribing. | Could Have      |

### User stories "won't have's"

All of the user stories were completed excluding these below: 

### **Changes:**
- **Marked as "Won't Have"**:
  - ES3b: Downloadable guides/maps for taproom & brewery tours.
  - ES8b: Apply discount codes during checkout.
  - ES8c: Monthly beer care package subscription.
  - ES10c: QR code for event bookings.
  - ES11b: Upvote helpful reviews.
  - ES12c: Exclusive discount codes for newsletter signup.

## Custom-models 

### ERD
Using DBDIAGRAM 
![alt text]( /static/images/ERD.png)


### Key Relationship Summary
The **Entity Relationship Diagram (ERD)** defines the core database structure for **Jungle Peaks Brewing & Co**. Below is a summary of key relationships between models:

#### **User & UserProfile**
- **One-to-One Relationship**
- Each `User` has a corresponding `UserProfile`, which stores additional details such as default address and phone number.

#### **User & Order**
- **One-to-Many Relationship**
- A `User` can place multiple `Orders`, but each `Order` belongs to one `UserProfile` (if logged in).

#### **Order & OrderLineItem**
- **One-to-Many Relationship**
- Each `Order` consists of multiple `OrderLineItem` records, linking it to specific `Products` and their quantities.

#### **Product & Category**
- **Many-to-One Relationship**
- A `Product` belongs to a single `Category`, but a `Category` can have multiple `Products`.

#### **User & Review**
- **One-to-Many Relationship**
- A `User` can submit multiple `Reviews`, but each `Review` belongs to one `User` and one `Product`.

#### **TourBooking & User**
- **Many-to-One Relationship**
- Each `TourBooking` is linked to a `User`, but a `User` can have multiple `TourBookings`.

#### **NewsletterSubscriber**
- **Standalone table** storing email subscriptions with interests and timestamps.

#### **ContactMessage**
- **Standalone table** storing messages submitted via the contact form.

These relationships define how **customers interact with the platform**, enabling smooth purchasing, booking, and feedback processes.

## Site Flow 
Using FIGMA

![alt text]( /static/images/siteflow.png)

## Wireframes
Using UIZARD I designed a canvas for my lifelike wireframes: 

![alt text]( /static/images/uizard-canvas.png)

### Desktop
#### Home Page
![alt text]( /static/images/homepage.jpeg)

#### Product List
![alt text]( /static/images/product-list.jpeg)

#### Product Detail
![alt text]( /static/images/product-detail.jpeg)

#### Shopping Cart 
![alt text]( /static/images/shopping-cart.jpeg)

#### Checkout
![alt text]( /static/images/checkout-page.jpeg)

#### Taproom 
![alt text]( /static/images/taproom.jpeg)

#### Tours & Tastings 
![alt text]( /static/images/tours-tasting-page.jpeg)

#### User Management
![alt text]( /static/images/user-management.jpeg)

## Features Overview

This section outlines the key features implemented in the Jungle Peaks Brewing & Co. website based on the **user stories**. Each feature is linked to the corresponding **user stories**, **database models** used, and includes relevant images showcasing the functionality.

---

### **1. Product Management (Admin)**
   - **Summary:** Business owners can fully manage products, including adding, editing, and deleting them to ensure inventory remains up to date. Products are categorized to enhance browsing, and seasonal collections or promotional bundles can be created.
   - **User Stories:**  
     - **ES1a:** Business owners can add, edit, and delete products to keep inventory up to date.  
     - **ES1b:** Upload images for products to make them visually appealing.  
     - **ES1c:** Categorize products (e.g., beers, merchandise) to improve browsing experience.  
     - **ES1d:** Create seasonal collections or bundles for promotional campaigns.  
   - **Models Used:** `Product`, `Category`

![Add Product]( /static/images/add-product-feature.png)
![Edit Product]( /static/images/edit-product-feature.png)
![Admin Product Management]( /static/images/admin-products.png)

---

### **2. Taproom & Brewery Pages**
   - **Summary:** The site separates taproom events from brewery tours and tastings to provide a better booking experience for users. Customers can clearly distinguish between the two when making a reservation.
   - **User Stories:**  
     - **ES3a:** Separate taproom events from brewery tours and tastings to enhance user experience.  
   - **Models Used:** `Booking`, `TourBooking`

![Separate Bookings]( /static/images/separate-bookings.png)
![Taproom Booking]( /static/images/taproom-booking.png)
![Tour Bookings]( /static/images/tour-bookings.png)

---

### **3. Deals & Promotions**
   - **Summary:** Promotions are highlighted in the header navigation, ensuring customers are always aware of ongoing deals. Additionally, a countdown timer for limited-time promotions creates urgency to encourage purchases.
   - **User Stories:**  
     - **ES4a:** Highlight deals in the header navigation for visibility.  
     - **ES4b:** Add a countdown timer for limited-time promotions to create urgency.  

![Promo Banner]( /static/images/promo-banner.png)

---

### **4. FAQs & Contact Information**
   - **Summary:** An FAQ section provides quick answers to common customer queries, reducing the need for direct inquiries. The contact form allows customers to submit messages for further assistance.
   - **User Stories:**  
     - **ES5a:** Display FAQs to provide quick answers to common queries.  
     - **ES6c:** Include a "Contact Us" link in the footer for customer inquiries.  
   - **Models Used:** `ContactMessage`

![Contact Feature]( /static/images/contact-feature.png)

---

### **5. Footer Links & Social Media**
   - **Summary:** Social media links in the footer help increase brand engagement, while legal links (signup, privacy policy, and terms) ensure compliance with industry regulations.
   - **User Stories:**  
     - **ES6a:** Display social media links in the footer for better engagement.  
     - **ES6b:** Include signup, privacy policy, and terms links in the footer to meet legal requirements.  

![Footer Feature]( /static/images/footer-feature.png)

---

### **6. Product Browsing & Filtering**
   - **Summary:** Customers can easily browse all products, view detailed information, and use filtering options to quickly find products based on price, type, or popularity.
   - **User Stories:**  
     - **ES7a:** Allow customers to view all products, including beers and merchandise.  
     - **ES7b:** Display detailed product information, including images, prices, and descriptions.  
     - **ES7c:** Enable filtering of products by price, type, or popularity for easy discovery.  
   - **Models Used:** `Product`, `Category`

![Search Bar]( /static/images/search-bar-feature.png)
![Product Filtering]( /static/images/product-filtering-feature.png)
![Product Detail]( /static/images/product-detail-feature.png)

---

### **7. Online Purchases & Checkout**
   - **Summary:** Customers can purchase products directly from the website, ensuring a seamless and secure checkout process.
   - **User Stories:**  
     - **ES8a:** Customers can purchase products online.  
   - **Models Used:** `Order`, `OrderLineItem`, `Product`
   
![Checkout Feature]( /static/images/checkout-feature.png)

---

### **8. Order History**
   - **Summary:** Customers can view their order history within their accounts, making it easy to track past purchases and reorder items.
   - **User Stories:**  
     - **ES9a:** Customers can view their order history to track past purchases.  
     - **ES9b:** Option to export order history as a PDF for record-keeping.  
   - **Models Used:** `Order`, `OrderLineItem`, `UserProfile`

![Order History]( /static/images/order-history-feature.png)

---

### **9. Tour & Tasting Bookings**
   - **Summary:** Customers can book brewery tours and tastings online, providing a streamlined reservation process. They can also view past bookings in their account history.
   - **User Stories:**  
     - **ES10a:** Customers can book brewery tours and tastings online.  
     - **ES10b:** View past tour and tasting bookings in their account.  
   - **Models Used:** `TourBooking`, `UserProfile`

![Tour Booking]( /static/images/tour-booking-feature.png)
![View Tour Bookings]( /static/images/view-tour-bookings.png)

---

### **10. Customer Reviews**
   - **Summary:** Customers can leave reviews for products and events, helping others make informed decisions and enhancing credibility.
   - **User Stories:**  
     - **ES11a:** Customers can leave reviews for products and events to share their experiences.  
   - **Models Used:** `Review`, `User`, `Product`
  
![Leave a Review]( /static/images/leave-review-feature.png)

---

### **11. Newsletter Signup & Marketing**
   - **Summary:** Customers can sign up for newsletters to receive updates, promotions, and event notifications. Business owners can segment subscribers based on interests for targeted campaigns.
   - **User Stories:**  
     - **ES12a:** Customers can sign up for newsletters to receive updates, deals, and event notifications.  
     - **ES12b:** Business owners can segment subscribers by interests for targeted campaigns.  
   - **Models Used:** `NewsletterSubscriber`

![Newsletter Signup]( /static/images/newsletter-signup-feature.png)
![Newsletter Admin]( /static/images/newsletter-admin-feature.png)

## Testing

### Validation

#### HTML
![alt text]( /static/images/home-valid-html.png)

![alt text]( /static/images/products-valid-html.png)

![alt text]( /static/images/taproom-valid-html.png)

![alt text]( /static/images/tours-valid-html.png)

![alt text]( /static/images/contact-valid-html.png)

![alt text]( /static/images/profile-valid-html.png)

#### CSS

The core list of CSS Files:

- BASE
- CHECKOUT
- HOME
- PRODUCT
- PRODUCT DETAIL
- PROFILE 
- TAPROOM
- TOUR 

These all received a validation pass from WS3 
![alt text]( /static/images/css-valid.png)

#### JAVASCRIPT

base script

![alt text]( /static/images/base-js-valid.png)

pop up newsletter

![alt text]( /static/images/newsletter-js-valid.png)

quantity input - product 

![alt text]( /static/images/quantity-input-js-valid.png)

Stripe element js

![alt text]( /static/images/stripe-element-valid.png)

Product page scroll up btn

![alt text]( /static/images/product-scroll-valid.png)

#### PYTHON

Tours views

![alt text]( /static/images/tours-views-pass.png)

Taproom Views

![alt text]( /static/images/taproom-views-pass.png)


Profile views 

![alt text]( /static/images/profile-views-pass.png)

Product views

![alt text]( /static/images/product-views-pass.png)

Home Views

![alt text]( /static/images/home-views-pass.png)

Checkout Views

![alt text]( /static/images/checkout-views-pass.png)

Bag Views

![alt text]( /static/images/bag-views-pass.png)

### Lighthouse & Accessibility

Home

![alt text]( /static/images/home-lighthouse.png)

Products

![alt text]( /static/images/products-lighthouse.png)

Product Detail 

![alt text]( /static/images/product-detail-lighthouse.png)

Taproom 

![alt text]( /static/images/taproom-lighthouse.png)

Tours

![alt text]( /static/images/tours-lighthouse.png)

Contact

![alt text]( /static/images/contact-lighthouse.png)

Profile

![alt text]( /static/images/profile-lighthouse.png)

### Manual Forms

#### Purchasing with Stripe

Payment success message 
![alt text]( /static/images/purchase-stripe.png)

Checkout contents of £7.14

![alt text]( /static/images/checkout-contents.png)

Stripe events log correctly displaying charge of £7.14
![alt text]( /static/images/stripe-hooked-up.png)

#### Booking a table

Book a table success

![alt text]( /static/images/book-table.png)

Edit table booking 

![alt text]( /static/images/edit-table.png)

Cancel table booking 

![alt text]( /static/images/cancel-table.png)

#### Booking a tour

Availability 

![alt text]( /static/images/tour-availability.png)

Book tour success

![alt text]( /static/images/book-tour.png)


Edit tour booking 

![alt text]( /static/images/edit-tour.png)

Cancel tour booking

![alt text]( /static/images/cancel-tour.png)

#### Newsletter Signup

Newsletter pop-up

![alt text]( /static/images/newsletter-popup.png)

Newsletter successful sign-up 

![alt text]( /static/images/newsletter-signup.png)

Newsletter admin panel

![alt text]( /static/images/newsletter-admin.png)


#### Write a review

Add review success 

![alt text]( /static/images/add-review.png)

Delete review success 

![alt text]( /static/images/delete-review.png)

Edit review success

![alt text]( /static/images/edit-review.png)

#### Contact message 

Contact message sent

![alt text]( /static/images/send-message.png)

Contact admin message received 

![alt text]( /static/images/admin-message.png)


#### Profile dashboard 

All website activity successfully collected into profile dashboard

![alt text]( /static/images/profile-dashboard.png)


#### Product Categories

Merch shows merch

![alt text]( /static/images/merch-show.png)

Gift sets show gift sets

![alt text]( /static/images/gift-sets-show.png)

IPA sort shows IPAs 

![alt text]( /static/images/ipa-show.png)


#### Add Product

Add a product 

![alt text]( /static/images/add-product.png)

Delete a product 

![alt text]( /static/images/delete-product.png)

Edit a product

![alt text]( /static/images/edit-product.png)


#### Register for an account 
Verification email

![alt text]( /static/images/confirmation-email-sent.png)

Email received

![alt text]( /static/images/email-received.png)

Confirmed email

![alt text]( /static/images/confirm-email.png)


### Automated 


### Checkout views tests 

![alt text]( /static/images/checkout-tests-pass.png)

## 🛠️ Checkout Test Cases

| **Test Name**                               | **Description**                                                      | **Expected Outcome**                                      |
|---------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------|
| `test_cache_checkout_data`                  | Ensures checkout data is cached in Stripe's PaymentIntent.          | Stripe's API modifies the payment intent successfully.   |
| `test_checkout_page_loads`                  | Checks if the checkout page loads correctly.                         | Page loads with status `200`, correct template is used.  |
| `test_checkout_post_creates_order`          | Tests order creation after form submission.                          | Order and line items are saved in the database.          |
| `test_checkout_redirects_when_bag_is_empty` | Ensures checkout redirects when the shopping bag is empty.           | Redirects to `products` with a message.                  |
| `test_checkout_success_view`                | Verifies successful checkout page loads correctly.                   | Order confirmation page displays order details.          |
| `test_checkout_fails_for_invalid_product`   | Tests checkout failure when a product in the bag does not exist.     | Redirects to `view_bag` with an error message.           |

✅ **All tests passed successfully, ensuring checkout functionality is working as expected.**

This Django test suite ensures that the checkout process functions correctly, covering order creation, payment processing, and error handling. All tests have **passed successfully** ✅.

## 📌 What was Tested
The test suite includes various unit tests to validate the checkout functionality:

### 🔹 Checkout Page Loads Properly
- Ensures the checkout page renders correctly with the correct template.
- Uses `mock_stripe_create` to simulate Stripe PaymentIntent creation.

### 🔹 Caching Checkout Data
- Tests if checkout data is successfully cached in Stripe's PaymentIntent.
- Uses `mock_stripe_modify` to mock the Stripe API.

### 🔹 Order Creation
- Verifies that submitting the checkout form correctly creates an order.
- Ensures the order contains the correct customer details and products.

### 🔹 Handling Empty Cart Checkout
- Ensures users **cannot proceed to checkout** with an empty cart.
- Confirms redirection back to the products page with an appropriate message.

### 🔹 Checkout Success Page
- Verifies that the order success page displays correctly after a successful checkout.

### 🔹 Handling Missing Products
- Simulates a scenario where a product in the cart does not exist.
- Ensures the user is redirected back to their shopping bag with an error message.

## 📊 Test Results
✅ **All tests passed successfully**, confirming that the checkout process works as expected.

## 🐛 Bugs  

### 🛠️ **Bug: Quantity Buttons Incrementing by 2 Instead of 1**  
**Issue:**  
- The quantity increment and decrement buttons were increasing/decreasing by **2 instead of 1**.  

**Root Cause:**  
- Duplicate event binding: Both inline JavaScript (`onclick`) and jQuery were handling the click event, causing it to fire twice.  

**✅ Solution:**  
1. **Remove the Duplicate Binding:**  
   - Choose **either** inline JavaScript **or** jQuery to handle the event.  
   - If using jQuery, remove the inline `onclick` attributes to prevent duplicate handlers.  

2. **Ensure Unique Class Names:**  
   - Avoid using multiple conflicting classes on the same element (e.g., `increase-btn` and `increment-qty` together).  
   - This prevents multiple handlers from triggering on a single click.  

---

### 🎨 **Bug: Blue Highlight Around Account Dropdown on Mobile (Heroku Deployment)**  
**Issue:**  
- When tapping the account dropdown on **mobile devices**, a **blue highlight** appeared due to the browser’s default `outline` behavior for focusable elements (`<a>` tags).  

**✅ Solution:**  
1. **Remove Focus Outline on Click:**  
   - Apply `outline: none;` but **only when using a mouse/touch**, ensuring accessibility for keyboard users.  
   - Example CSS Fix:  
     ```css
     .user-icon:focus {
         outline: none;
     }
     ```  
2. **Maintain Accessibility:**  
   - While removing the outline for mouse/touch users, keep it for keyboard navigation to comply with accessibility best practices.  

---

### 🔄 **Bug: Update Button Not Submitting the Form**  
**Issue:**  
- Clicking the **"Update"** button in the shopping bag visually changed the quantity but **did not submit the form**, meaning the session data was **not updated**.  

**Root Causes:**  
1. **Incorrect `.update-link` Selector:**  
   - The jQuery selector was not correctly identifying the form associated with each product.  
   - The previous code targeted `.product-details` and `.quantity-container`, which are **not always present** in **desktop view**.  

2. **Quantity (`+` and `-`) Buttons Were Updating Visually, But Not Updating the Session:**  
   - Clicking the buttons **changed the number in the input field** but **did not submit the form**, so the cart was not updated in the session.  

3. **Event Listeners Not Binding Correctly:**  
   - If `.update-link` could not find the correct form, `.submit()` was **not being triggered** properly.  

**✅ Solution:**  
1. **Fix `.update-link` to Target the Correct Form:**  
   - Updated the selector to **look inside `<td>` (table cell)** as another possible container.  
   - This ensures that, whether in **mobile** or **desktop** view, the correct `.update-form` is found and submitted.  

2. **Prevent `+` and `-` Buttons from Automatically Updating the Cart:**  
   - Previously, clicking `+` or `-` changed the value in the input field but **did not trigger a session update**.  
   - Now, the session updates **only when the user clicks "Update"**.  

3. **Fix Form Submission Logic:**  
   - Ensured that clicking "Update" correctly **finds the nearest `<td>` or `.product-details` container** and submits the **correct form**.  

---

✅ **All these bugs have been identified and fixed, improving the checkout and shopping experience.** 🎉  
## Deployment

This project was deployed on heroku - the steps to do so are number below:

### Heroku

#### Step 1: Create a Heroku app

1. Go to your Heroku app dashboard > Settings > Config Vars. Add:
   - Key: `DISABLE_COLLECTSTATIC`
   - Value: `1`  
   _(Static files will be handled later.)_

   ```bash
   # Create a Heroku app and set DISABLE_COLLECTSTATIC
   heroku create your-app-name
   heroku config:set DISABLE_COLLECTSTATIC=1

#### Step 2: Update your code for deployment 
1.	Install the required dependencies and update requirements.txt:

        pip install gunicorn django-heroku whitenoise psycopg2-binary
        pip freeze > requirements.txt

    - the requirements.txt tells heroku what version to run the app at. 
    - This ensures heroku has the correct packages during deployment.
    
```bash
echo "web: gunicorn event_scheduler.wsgi" > Procfile
```

- Update your settings debug == **false**

- Add .herokuapp.com to ALLOWED_HOSTS: 

```bash
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', '.herokuapp.com']
```

- Add whitenoise to static files  

```bash
django.middleware.security.SecurityMiddleware 
whitenoise.middleware.WhiteNoiseMiddleware
```

- Static file configs: 
```bash
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATIC_URL = '/static/' 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
  ```

- Push changes to github via commit.
```bash
git add .
git commit -m "Prepare app for Heroku deployment"
git push origin main
```

#### Step 3: Deploy to heroku

1.	Connect Heroku to your GitHub repository:

    Go to the Heroku dashboard > Deploy tab.
    Select “GitHub” as the deployment method and connect your repository.

2.	Deploy the main branch:

    Scroll to the “Manual deploy” section.
    Select the main branch and click “Deploy Branch.”

3.	Monitor activity logs to ensure a successful deployment.

#### Step 4: Post-deployment

1.	Connect to your PostgreSQL database:
	•	Add the DATABASE_URL and SECRET_KEY to env.py:

```bash
import os
os.environ["DATABASE_URL"] = "your-database-url"
os.environ["SECRET_KEY"] = "your-secret-key"
```

be sure to add env.py to gitignore

2.	Update settings.py to use dj_database_url:

```bash
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}
```

3.	Add DATABASE_URL and SECRET_KEY to Heroku Config Vars via the dashboard.
4.	Run database migrations and create a superuser:

- Run your database migrations "python manage.py makemigrations" "python manage.py migrate" 

- create superuser for admin access "python manage.py createsuperuser"

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

- You need to then collectstatic:
    - remove DISABLE_COLLECTSTATIC config var > then run in terminal 
    
```bash
    "python manage.py collectstatic"
```

- You should be able to then deploy your heroku app with your database connected and begin production. 

**My heroku app link:** 
- [the website link](https://jungle-peaks-brewing-29d2cf7236c2.herokuapp.com/)

## 🚀 Future Features

While the core features of **Jungle Peaks Brewing & Co.** have been successfully implemented, there are some functionalities that were initially planned but not included in this version. Additionally, there are exciting possibilities for future development to enhance user experience and business operations.

---

## 📌 Features for Future Implementation  

### 1️⃣ Enhanced Taproom & Brewery Tour Experience  
#### **Downloadable guides/maps for taproom & brewery tours** (**ES3b**)  
- Adding **downloadable maps or digital guides** for brewery tours and taproom events would improve customer experience by providing clear navigation and details about available attractions.  
- **Potential Implementation:**  
  - Generate **dynamic PDF guides** for customers.  
  - Integrate **Google Maps API** with custom brewery routes.  

---

### 2️⃣ Expanded Checkout & Discounts  

#### **Apply discount codes during checkout** (**ES8b**)  
- Allowing customers to use **promo codes or loyalty discounts** during checkout would incentivize repeat purchases.  
- **Potential Implementation:**  
  - Create a **discount model** that tracks active codes.  
  - Implement **validation logic** in the checkout process.  
  - Add **auto-applied discounts** for newsletter subscribers or loyal customers.  

#### **Exclusive discount codes for newsletter signup** (**ES12c**)  
- Rewarding newsletter subscribers with a **personalized discount code** would increase subscription rates and encourage purchases.  
- **Potential Implementation:**  
  - Generate **unique discount codes per user**.  
  - Send via **automated emails** using **Mailchimp API** or Django’s email system.  

---

### 3️⃣ Subscription Model for Beer Lovers  

#### **Monthly beer care package subscription** (**ES8c**)  
- Introducing a **beer subscription box** where customers receive curated beers every month would generate **recurring revenue** and boost customer retention.  
- **Potential Implementation:**  
  - Allow users to **subscribe to a plan** (e.g., **Monthly, Quarterly, Seasonal**).  
  - Use **Stripe Subscriptions API** for automatic billing.  
  - Implement an **admin dashboard** for managing curated selections.  

---

### 4️⃣ Improved Customer Engagement & Reviews  

#### **Upvote helpful reviews** (**ES11b**)  
- Implementing an **upvote/downvote system** for product reviews would help customers find the most relevant feedback.  
- **Potential Implementation:**  
  - Add a **vote counter** to reviews.  
  - Use **AJAX or WebSockets** to update votes dynamically.  
  - Display **top-rated reviews** first.  

---

### 5️⃣ Event Booking Enhancements  

#### **QR Code for event bookings** (**ES10c**)  
- Sending a **QR code ticket** to customers upon booking an event would simplify check-in and improve security at brewery tours or taproom events.  
- **Potential Implementation:**  
  - Use **Python’s qrcode library** to generate unique QR codes.  
  - Validate **QR codes at event entry**.  
  - Implement **email automation** to send tickets upon successful booking.  

---

## 🎯 Summary  
✅ The planned **“Won’t Have”** features have been reframed into **future development opportunities**.  
✅ Expanding discounts, subscriptions, and event booking features would **enhance user experience**.  
✅ Additional features like a **loyalty program, mobile app, and beer-pairing recommendations** could significantly improve engagement. 

## Credits 

