# API Conventions for Scholarship System
## Overview
The user login protocol has been completed long before, here we only need to implement APIs for operations after login.
There are three kinds of users, marked with different user_type fields: 0 for students, 1 for teachers, whereas 2 for admins. When you write views handlers in Django, make sure you use the correct decorator for privilege authentication, e.g. **check_login for all users, check_teacher for teachers, etc**.

## Basic Conventions for Inter-communication

### Client -> Server

Always use **POST** request, and the post data is as follows. Note here I didn't use strict JSON grammar in order to sneak some comments in.

```js
{
    token: 'user_token_in_session_storage', // can be obtained through window.sessionStorage.token REQUIRED
    username: 'username_in_session_storage', // window.sessionStorage.username REQUIRED
    data: {} // payload data  OPTIONAL
}
```

### Server->Client

```JS
{
    status: 0, // status code, REQUIRED. 0: no error; -1: user not login; >0: server error
    message: 'error_msg', // only useful when status code > 0, OPTIONAL. Messages are in Chinese, and can be displayed directly on client side through `alert(res.message)`
    data: {} // payload data OPTIONAL
}
```

### Working Schedule

### Common

- [x] User login (for all types of users) and OAuth

### Student Side

- [x] Get notifications

- [x] Scholarship application form submission(Just send encoded JSON, and the server stores it. Yuh! That's sufficient. No more conversion is needed.)

- [x] Obtain scholarship application information for individual students

  (Note: reuse ApplyMain.vue page, but pass the student_id in the router parameter, and obtain this id in your handler, and POST necessary data to server to get the response)

  If router param is empty, it means the student just wanna check his/her own record.

- [x] Obtain ordered application list (send filter data to server, i.e. scholarship_name, doctor/bachelor, department, ordering criteria, and get the corresponding response. **Remember to handle pagination**, which means you have to POST some page number)

### Teacher Side

- [x] Change password (this works the same as admin, you just have to implement once. Please send MD5-encoded password)
- [x] Set the score of individual students (also in ApplyMain.vue. Hint: **the server can return user_type to client, allowing it to determine whether it is teacher, and display scoring gadgets accordingly. There is a variable named isTeacher in that component. Use it wisely**)

### Admin Side

- [x] Download XLSX/ CSV data of all applicants from ApplyList.vue. Similarly, there is a isAdmin in that component, if set to true, an extra DOWNLOAD XLSX button will show up.
- [x] Send notifications to all users. **Easy to implement! I have set up a rich-text editor in that page(/admin/notify), and you can obtain encoded HTML directly and send it to server**
- [x] Support upload DOC/ DOCX file to server and have it converted to HTML to form a notification. Hint: there are many Python libs that can support this. All that you need to take care of is a robust file uploader.
- [x] Scholarship application settings (/admin/apply_info_settings): add scholarship, edit scholarship, enable/disable the application, delete scholarship
- [x] Scoring rule settings (/admin/apply_score_rule_settings): add/edit/delete scoring rules. **The rules are encoded as JSON directly.**
- [x] Application material rule settings (/admin/apply_material_settings): add/edit/delete rules. **Encoded as JSON as well**.

### Challenging Tasks

- [x] Scoring rules parsers and score calculators

## Extra Notes

The system supports applications for multiple scholarships simultaneously (which is strongly reminiscent of that piece of Chinglish in Tsinghua course selection system: "**realizes the overlapping operation of teaching activities during multiple semesters including fall, spring and summer.**"). There are three major models, material rule, scoring rule and application info respectively. Their relationship is

**material rule <- scoring rule <- application info <- many application forms submitted**

This means we can have multiple material rules. For a single material rule, we can have multiple scoring rules for it. And for a single scholarship, we can match a specific scoring rule to it, and since the scoring rule depends on a specific material rule, what application materials this scholarship requires and how the scores are calculated are fully determined in this way.

When the applicants wanna apply for a certain scholarship, he/she can pick up one available in the system. And we can extend some functions such as import previous application data, provided their material rules are the same (to ensure compatibility). And this is why every entry in the **ApplyInfo** table is attached to a certain apply_score_rule_id/ apply_material_id (Foreign key constraint).

***Warning: have a look at backend/dbapp/models.py before you kick off!*** 
