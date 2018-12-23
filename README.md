# Categories

This project shows the relationship between the category and related items. You are able as a logged in user to: 
- Create new Category
- Create new Item
- Edit Existing Item
- Delete Existing item

# Technologies Used

- Flask
- SqlAlchemy
- Google Auth Api
- Vagrant

## Installation



```bash
cd categoires && run vagrant up 
```


## Run Application
in the current categories directory run:
```bash
vagrant ssh 
```
```bash
cd /vagrant
```
```bash
python app.py
```

## Endpoints 


| Description  | URI 
| :------------ |:---------------:
| /     | Home Page
| /process_google_auth     | Processing Google Authentication   
|  /logout | Logout and flush the session
|  /category/create | Show Category Create Page
|  /category/save| Save Category New Values
|  /categories| Get all Categories as JSON endpoint
|  /category/<int:category_id>/items| Get All Items related to category_id
|  /category/<int:category_id>/item| Show Item Create Page
|  /category/<int:category_id>/item/save|Save Item New Values
|  /item/<int:item_id>/delete| Delete an Item
|  /item/<int:item_id>/edit| Edit Item Page
|  /item/<int:item_id>/edit/apply| update new item values
