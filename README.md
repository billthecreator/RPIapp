# RPIapp

Web server built on Flask.
Eventually will house apps accessible via local network.

### Reason ###
Although this will only be accessible only in my house, I'm building this server to teach myself Python. Doesn't really need a lot of the functionality, but I want to learn it, so why not?
The idea of custom building a server, from scratch, is pretty frick'n sweet.
Below are some screens of how it looks at the moment. When I push a major update, I will also update the screens.

## Screen of Admin Dashboard
!["Admin Dashboard"](/screens/admin.png)

The admin will have more control, edit links, colors, description, title, path, etc. While also monitoring the users who have an account.

#### Admin App Options Dropdown
!["App Options"](/screens/options.png)
#### Account Options Dropdown
!["Account Options"](/screens/user_options.png)

#### Dropdown Code
```html
<li class="dropdown">
    {{ g.user.username.upper() }} <!-- username -->
    <i class="fa fa-caret-down"></i>

    <div class="dropdown-content">
        <a href="{{ url_for('myAccount') }}">My account</a>
        <a href="{{ url_for('logout') }}">Sign out</a>
    </div>

</li>
```

## Screen of User Dashboard
!["User Dashboard"](/screens/user.png)

This is the same page, but logged in as a user. They can't do anything but click on the links.

## Todo List
* Email confirmation when registering account
* Profile Page
* Password forget system
* Settings page for all users

### This is how I access my Pi
!["remotePi"](/remoteRPI.PNG)
