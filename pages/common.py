def create_navbar(request, current):
    navbar = []
    this_dict = {"link": "/", "label": "Home", "active": True if current == "home" else ""}
    navbar.append(this_dict)
    navbar.append({"label": "Services", "link": "page/1"})
    return navbar